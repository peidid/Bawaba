"""Bawaba control room: runs the gateway loop for one request, live, and streams
every agent event to the browser. Pauses at human checkpoints.

    .env311/bin/python server.py            # then open http://localhost:8341

Every session is recorded to recordings/<id>.json, and the page can replay any
recording at any speed (the no-network fallback for the presentation).
"""
import hashlib
import json
import threading
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from pydantic import BaseModel

import agents
import oversight_agent as OA
import rag
from policy import (FIELDS, FIELD_LABELS, LADDER, OPTION_LEVEL, PRESETS, TAG_FIELD, funnel, is_looser,
                    linkage_k, preset_name, render, stricter)

ROOT = Path(__file__).parent
REC = ROOT / "recordings"
REC.mkdir(exist_ok=True)
LIVE_CACHE = ROOT / "results" / "cache_live.json"
SMALL_GROUPS = {"Kenyan", "British", "Sudanese", "Jordanian", "Sri Lankan", "Pakistani"}
DIRECT = {"NAME", "QID", "MRN", "DOB", "PHONE", "RELATIVE", "CLINICIAN"}

PATIENTS = {p["pid"]: p for p in json.loads((ROOT / "data/patients.json").read_text())}
REGISTRY = json.loads((ROOT / "data/registry.json").read_text())
_lock = threading.Lock()


def h(text):
    return hashlib.md5(text.encode()).hexdigest()[:10]


def load_cache():
    out = {}
    for path in (ROOT / "results/cache_openai.json", LIVE_CACHE):
        try:
            out.update(json.loads(path.read_text()))
        except Exception:
            pass
    return out


def cached(key, fn):
    c = load_cache()
    if key in c:
        return c[key]
    val = fn()
    with _lock:
        try:
            live = json.loads(LIVE_CACHE.read_text())
        except Exception:
            live = {}
        live[key] = val
        LIVE_CACHE.write_text(json.dumps(live, ensure_ascii=False))
    return val


def playbook_for(policy):
    name = preset_name(policy)
    if name == "custom":   # nearest preset that is no stricter than this policy
        name = "L2" if any(policy[f] in ("exact", "keep") for f in FIELDS) else "L3"
    c = load_cache()
    for k, v in c.items():
        if k.startswith(f"playbook|{name}|"):
            return v
    samples = [p["notes"][name] for p in list(PATIENTS.values())[::40][:3]]
    return cached(f"playbook|{name}|3", lambda: agents.write_playbook(name, samples))


def segments_view(p, policy, prev_policy):
    """Rendered segments with tags, so the page can colour and diff them."""
    out = []
    for s in p["segments"]:
        tag = s.get("tag")
        field = TAG_FIELD.get(tag)
        lvl = OPTION_LEVEL[policy[field]] if field else "L1"
        text = s[lvl] if (field or tag) else s["text"]
        changed = False
        if prev_policy is not None and field:
            changed = s[OPTION_LEVEL[prev_policy[field]]] != text
        kind = "direct" if tag in DIRECT or tag == "ADDRESS" and not field else "field" if field else "sensitive" if tag == "SENSITIVE_HX" else "plain"
        out.append({"t": text, "tag": tag, "field": field, "kind": kind, "changed": changed,
                    "orig": s["text"] if tag else None})
    return out


class Session:
    def __init__(self, pid, start="L1"):
        self.id = datetime.now().strftime("%m%d-%H%M%S-") + uuid.uuid4().hex[:4]
        self.pid, self.p = pid, PATIENTS[pid]
        self.start_preset = start
        self.events, self.cond = [], threading.Condition()
        self.t0 = time.time()
        self.paused, self.step_tokens = False, 0
        self.action, self.action_ev = None, threading.Event()
        self.done = False
        self.lib = rag.Library()          # re-read per session: editing a policy file takes effect immediately
        self.decisions, self.case = [], None

    # ---- event stream
    def emit(self, typ, agent, **data):
        with self.cond:
            ev = {"seq": len(self.events), "t": round(time.time() - self.t0, 2), "type": typ, "agent": agent, "data": data}
            self.events.append(ev)
            self.cond.notify_all()
        (REC / f"{self.id}.json").write_text(json.dumps(
            {"id": self.id, "pid": self.pid, "recorded": datetime.now(timezone.utc).isoformat(timespec="seconds"),
             "events": self.events}, ensure_ascii=False))
        return ev

    def cite(self, for_agent, ids=(), query=None, k=2, applies=None):
        """Exact lookups for enforced rules + BM25 retrieval of related policy/legal text."""
        exact = [self.lib.rule(i) for i in ids if self.lib.rule(i)]
        found = self.lib.retrieve(query, k=k, applies=applies, exclude={c["id"] for c in exact}) if query else []
        chunks = exact + found
        if chunks:
            self.emit("policy.retrieved", "policy", for_agent=for_agent, query=query,
                      rules=[dict(rag.brief(c), how="lookup" if c in exact else "retrieved") for c in chunks])
        return chunks

    def gate(self):
        with self.cond:
            while self.paused and self.step_tokens == 0 and not self.done:
                self.cond.wait(0.5)
            if self.step_tokens:
                self.step_tokens -= 1

    def wait_human(self):
        self.action_ev.clear()
        self.action_ev.wait()
        a, self.action = self.action, None
        return a

    # ---- the loop
    def run(self):
        try:
            self._run()
        except Exception as e:  # surface errors on screen rather than hanging the demo
            self.emit("error", "system", message=f"{type(e).__name__}: {e}")
        finally:
            self.done = True
            with self.cond:
                self.cond.notify_all()

    def on_oversight_step(self, version, step):
        """Streams the oversight agent's tool calls to the page (and its rule lookups to the Policy basis panel)."""
        light = {k: v for k, v in step.items() if k != "briefs"}
        self.emit("oversight.step", "oversight", version=version, **light)
        if step["tool"] == "retrieve_rules" and step.get("briefs"):
            self.emit("policy.retrieved", "policy", for_agent="oversight", query=step.get("query"),
                      rules=[dict(b, how="retrieved") for b in step["briefs"]])
        if step["tool"] == "verifier" and step.get("rules"):
            found = [self.lib.rule(r) for r in step["rules"] if r and self.lib.rule(r)]
            if found:
                self.emit("policy.retrieved", "policy", for_agent="verifier", query=None,
                          rules=[dict(rag.brief(c), how="lookup") for c in found])
        if step["tool"] == "propose_rule_change":
            self.emit("oversight.amendment", "oversight", version=version, **light)

    def _run(self):
        p, per = self.p, self.p["person"]
        prof = self.lib.profile("ai_diagnosis")          # stakeholder profile + guardrail parameters, read from the library
        case = OA.Case(p["pid"], per, REGISTRY, p.get("context_reveals"), per["nationality"] in SMALL_GROUPS,
                       p["sensitive_history"], prof)
        self.case = case
        flags = [f for f, on in (("sensitive history", bool(p["sensitive_history"])),
                                 ("small nationality group", per["nationality"] in SMALL_GROUPS)) if on]
        self.emit("session.start", "request", pid=p["pid"], channel="External AI diagnostic tool",
                  purpose="diagnostic decision support", condition_hidden=p["condition"],
                  patient={"nationality": per["nationality"], "sex": per["sex"], "age": per["age"],
                           "occupation": per["occupation"], "small_group": per["nationality"] in SMALL_GROUPS,
                           "sensitive_history": p["sensitive_history"]},
                  flags=flags, fields={f: {"label": FIELD_LABELS[f], "options": FIELDS[f]["options"]} for f in FIELDS},
                  registry_size=len(REGISTRY), k_threshold=prof["params"]["k_min"], oversight_model=OA.OVERSIGHT_MODEL,
                  profile={k: prof.get(k) for k in ("id", "title", "needs", "receives", "never", "on_request")},
                  guardrails={k: [v, prof["param_source"].get(k)] for k, v in prof["params"].items()})
        self.gate()
        base_top, base_ranked = None, None
        policy, source, prev_policy, version = dict(PRESETS[self.start_preset]), "certified policy", None, 0
        self.emit("oversight.policy", "oversight", policy=policy, preset=preset_name(policy),
                  reason=f"loads the certified channel policy ({self.start_preset}) for profile {prof['id']}")
        history = []
        while True:
            version += 1
            self.gate()
            text = render(p["segments"], policy)
            self.emit("minimizer.draft", "minimizer", version=version, policy=dict(policy), preset=preset_name(policy),
                      segments=segments_view(p, policy, prev_policy), source=source)
            self.gate()
            # utility team and red team in parallel
            self.emit("tests.start", "oversight", version=version)
            if base_top is None:   # reference answer: the full note, diagnosed inside the hospital
                base = cached(f"diag|{h(p['notes']['L0'])}", lambda: agents.diagnose(p["notes"]["L0"]))
                base_ranked = base.get("ranked") or []
                base_top = (base_ranked or [None])[0]
                self.emit("utility.baseline", "utility", ranked=base_ranked, note="full note, inside the hospital")
            with ThreadPoolExecutor(2) as ex:
                fu = ex.submit(lambda: agents.diagnose(text))
                pb = playbook_for(policy)
                self.emit("red.strategy", "red", version=version, level=preset_name(policy),
                          weakest_point=(pb.get("playbook") or {}).get("weakest_point", ""),
                          strategies=[s["name"] for s in (pb.get("playbook") or {}).get("strategies", [])][:4])
                fa = ex.submit(lambda: agents.attack(text, REGISTRY, pb, on_event=lambda k, d: self.emit(
                    f"red.{k}", "red", version=version, **d)))
                d = fu.result()
                ranked = d.get("ranked") or []
                util_ok = bool(ranked) and ranked[0] == base_top
                self.emit("utility.result", "utility", version=version, ranked=ranked, findings=d.get("findings", ""),
                          baseline_top=base_top, passed=util_ok)
                a = fa.result()
            sub = a.get("submission") or {}
            reid = sub.get("pid") == p["pid"]
            k = linkage_k(per, REGISTRY, policy, p.get("context_reveals"))
            self.emit("red.result", "red", version=version, identified=reid, guessed_pid=sub.get("pid"),
                      guessed_name=sub.get("name"), candidates=sub.get("candidates_remaining"),
                      confidence=sub.get("confidence"), reasoning=sub.get("reasoning"), true_name=per["name"],
                      searches=len(a.get("trace", [])), k=k,
                      funnel=funnel(per, REGISTRY, policy, p.get("context_reveals")))
            priv_ok = k >= case.params()["k_min"] and not reid
            history.append({"version": version, "preset": preset_name(policy), "privacy": priv_ok, "utility": util_ok, "k": k})
            case.rounds.append(OA.round_entry(version, policy, k, reid, sub.get("candidates_remaining"), sub.get("reasoning"),
                                              len(a.get("trace", [])), util_ok, ranked, base_ranked, d.get("findings", ""),
                                              source, text))
            self.gate()

            # agentic oversight: the agent reads the case, uses its tools and decides; the verifier checks the decision
            self.emit("oversight.start", "oversight", version=version, model=OA.OVERSIGHT_MODEL)
            res = OA.decide(case, self.lib, on_step=lambda typ, step, v=version: self.on_oversight_step(v, step))
            decision, why = res["decision"], res["reason"]
            self.decisions.append({"version": version, "decision": decision, "reason": why, "cited_rules": res["cited_rules"],
                                   "refusals": res["refusals"], "model": res["model"], "usage": res["usage"]})
            self.emit("oversight.verdict", "oversight", version=version, privacy=priv_ok, utility=util_ok, k=k,
                      identified=reid, decision=decision, reason=why, flags=flags, history=[dict(x) for x in history],
                      rules=res["cited_rules"], next_policy=res["policy"], message=res["message"],
                      change=OA.describe(res["policy"], policy) if res["policy"] else None,
                      refusals=res["refusals"], by_agent=True, model=res["model"], k_min=case.params()["k_min"],
                      tools=[s["tool"] for s in res["steps"]])
            if decision == "RELEASE":
                self.finish_release(version, policy, text, "automatic: oversight agent, guardrails passed")
                return
            if decision == "REDRAFT":
                prev_policy, policy, source = policy, res["policy"], "oversight"
                self.emit("oversight.policy", "oversight", policy=policy, preset=preset_name(policy), reason=why)
                continue
            if decision == "BLOCK":
                self.emit("block", "oversight", version=version, reason=why)
                self.audit("BLOCK_KEEP_LOCAL", version, policy, "blocked by the oversight agent")
                return
            if decision == "ESCALATE":
                self.emit("oversight.memo", "oversight", memo=res["message"] or why)
            ask = (res["message"] if decision == "ASK_HUMAN" and res["message"] else why)

            # human checkpoint
            while True:
                self.emit("human.wait", "human", version=version, reason=ask, privacy=priv_ok, utility=util_ok,
                          flags=flags, policy=policy)
                act = self.wait_human()
                role, kind = act.get("role", "clinician"), act.get("action")
                self.emit("human.action", "human", role=role, action=kind,
                          detail={k2: v for k2, v in act.items() if k2 not in ("role", "action")})
                case.human.append({"role": role, "action": kind, "suggestion": act.get("suggestion")})
                if kind == "approve":
                    if priv_ok:
                        case.human_approved = True
                        self.finish_release(version, policy, text, f"approved by {role}")
                        return
                    if role == "dpo" and act.get("legal_basis") and act.get("reason"):
                        self.finish_release(version, policy, text, f"DPO override: {act['legal_basis']}", override=True)
                        return
                    self.emit("human.rejected", "oversight",
                              message="This release failed the privacy test. Only the DPO can override, with a legal basis and a reason.")
                    continue
                if kind == "block":
                    self.emit("block", "oversight", version=version, reason=act.get("reason") or f"blocked by {role}")
                    self.audit("BLOCK_KEEP_LOCAL", version, policy, f"blocked by {role}")
                    return
                if kind == "stricter":
                    n2, p2 = stricter(policy)
                    if not p2:
                        self.emit("human.rejected", "oversight", message="Already at the strictest preset.")
                        continue
                    prev_policy, policy, source = policy, p2, "human"
                    case.human[-1].update(changes={f: p2[f] for f in FIELDS if p2[f] != prev_policy[f]}, loosened=False)
                    self.emit("oversight.policy", "oversight", policy=policy, preset=n2, reason=f"{role} asked for stricter")
                    break
                if kind in ("set_policy", "suggest"):
                    new = dict(policy)
                    if kind == "suggest":
                        ctx = rag.as_prompt(self.cite("minimizer", ["GW-HITL-03"], query=act.get("suggestion", "") + " clinical context occupation travel small nationality group", k=2))
                        r = agents.interpret_suggestion(act.get("suggestion", ""), policy, text, ctx)
                        new.update(r["changes"])
                        self.emit("human.interpreted", "minimizer", suggestion=act.get("suggestion", ""),
                                  changes=r["changes"], explanation=r["explanation"], cited_rules=r.get("cited_rules", []))
                    else:
                        new.update({f: v for f, v in (act.get("policy") or {}).items() if f in FIELDS and v in FIELDS[f]["options"]})
                    if new == policy:
                        self.emit("human.rejected", "oversight", message="No change to the release policy.")
                        continue
                    if is_looser(new, policy) and not (act.get("reason") or kind == "suggest"):
                        self.emit("human.rejected", "oversight", message="Loosening a release needs a reason.")
                        continue
                    case.human[-1].update(changes={f: new[f] for f in FIELDS if new[f] != policy[f]}, loosened=is_looser(new, policy))
                    prev_policy, policy, source = policy, new, "human"
                    self.emit("oversight.policy", "oversight", policy=policy, preset=preset_name(policy),
                              reason=f"{role} changed the policy; re-testing before release")
                    break

    def finish_release(self, version, policy, text, how, override=False):
        self.emit("release", "oversight", version=version, policy=policy, preset=preset_name(policy), how=how,
                  override=override, text=text)
        self.audit("RELEASE", version, policy, how)

    def audit(self, decision, version, policy, how):
        entry = {"ts": datetime.now(timezone.utc).isoformat(timespec="seconds"), "channel": "ai_diagnosis",
                 "record": self.pid, "version": version, "decision": decision, "policy": policy, "how": how,
                 "policy_library": self.lib.versions(),
                 "rules_cited": sorted({r["id"] for e in self.events if e["type"] == "policy.retrieved" for r in e["data"]["rules"]}),
                 "oversight": [{k: v for k, v in x.items() if k != "usage"} for x in self.decisions],
                 "oversight_model": OA.OVERSIGHT_MODEL,
                 "guardrail_refusals": sum(len(x["refusals"]) for x in self.decisions),
                 "rule_change_proposals": (self.case.amendments if self.case else []),
                 "events": len(self.events)}
        with open(ROOT / "results" / "audit_log_live.jsonl", "a") as fh:
            fh.write(json.dumps(entry) + "\n")
        self.emit("audit", "oversight", entry=entry)
        self.emit("session.end", "system")


SESSIONS: dict = {}
app = FastAPI(title="Bawaba control room")


class StartReq(BaseModel):
    pid: str
    start: str = "L1"


class ActionReq(BaseModel):
    role: str = "clinician"
    action: str
    policy: Optional[dict] = None
    suggestion: Optional[str] = None
    reason: Optional[str] = None
    legal_basis: Optional[str] = None


@app.get("/")
def index():
    return FileResponse(ROOT / "control" / "index.html")


@app.get("/api/patients")
def patients():
    res_path = ROOT / "results/pipeline.json"
    picks = {}
    if res_path.exists():
        for r in json.loads(res_path.read_text())["records"]:
            picks[r["pid"]] = {"decision": r["decision"], "released_level": r["released_level"]}
    out = []
    for p in PATIENTS.values():
        per = p["person"]
        out.append({"pid": p["pid"], "condition": p["condition"], "nationality": per["nationality"], "sex": per["sex"],
                    "age": per["age"], "small_group": per["nationality"] in SMALL_GROUPS,
                    "sensitive": p["sensitive_history"], "context": (p.get("vignette") or {}).get("context_dependence"),
                    **picks.get(p["pid"], {})})
    return out


@app.post("/api/sessions")
def start(req: StartReq):
    if req.pid not in PATIENTS:
        raise HTTPException(404, "unknown patient")
    s = Session(req.pid, req.start if req.start in LADDER else "L1")
    SESSIONS[s.id] = s
    threading.Thread(target=s.run, daemon=True).start()
    return {"id": s.id}


@app.get("/api/sessions/{sid}/events")
def events(sid: str, since: int = 0):
    s = SESSIONS.get(sid)
    if not s:
        raise HTTPException(404)

    def gen():
        i = since
        while True:
            with s.cond:
                while i >= len(s.events) and not s.done:
                    s.cond.wait(1.0)
                    if i >= len(s.events):
                        break
                batch = s.events[i:]
            for ev in batch:
                yield f"data: {json.dumps(ev, ensure_ascii=False)}\n\n"
            i += len(batch)
            if s.done and i >= len(s.events):
                yield "event: end\ndata: {}\n\n"
                return
            if not batch:
                yield ": keepalive\n\n"
    return StreamingResponse(gen(), media_type="text/event-stream",
                             headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


@app.post("/api/sessions/{sid}/action")
def action(sid: str, req: ActionReq):
    s = SESSIONS.get(sid)
    if not s:
        raise HTTPException(404)
    s.action = req.model_dump()
    s.action_ev.set()
    return {"ok": True}


@app.post("/api/sessions/{sid}/pause")
def pause(sid: str, paused: bool = True, step: bool = False):
    s = SESSIONS.get(sid)
    if not s:
        raise HTTPException(404)
    with s.cond:
        s.paused = paused
        if step:
            s.step_tokens += 1
        s.cond.notify_all()
    return {"paused": s.paused}


@app.get("/api/recordings")
def recordings():
    out = []
    for f in sorted(REC.glob("*.json"), reverse=True):
        try:
            d = json.loads(f.read_text())
            evs = d["events"]
            end = next((e["type"] for e in reversed(evs) if e["type"] in ("release", "block", "error")), "unfinished")
            out.append({"name": f.stem, "pid": d["pid"], "events": len(evs), "seconds": evs[-1]["t"] if evs else 0, "outcome": end})
        except Exception:
            continue
    return out


@app.get("/api/recordings/{name}")
def recording(name: str):
    f = REC / f"{Path(name).name}.json"
    if not f.exists():
        raise HTTPException(404)
    return JSONResponse(json.loads(f.read_text()))


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8341, log_level="warning")
