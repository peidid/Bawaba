"""Agentic oversight for the AI-diagnosis channel: an LLM agent decides, a verifier checks.

The oversight agent is a language model with tools. For each draft it reads the case (the
stakeholder profile, the test results, the history, any human request), and then:

  retrieve_rules(query)        searches the policy library (rules, stakeholder profiles, law)
  simulate_policy(policy)      computes, inside the hospital and without any outside model,
                               how many people in the population directory a candidate field
                               policy would leave matching (k)
  propose_rule_change(...)     proposes an amendment when the case shows a rule is too loose,
                               too strict or missing; tightening applies to the case at once,
                               loosening waits for the DPO (GW-OV-02)
  decide(...)                  RELEASE | REDRAFT (with a field policy it chooses) | ASK_HUMAN |
                               ESCALATE (with a memo) | BLOCK, with a reason and cited rule IDs

There is no if/then decision table here. What is not left to the model is a small verifier
(verify()) that checks a decision against the guardrail parameters declared in the policy
library ("Param:" lines such as k_min = 5). The verifier only says yes or no and why; when it
refuses, the agent is told why and decides again (GW-OV-01). Thresholds live in the policy
files, so changing a rule changes behaviour with no code change.
"""
import json
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Optional

import agents
import rag
from policy import FIELDS, PRESETS, linkage_k, preset_name, rank, visible

ROOT = Path(__file__).parent
OVERSIGHT_MODEL = os.getenv("BAWABA_OVERSIGHT_MODEL", agents.OUTSIDER)
OVERSIGHT_EFFORT = os.getenv("BAWABA_OVERSIGHT_EFFORT", "low")
AMENDMENTS = ROOT / "policies" / "amendments_proposed.jsonl"
DECISIONS = ["RELEASE", "REDRAFT", "ASK_HUMAN", "ESCALATE", "BLOCK"]
# which direction of a parameter change makes the gateway stricter (more private)
STRICTER_IF = {"k_min": "up", "cell_min": "up", "spot_check_rate": "up", "dp_epsilon": "down", "max_drafts": "down",
               "red_team_must_fail": "true", "utility_must_hold": "true", "redraft_needs_local_k": "true",
               "human_review_if": "superset", "never_release": "superset"}


# ---------------------------------------------------------------- the case the agent decides on
@dataclass
class Case:
    pid: str
    person: dict
    registry: list
    reveals: Optional[dict]
    small_group: bool
    sensitive_history: Optional[str]
    profile: dict                                   # lib.profile(channel)
    rounds: list = field(default_factory=list)      # one entry per tested draft
    human: list = field(default_factory=list)       # human actions, in order
    tightened: dict = field(default_factory=dict)   # case-level parameter overrides (tightening only)
    amendments: list = field(default_factory=list)
    human_approved: bool = False

    def params(self):
        return {**self.profile["params"], **self.tightened}

    @property
    def policy(self):
        return self.rounds[-1]["policy"]

    def k_of(self, policy):
        return linkage_k(self.person, self.registry, policy, self.reveals)

    def triggers(self):
        """Mandatory-review triggers (GW-HITL-01) that hold for this record right now."""
        on = {"small_group": self.small_group, "sensitive_history": bool(self.sensitive_history),
              "loosened_by_human": any(h.get("loosened") for h in self.human), "escalated": False}
        return [t for t in self.params().get("human_review_if", []) if on.get(t)]


def round_entry(version, policy, k, identified, candidates, reasoning, searches, utility_ok, draft_top, full_top,
                findings, source, text):
    return {"version": version, "policy": dict(policy), "preset": preset_name(policy), "k": k, "identified": identified,
            "candidates": candidates, "attacker_reasoning": reasoning, "searches": searches, "utility_ok": utility_ok,
            "draft_top3": draft_top, "full_top3": full_top, "findings": findings, "source": source, "text": text}


# ---------------------------------------------------------------- local analysis (no outside model)
def describe(policy, base=None):
    if base is None:
        return ", ".join(f"{f}: {policy[f]}" for f in FIELDS)
    ch = [f"{f} {base[f]} → {policy[f]}" for f in FIELDS if policy[f] != base[f]]
    return ", ".join(ch) or "no change"


def what_if(case, policy):
    """k after moving one field one step more private, and one step more detailed."""
    more_private, more_detail = {}, {}
    for f, d in FIELDS.items():
        opts, i = d["options"], d["options"].index(policy[f])
        if i + 1 < len(opts):
            more_private[f"{f} → {opts[i + 1]}"] = case.k_of({**policy, f: opts[i + 1]})
        if i > 0:
            more_detail[f"{f} → {opts[i - 1]}"] = case.k_of({**policy, f: opts[i - 1]})
    return more_private, more_detail


# ---------------------------------------------------------------- what the agent is told
SYSTEM = """You are the oversight agent of Bawaba, a privacy gateway at a hospital in Qatar. For one patient record and one recipient you decide what may leave the hospital. You are an agent: read the evidence, use your tools, decide, and explain your reasons by citing rule IDs.

Goal: release the most useful draft that is safe.
- Safe: enough people in the population directory match everything the draft reveals (k at least k_min) AND the red-team attacker could not single the patient out.
- Useful: the diagnostic tool's top answer on the draft is the same as on the full note.
Keep the clinical context that drives the diagnosis (work exposure, travel, season); generalize or remove what singled the patient out (nationality, exact age, job title and employer, address). The fields and their options go from most detailed to most private.
Facts about the drafts: direct identifiers (name, Qatar ID, MRN, date of birth, phone, street address, names of relatives and clinicians) are always replaced by placeholders such as [NAME] or [QID]; a placeholder means the identifier is already gone, it is not a leak. The red team attacks a sample of records; when it was not run on a record, privacy is judged on k alone and red_team_must_fail is satisfied. Mandatory human review applies to the final draft: redraft and let the tests run first, and ask the human once a tested draft passes.

How to work:
1. Read the case. If you are unsure which rule applies, call retrieve_rules.
2. Before a REDRAFT, call simulate_policy on one or more candidate policies to check k locally. Change as few fields as needed and prefer the candidate that keeps the most clinically useful detail. Do not repeat a policy that failed; going back to an earlier version that passed both tests is allowed.
3. If a human asked for detail, keep as much of their request as you can: first try making other fields more private to compensate, and generalize the requested field only if nothing else reaches k_min. If nothing safe keeps the request, go back to the last version that passed. Say what you changed.
4. If the diagnosis was lost but privacy has a wide margin, you may restore detail the diagnosis needs, as long as the local k check still passes.
5. Decide with exactly one call to decide:
   RELEASE: every guardrail passes and no mandatory human review applies.
   REDRAFT: give the complete new field policy; the minimizer redrafts it and the tests run again.
   ASK_HUMAN: the draft passes the tests but a rule requires a human review (or a human must choose); message_to_human is one sentence for the reviewer.
   ESCALATE: privacy and the diagnosis conflict and no policy you can find passes both; message_to_human is a 60-90 word memo with two options.
   BLOCK: nothing can safely leave.
6. Rules can change. If this case gives concrete evidence that a rule is too loose (for example the attacker narrowed the candidates to only a few even though k met k_min, or the patient is in a small nationality group), too strict, or missing something this stakeholder needs, call propose_rule_change before you decide. A tightening applies to this case at once; a loosening goes to the Data Protection Officer and does not apply now.

A verifier checks your decision against the guardrail parameters in the policy library. If it refuses, read why and decide again."""


def _enum(f, nullable=False):
    opts = list(FIELDS[f]["options"])
    return {"type": ["string", "null"], "enum": opts + [None]} if nullable else {"type": "string", "enum": opts}


TOOLS = [
    {"type": "function", "name": "retrieve_rules", "strict": True,
     "description": "Search the hospital's policy library: gateway rules, stakeholder profiles (who may receive what) and Qatari legal provisions. Returns the 3 best matches with IDs and text.",
     "parameters": {"type": "object", "additionalProperties": False,
                    "properties": {"query": {"type": "string", "description": "What you need to know, in plain words"}},
                    "required": ["query"]}},
    {"type": "function", "name": "simulate_policy", "strict": True,
     "description": "Check a candidate field policy locally, inside the hospital, with no outside model: returns k (how many people in the population directory match everything a note under this policy would reveal), whether k meets k_min, and what the note would reveal.",
     "parameters": {"type": "object", "additionalProperties": False,
                    "properties": {f: _enum(f) for f in FIELDS}, "required": list(FIELDS)}},
    {"type": "function", "name": "propose_rule_change", "strict": True,
     "description": "Propose an amendment to one parameter of a rule in the policy library (for example GW-AI-02 k_min). Tightening applies to this case at once and is queued for the governance committee; loosening waits for the DPO.",
     "parameters": {"type": "object", "additionalProperties": False,
                    "properties": {"rule_id": {"type": "string"}, "param": {"type": "string"},
                                   "new_value": {"type": "string"},
                                   "reason": {"type": "string", "description": "The evidence from this case, in one or two sentences"}},
                    "required": ["rule_id", "param", "new_value", "reason"]}},
    {"type": "function", "name": "decide", "strict": True,
     "description": "Your decision for this draft. Call exactly once, when you are ready.",
     "parameters": {"type": "object", "additionalProperties": False,
                    "properties": {
                        "decision": {"type": "string", "enum": DECISIONS},
                        **{f: {**_enum(f, nullable=True), "description": f"REDRAFT only: the new setting for {f}; null otherwise"} for f in FIELDS},
                        "reason": {"type": "string", "description": "One or two plain sentences: why, naming the evidence (k, the attacker, the diagnosis, review flags)"},
                        "cited_rules": {"type": "array", "items": {"type": "string"}, "description": "IDs of the rules this decision relies on"},
                        "message_to_human": {"type": ["string", "null"], "description": "ASK_HUMAN: one sentence for the reviewer. ESCALATE: a 60-90 word memo with two options. Otherwise null."}},
                    "required": ["decision", *FIELDS, "reason", "cited_rules", "message_to_human"]}},
]


def brief(case: Case, lib: rag.Library) -> str:
    prof, P, src = case.profile, case.params(), case.profile["param_source"]
    cur = case.rounds[-1]
    lines = [f"You are deciding for: {prof['title']} (channel {prof['channel']}, profile {prof['id']}).",
             f"- Needs: {prof.get('needs', '')}", f"- Receives: {prof.get('receives', '')}",
             f"- Never: {prof.get('never', '')}", f"- On request: {prof.get('on_request', '')}", "",
             "Guardrails in force (from the policy library; the verifier checks these):"]
    for k in ("k_min", "red_team_must_fail", "utility_must_hold", "human_review_if", "max_drafts", "redraft_needs_local_k",
              "review_tested_drafts_only", "block_needs_most_private_tested"):
        if k in P:
            v = ", ".join(P[k]) if isinstance(P[k], list) else P[k]
            note = " (raised for this case by an amendment you proposed)" if k in case.tightened else ""
            lines.append(f"- {k} = {v} ({src.get(k, 'case')}){note}")
    trig = case.triggers()
    lines += ["", f"This record: small nationality group: {'yes' if case.small_group else 'no'}; "
                  f"sensitive history: {case.sensitive_history or 'none'}.",
              f"Mandatory human review applies now: {', '.join(trig) if trig else 'no'}"
              + (" (a human has already approved an earlier version)" if case.human_approved else ""), "",
              "Fields and options (most detailed → most private):"]
    lines += [f"- {f}: {' | '.join(d['options'])}" for f, d in FIELDS.items()]
    lines += ["", "Drafts tested so far:"]
    for r in case.rounds:
        atk = ("SINGLED OUT the patient" if r["identified"] else
               "did not single out the patient" + (f" ({r['candidates']} candidates left)" if r["candidates"] else "")) \
            if r["identified"] is not None else "not run on this record (sampled records only; privacy judged on k)"
        lines.append(f"v{r['version']} [{r['source']}] policy {{{describe(r['policy'])}}}: k = {r['k']}; red team {atk}; "
                     f"diagnosis {'kept' if r['utility_ok'] else 'CHANGED'} ({(r['draft_top3'] or ['?'])[0]} vs full note {(r['full_top3'] or ['?'])[0]})")
    mp, md = what_if(case, cur["policy"])
    lines += ["", f"Current draft v{cur['version']} in detail:",
              f"- attacker's reasoning: {cur['attacker_reasoning'] or 'n/a'}",
              f"- full note top-3: {cur['full_top3']}; this draft top-3: {cur['draft_top3']}",
              f"- findings the tool used: {cur['findings'] or 'n/a'}",
              "- what-if, computed locally (k if ONE field moves one step):",
              "  more private: " + ("; ".join(f"{a}: k={b}" for a, b in mp.items()) or "none"),
              "  more detailed: " + ("; ".join(f"{a}: k={b}" for a, b in md.items()) or "none")]
    if case.human:
        lines += ["", "Human input on this record:"]
        for h in case.human:
            lines.append(f"- {h['role']} {h['action']}" + (f": \"{h['suggestion']}\"" if h.get("suggestion") else "")
                         + (f" → fields changed: {h['changes']}" if h.get("changes") else ""))
    if case.amendments:
        lines += ["", "Rule changes you proposed on this case: " + "; ".join(
            f"{a['rule_id']} {a['param']} → {a['new_value']} ({a['status']})" for a in case.amendments)]
    lines += ["", "Text of the current draft (exactly what would be released):", '"""', cur["text"][:2600], '"""',
              "", "Decide what happens next."]
    return "\n".join(lines)


# ---------------------------------------------------------------- guardrail verifier (no decision logic)
def verify(d: dict, case: Case):
    """Checks a decision against the guardrail parameters declared in the policy library. Returns (ok, why, rules)."""
    P, src, cur = case.params(), case.profile["param_source"], case.rounds[-1]
    if d["decision"] == "RELEASE":
        fails, rules = [], []
        if cur["k"] < P.get("k_min", 0):
            fails.append(f"k = {cur['k']} is below k_min = {P['k_min']}"); rules.append(src.get("k_min", "case"))
        if P.get("red_team_must_fail") and cur["identified"]:
            fails.append("the red team singled the patient out"); rules.append(src.get("red_team_must_fail"))
        if P.get("utility_must_hold") and not cur["utility_ok"]:
            fails.append("the top diagnosis changed"); rules.append(src.get("utility_must_hold"))
        trig = case.triggers()
        if trig and not case.human_approved:
            fails.append("a human must review first (" + ", ".join(trig) + ")"); rules.append(src.get("human_review_if"))
        return (not fails), "; ".join(fails), sorted({r for r in rules if r})
    passes = cur["k"] >= P.get("k_min", 0) and not cur["identified"] and cur["utility_ok"]
    budget_left = len(case.rounds) < P.get("max_drafts", 99)
    if d["decision"] == "ASK_HUMAN" and P.get("review_tested_drafts_only") and not passes and budget_left:
        return False, ("a human reviews only a tested draft that passes; REDRAFT and let the tests run first, "
                       "or ESCALATE if no policy can pass both tests"), [src.get("review_tested_drafts_only"), "GW-HITL-02"]
    if d["decision"] == "BLOCK" and P.get("block_needs_most_private_tested") and budget_left:
        most_private = {f: FIELDS[f]["options"][-1] for f in FIELDS}
        if most_private not in [r["policy"] for r in case.rounds]:
            return False, ("test the most private policy before blocking: "
                           + describe(most_private)), [src.get("block_needs_most_private_tested")]
    if d["decision"] == "REDRAFT":
        pol, tested = d["policy"], [r["policy"] for r in case.rounds]
        if pol == cur["policy"]:
            return False, "that is the current draft's policy; a redraft must change something", []
        if pol in tested:   # going back is allowed only to a version that passed both tests (GW-HITL-03)
            r = next(r for r in case.rounds if r["policy"] == pol)
            passed = r["k"] >= P.get("k_min", 0) and not r["identified"] and r["utility_ok"]
            if not passed:
                return False, f"this policy was already tested as v{r['version']} and failed", []
        if len(case.rounds) >= P.get("max_drafts", 99):
            return False, f"max_drafts = {P['max_drafts']} reached: ask a human, escalate or block", [src.get("max_drafts")]
        if P.get("redraft_needs_local_k"):
            k = case.k_of(pol)
            if k < P.get("k_min", 0):
                return False, f"under that policy k = {k} < k_min = {P['k_min']}; it cannot pass, so do not ask the red team", [src.get("redraft_needs_local_k"), src.get("k_min")]
        return True, "", [src.get("redraft_needs_local_k")] if P.get("redraft_needs_local_k") else []
    return True, "", []


def _direction(param, old, new):
    rule = STRICTER_IF.get(param)
    try:
        if rule == "up":
            return "tighten" if float(new) > float(old) else "loosen"
        if rule == "down":
            return "tighten" if float(new) < float(old) else "loosen"
        if rule == "true":
            return "tighten" if new is True else "loosen"
        if rule == "superset":
            o, n = set(old if isinstance(old, list) else [old]), set(new if isinstance(new, list) else [new])
            return "tighten" if n >= o and n != o else "loosen"
    except (TypeError, ValueError):
        pass
    return "unknown"


def handle_proposal(args, case: Case, lib: rag.Library):
    rid, param = args.get("rule_id", "").strip(), args.get("param", "").strip()
    rule = lib.rule(rid)
    if not rule or param not in rule["params"]:
        return {"status": "rejected", "why": f"{rid} has no parameter '{param}'"}
    old = case.params().get(param, rule["params"][param])
    new = rag.parse_value(args.get("new_value", ""))
    if isinstance(old, list) and not isinstance(new, list):
        new = [new] if new not in old else list(old)
    if new == old:
        return {"status": "rejected", "why": "no change"}
    direction = _direction(param, old, new)
    applies = direction == "tighten" and case.params().get("tighten_applies_now", True)
    if applies:
        case.tightened[param] = new
    entry = {"ts": datetime.now(timezone.utc).isoformat(timespec="seconds"), "record": case.pid, "rule_id": rid,
             "rule_version": rule["version"], "param": param, "old_value": old, "new_value": new,
             "direction": direction, "reason": args.get("reason", ""),
             "status": ("applied to this case; queued for the governance committee" if applies
                        else f"pending {case.params().get('loosen_requires', 'DPO')} approval; not applied")}
    case.amendments.append(entry)
    with open(AMENDMENTS, "a") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry


def _normalize(args, case):
    cur = case.policy
    pol = {f: (args.get(f) if args.get(f) in FIELDS[f]["options"] else cur[f]) for f in FIELDS}
    dec = args.get("decision") if args.get("decision") in DECISIONS else "ASK_HUMAN"
    return {"decision": dec, "policy": pol if dec == "REDRAFT" else None, "reason": (args.get("reason") or "").strip(),
            "cited_rules": [r for r in (args.get("cited_rules") or []) if isinstance(r, str)][:6],
            "message": (args.get("message_to_human") or "").strip() or None}


# ---------------------------------------------------------------- the agent loop
def decide(case: Case, lib: rag.Library, on_step: Optional[Callable[[str, dict], None]] = None,
           model: str = None, max_turns: int = 8) -> dict:
    """One oversight round. Returns {decision, policy, reason, cited_rules, message, steps, refusals, usage, model}."""
    model = model or OVERSIGHT_MODEL
    emit = on_step or (lambda *a: None)
    steps, refusals, usage = [], [], {"model": model, "in": 0, "out": 0, "calls": 0}
    inp = [{"role": "user", "content": brief(case, lib)}]
    for turn in range(max_turns):
        force = turn >= max_turns - 1
        resp = agents.client.responses.create(
            model=model, instructions=SYSTEM, input=inp, tools=TOOLS, reasoning={"effort": OVERSIGHT_EFFORT},
            tool_choice={"type": "function", "name": "decide"} if force else "auto")
        u = agents._usage(resp, model)
        usage["in"] += u["in"]; usage["out"] += u["out"]; usage["calls"] += 1
        calls = [o for o in resp.output if o.type == "function_call"]
        inp += resp.output
        if not calls:
            inp.append({"role": "user", "content": "Use your tools if you need them, then call decide."})
            continue
        for c in calls:
            try:
                args = json.loads(c.arguments or "{}")
            except json.JSONDecodeError:
                args = {}
            if c.name == "retrieve_rules":
                found = lib.retrieve(args.get("query", ""), k=3)
                step = {"tool": "retrieve_rules", "query": args.get("query", ""), "rules": [x["id"] for x in found],
                        "briefs": [rag.brief(x) for x in found]}
                out = rag.as_prompt(found) or "No matching rules."
            elif c.name == "simulate_policy":
                pol = {f: args.get(f) if args.get(f) in FIELDS[f]["options"] else case.policy[f] for f in FIELDS}
                k = case.k_of(pol)
                ok = k >= case.params().get("k_min", 0)
                step = {"tool": "simulate_policy", "policy": pol, "change": describe(pol, case.policy), "k": k, "meets_k_min": ok}
                out = json.dumps({"k": k, "k_min": case.params().get("k_min"), "meets_k_min": ok,
                                  "reveals": sorted(visible(case.person, pol, case.reveals)),
                                  "already_tested": pol in [r["policy"] for r in case.rounds]})
            elif c.name == "propose_rule_change":
                entry = handle_proposal(args, case, lib)
                step = {"tool": "propose_rule_change", **{k: entry.get(k) for k in ("rule_id", "param", "old_value", "new_value", "direction", "status", "reason", "why")}}
                out = json.dumps({k: entry.get(k) for k in ("status", "why", "old_value", "new_value", "direction")}, default=str)
            elif c.name == "decide":
                d = _normalize(args, case)
                ok, why, grules = verify(d, case)
                step = {"tool": "verifier", "decision": d["decision"], "ok": ok, "why": why, "rules": grules,
                        "change": describe(d["policy"], case.policy) if d["policy"] else None}
                steps.append(step); emit("oversight.step", step)
                if ok:
                    return {**d, "steps": steps, "refusals": refusals, "usage": usage, "model": model}
                refusals.append(why)
                out = f"REFUSED by the guardrail verifier: {why}. Rules: {', '.join(grules) or 'n/a'}. Decide again."
                inp.append({"type": "function_call_output", "call_id": c.call_id, "output": out})
                continue
            else:
                step, out = {"tool": c.name, "error": "unknown tool"}, "Unknown tool."
            steps.append(step); emit("oversight.step", step)
            inp.append({"type": "function_call_output", "call_id": c.call_id, "output": out})
    why = "the oversight agent did not reach a decision the guardrails accept" + (f" (last refusal: {refusals[-1]})" if refusals else "")
    return {"decision": "ASK_HUMAN", "policy": None, "reason": why, "cited_rules": ["GW-OV-01"], "message": why.capitalize() + ".",
            "steps": steps, "refusals": refusals, "usage": usage, "model": model, "fallback": True}


def detail_score(policy):
    """How much quasi-identifying detail a policy keeps: 2 = most detailed option, 0 = most private (max 9)."""
    return sum(len(FIELDS[f]["options"]) - 1 - rank(f, policy[f]) for f in FIELDS)


if __name__ == "__main__":   # quick look at one decision on cached L1 results:  python oversight_agent.py P1017
    import sys
    from policy import render
    pid = sys.argv[1] if len(sys.argv) > 1 else "P1017"
    pats = {p["pid"]: p for p in json.loads((ROOT / "data/patients.json").read_text())}
    reg = json.loads((ROOT / "data/registry.json").read_text())
    rec = {r["pid"]: r for r in json.loads((ROOT / "results/pipeline.json").read_text())["records"]}[pid]
    p, lib = pats[pid], rag.Library()
    case = Case(pid, p["person"], reg, p.get("context_reveals"), p["person"]["nationality"] in {"Kenyan", "British", "Sudanese", "Jordanian", "Sri Lankan", "Pakistani"},
                p["sensitive_history"], lib.profile("ai_diagnosis"))
    lv = rec["levels"]["L1"]; atk = (lv.get("llm_attack") or {}).get("submission") or {}
    case.rounds.append(round_entry(1, PRESETS["L1"], lv["k"], lv["llm_reidentified"], atk.get("candidates_remaining"),
                                   atk.get("reasoning"), len((lv.get("llm_attack") or {}).get("trace", [])), lv["agrees_with_full_note"],
                                   lv["ranked"], rec["levels"]["L0"]["ranked"], lv["findings"], "certified policy", render(p["segments"], PRESETS["L1"])))
    res = decide(case, lib, on_step=lambda t, s: print(" ", t, json.dumps({k: v for k, v in s.items() if k != "briefs"}, default=str)[:300]))
    print(json.dumps({k: res[k] for k in ("decision", "policy", "reason", "cited_rules", "message", "refusals", "usage")}, indent=1, default=str))
