"""E7: agentic oversight vs the fixed ladder, on all 120 synthetic patients (certification setting).

For every patient the gateway starts from the certified policy (L1). After each draft is tested
(utility: the outside AI tool's diagnosis vs the full note; privacy: k against the 2,000-person
directory, plus the LLM red team for the same attack subset as E2), the oversight agent decides.
The baseline is the fixed ladder of E5 (L1 -> L2 -> L3, first level that passes both tests).

    python e7_agentic_oversight.py --limit 3      # smoke test
    python e7_agentic_oversight.py                # all 120 (resumable: finished patients are kept)

Writes results/e7_agentic_oversight.json. Agent rule-change proposals go to results/e7_amendments.jsonl.
"""
import argparse
import hashlib
import json
import threading
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import agents
import oversight_agent as OA
import rag
from policy import FIELDS, PRESETS, linkage_k, preset_name, render

ROOT = Path(__file__).parent
RES = ROOT / "results"
OUT = RES / "e7_agentic_oversight.json"
CACHE_W = RES / "cache_e7.json"
SMALL_GROUPS = {"Kenyan", "British", "Sudanese", "Jordanian", "Sri Lankan", "Pakistani"}
OA.AMENDMENTS = RES / "e7_amendments.jsonl"

_lock = threading.Lock()
cache = {}
for f in (RES / "cache_openai.json", RES / "cache_live.json", CACHE_W):
    if f.exists():
        cache.update(json.loads(f.read_text()))
own = json.loads(CACHE_W.read_text()) if CACHE_W.exists() else {}


def h(text):
    return hashlib.md5(text.encode()).hexdigest()[:10]


def cached(key, fn):
    with _lock:
        if key in cache:
            return cache[key]
    val = fn()
    with _lock:
        cache[key] = own[key] = val
        CACHE_W.write_text(json.dumps(own, ensure_ascii=False))
    return val


def nearest_preset(policy):
    name = preset_name(policy)
    if name != "custom":
        return name
    return "L2" if any(policy[f] in ("exact", "keep") for f in FIELDS) else "L3"


def run_patient(p, rec, registry, playbooks, lib, max_drafts):
    per = p["person"]
    full_top3 = rec["levels"]["L0"]["ranked"]
    case = OA.Case(p["pid"], per, registry, p.get("context_reveals"), per["nationality"] in SMALL_GROUPS,
                   p["sensitive_history"], lib.profile("ai_diagnosis"))
    policy, source, log = dict(PRESETS["L1"]), "certified policy", []
    usage = Counter()
    for version in range(1, max_drafts + 2):
        note = render(p["segments"], policy)
        d = cached(f"diag|{h(note)}", lambda: agents.diagnose(note))
        ranked = d.get("ranked") or []
        util = bool(ranked) and bool(full_top3) and ranked[0] == full_top3[0]
        k = linkage_k(per, registry, policy, p.get("context_reveals"))
        ident = cand = reason = None
        searches = 0
        if rec["attacked"]:
            lv = nearest_preset(policy)
            tag = preset_name(policy) if preset_name(policy) != "custom" else "custom"
            a = cached(f"attack|{h(note)}|{tag}", lambda: agents.attack(note, registry, playbooks[lv]))
            sub = a.get("submission") or {}
            ident, cand, reason, searches = sub.get("pid") == p["pid"], sub.get("candidates_remaining"), sub.get("reasoning"), len(a.get("trace", []))
        case.rounds.append(OA.round_entry(version, policy, k, ident, cand, reason, searches, util, ranked, full_top3,
                                          d.get("findings", ""), source, note))
        res = OA.decide(case, lib)
        for m in ("in", "out", "calls"):
            usage[m] += res["usage"][m]
        log.append({"version": version, "policy": dict(policy), "k": k, "identified": ident, "utility_ok": util,
                    "top1_correct": bool(ranked) and ranked[0] == p["condition"], "decision": res["decision"],
                    "next_policy": res["policy"], "reason": res["reason"], "cited_rules": res["cited_rules"],
                    "message": res["message"], "refusals": res["refusals"], "fallback": res.get("fallback", False),
                    "tools": Counter(s["tool"] for s in res["steps"])})
        if res["decision"] == "REDRAFT":
            policy, source = res["policy"], "oversight"
            continue
        break
    last = log[-1]
    passes = last["k"] >= case.params()["k_min"] and not last["identified"] and last["utility_ok"]
    outcome = {"RELEASE": "release",
               "ASK_HUMAN": "release after review" if passes else "human decides (tests not passed)",
               "ESCALATE": "escalate", "BLOCK": "block", "REDRAFT": "draft limit"}[last["decision"]]
    final = last["policy"]
    return {"pid": p["pid"], "condition": p["condition"], "nationality": per["nationality"],
            "small_group": case.small_group, "sensitive_history": p["sensitive_history"],
            "context_dependence": (p.get("vignette") or {}).get("context_dependence"), "attacked": rec["attacked"],
            "outcome": outcome, "final_policy": final, "final_preset": preset_name(final), "final_k": last["k"],
            "final_identified": last["identified"], "final_utility": last["utility_ok"],
            "final_top1_correct": last["top1_correct"], "detail_score": OA.detail_score(final),
            "context_kept": final["context"] != "remove", "drafts": len(log), "rounds": log, "k_min": case.params()["k_min"],
            "amendments": case.amendments, "tightened": case.tightened,
            "usage": dict(usage), "model": OA.OVERSIGHT_MODEL}


def ladder_row(rec):
    lv = rec["released_level"]
    pol = PRESETS[lv] if lv else None
    L = rec["levels"].get(lv) if lv else None
    return {"outcome": "release" if lv else rec["decision"].lower(), "preset": lv,
            "detail_score": OA.detail_score(pol) if pol else None, "context_kept": bool(pol) and pol["context"] != "remove",
            "k": L["k"] if L else None, "utility": L["agrees_with_full_note"] if L else None,
            "top1_correct": L["top1_correct"] if L else None,
            "drafts": ["L1", "L2", "L3"].index(lv) + 1 if lv else 3}


def summarize(rows, recs):
    n = len(rows)
    mean = lambda xs: round(sum(xs) / len(xs), 3) if xs else None
    for r in rows:   # recomputed from the stored policy (keeps old rows consistent with the scorer)
        r["detail_score"] = OA.detail_score(r["final_policy"])
    released = [r for r in rows if r["outcome"] in ("release", "release after review")]
    lad = {r["pid"]: ladder_row(recs[r["pid"]]) for r in rows}
    lad_rel = [lad[r["pid"]] for r in rows if lad[r["pid"]]["preset"]]
    hi = [r for r in rows if r["context_dependence"] == "high"]
    return {
        "patients": n, "model": OA.OVERSIGHT_MODEL,
        "agent": {
            "outcomes": dict(Counter(r["outcome"] for r in rows)),
            "released": len(released),
            "final_presets": dict(Counter(r["final_preset"] for r in released)),
            "privacy_pass_released": mean([r["final_k"] >= r.get("k_min", 5) and not r["final_identified"] for r in released]),
            "final_k_median": sorted(r["final_k"] for r in released)[len(released) // 2] if released else None,
            "utility_agree_released": mean([r["final_utility"] for r in released]),
            "top1_correct_released": mean([r["final_top1_correct"] for r in released]),
            "detail_score_mean": mean([r["detail_score"] for r in released]),
            "context_kept_rate": mean([r["context_kept"] for r in released]),
            "context_kept_rate_high_context": mean([r["context_kept"] for r in hi if r in released]),
            "drafts_mean": mean([r["drafts"] for r in rows]),
            "verifier_refusals": sum(len(x["refusals"]) for r in rows for x in r["rounds"]),
            "fallbacks": sum(x["fallback"] for r in rows for x in r["rounds"]),
            "amendments": sum(len(r["amendments"]) for r in rows),
            "amendments_by_param": dict(Counter(f"{a['rule_id']} {a['param']} → {a['new_value']} ({a['direction']})" for r in rows for a in r["amendments"])),
            "tokens": {"in": sum(r["usage"].get("in", 0) for r in rows), "out": sum(r["usage"].get("out", 0) for r in rows),
                       "calls": sum(r["usage"].get("calls", 0) for r in rows)},
        },
        "ladder": {
            "outcomes": dict(Counter(lad[r["pid"]]["outcome"] for r in rows)),
            "released": len(lad_rel),
            "final_presets": dict(Counter(x["preset"] for x in lad_rel)),
            "utility_agree_released": mean([x["utility"] for x in lad_rel]),
            "top1_correct_released": mean([x["top1_correct"] for x in lad_rel]),
            "detail_score_mean": mean([x["detail_score"] for x in lad_rel]),
            "context_kept_rate": mean([x["context_kept"] for x in lad_rel]),
            "context_kept_rate_high_context": mean([lad[r["pid"]]["context_kept"] for r in hi if lad[r["pid"]]["preset"]]),
            "drafts_mean": mean([x["drafts"] for x in lad.values()]),
        },
        "both_released": sum(1 for r in released if lad[r["pid"]]["preset"]),
        "agent_more_detail": sum(1 for r in released if lad[r["pid"]]["preset"] and r["detail_score"] > lad[r["pid"]]["detail_score"]),
        "agent_less_detail": sum(1 for r in released if lad[r["pid"]]["preset"] and r["detail_score"] < lad[r["pid"]]["detail_score"]),
    }


def policy_variant(edits):
    """E8: copy the policy library and change Param lines in the copy ("k_min=10,cell_min=11"): the gateway's
    behaviour must follow the edited documents with no code change."""
    import re
    import shutil
    tmp = RES / "policy_variant"
    shutil.rmtree(tmp, ignore_errors=True)
    shutil.copytree(ROOT / "policies", tmp, ignore=shutil.ignore_patterns("*.jsonl"))
    for item in edits.split(","):
        param, val = [x.strip() for x in item.split("=")]
        for f in tmp.glob("*.md"):
            text = f.read_text()
            new = re.sub(rf"^Param: {re.escape(param)} = .*$", f"Param: {param} = {val}", text, flags=re.M)
            if new != text:
                f.write_text(new.replace("version: ", f"version: variant({param}={val}) of ", 1))
                print(f"policy variant: {f.name}: {param} = {val}", flush=True)
    return rag.Library(policy_dir=tmp)


def main():
    global OUT
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--pids", default="")
    ap.add_argument("--group", default="", choices=["", "small_group"])
    ap.add_argument("--set", default="", help="E8: edit Param lines in a copy of the policy library, e.g. k_min=10")
    ap.add_argument("--out", default="")
    args = ap.parse_args()
    if args.out:
        OUT = RES / args.out
        OA.AMENDMENTS = RES / (Path(args.out).stem + "_amendments.jsonl")
    patients = json.loads((ROOT / "data/patients.json").read_text())
    registry = json.loads((ROOT / "data/registry.json").read_text())
    recs = {r["pid"]: r for r in json.loads((ROOT / "results/pipeline.json").read_text())["records"]}
    playbooks = {lv: cache[f"playbook|{lv}|3"] for lv in ("L1", "L2", "L3")}
    lib = policy_variant(args.set) if args.set else rag.Library()
    if args.pids:
        patients = [p for p in patients if p["pid"] in args.pids.split(",")]
    if args.group == "small_group":
        patients = [p for p in patients if p["person"]["nationality"] in SMALL_GROUPS]
    if args.limit:
        patients = patients[:args.limit]
    done = {r["pid"]: r for r in json.loads(OUT.read_text())["records"]} if OUT.exists() else {}
    todo = [p for p in patients if p["pid"] not in done]
    print(f"E7: {len(todo)} patients to run ({len(done)} already done), oversight model {OA.OVERSIGHT_MODEL}", flush=True)
    t0 = time.time()

    def save():
        rows = [done[p["pid"]] for p in patients if p["pid"] in done]
        OUT.write_text(json.dumps({"generated": time.strftime("%Y-%m-%d %H:%M"), "summary": summarize(rows, recs),
                                   "records": list(done.values())}, ensure_ascii=False, indent=1, default=lambda o: dict(o)))

    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(run_patient, p, recs[p["pid"]], registry, playbooks, lib, 6): p for p in todo}
        for i, f in enumerate(as_completed(futs), 1):
            p = futs[f]
            try:
                r = f.result()
            except Exception as e:
                print(f"  {p['pid']} ERROR {type(e).__name__}: {e}", flush=True)
                continue
            with _lock:
                done[r["pid"]] = r
                save()
            print(f"  [{i}/{len(todo)}] {r['pid']} {r['condition']:<28} {r['outcome']:<22} {r['final_preset']:<6} k={r['final_k']:<4} "
                  f"detail={r['detail_score']} drafts={r['drafts']} ({time.time() - t0:.0f}s)", flush=True)
    save()
    print(json.dumps(json.loads(OUT.read_text())["summary"], indent=1))


if __name__ == "__main__":
    main()
