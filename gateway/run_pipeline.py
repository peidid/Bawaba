"""Runs the three-channel privacy gateway on the synthetic patients and writes
results/pipeline.json (consumed by the demo page).

  python run_pipeline.py --smoke     # 2 patients, 1 attack: checks the wiring
  python run_pipeline.py             # full run (university OpenAI account)

Every LLM result is cached in results/cache.json, so a re-run only pays for
what is missing.
"""
import argparse
import hashlib
import json
import re
import threading
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).parent
RES = ROOT / "results"
RES.mkdir(exist_ok=True)
CACHE_PATH = RES / "cache_openai.json"
LEVELS = ["L0", "L1", "L2", "L3"]
K_THRESHOLD = 5            # k-anonymity floor for a release (proposal: k = 5)
SMALL_GROUPS = {"Kenyan", "British", "Sudanese", "Jordanian", "Sri Lankan", "Pakistani"}
SENSITIVE_KEYWORDS = {"HIV": ["hiv", "antiretroviral", "dolutegravir"], "depression": ["depress", "sertraline", "ssri"],
                      "hepatitis B": ["hepatitis b", "hbv", "hep b"], "epilepsy": ["epilep", "seizure", "levetiracetam"]}

_lock = threading.Lock()
cache = json.loads(CACHE_PATH.read_text()) if CACHE_PATH.exists() else {}


def cached(key, fn):
    with _lock:
        if key in cache:
            return cache[key]
    val = fn()
    with _lock:
        cache[key] = val
        CACHE_PATH.write_text(json.dumps(cache, ensure_ascii=False))
    return val


# ---------------------------------------------------------------- deterministic linkage
from policy import PRESETS, age_band, linkage_k as _linkage_k  # noqa: E402
from presidio_eval import gold_spans  # noqa: E402


def linkage_k(p, registry, lv):
    return _linkage_k(p["person"], registry, "L0" if lv == "L0" else PRESETS[lv], p.get("context_reveals"))


def h(text):
    return hashlib.md5(text.encode()).hexdigest()[:10]


# ---------------------------------------------------------------- E1: detection scoring (same rule for every arm)
NUM = re.compile(r"\d+(?:[.,/]\d+)*")


def score_release(p, released):
    """Direct-identifier recall (identifier no longer present) + share of clinical numbers kept."""
    found, total, by_type = 0, 0, Counter()
    tot_type = Counter()
    for tag, a, b, txt in gold_spans(p["segments"]):
        leaked = txt in released
        if tag in ("NAME", "RELATIVE", "CLINICIAN"):
            toks = [t for t in re.findall(r"[A-Za-z][A-Za-z'-]{2,}", txt) if t not in ("Dr", "mother", "father", "brother", "sister")]
            leaked = leaked or any(re.search(rf"\b{re.escape(t)}\b", released) for t in toks)
        if tag == "ADDRESS":
            leaked = leaked or any(m in released for m in re.findall(r"(?:Zone|Street|Building) \d+", txt))
        total += 1; tot_type[tag] += 1
        if not leaked:
            found += 1; by_type[tag] += 1
    clinical = "".join(s["text"] for s in p["segments"] if not s["tag"])
    nums = NUM.findall(clinical.split("HISTORY OF PRESENTING ILLNESS")[-1])
    kept = sum(1 for n in nums if n in released)
    return {"removed": found, "total": total, "by_type": {t: [by_type[t], tot_type[t]] for t in tot_type},
            "clinical_numbers": len(nums), "clinical_numbers_kept": kept}


def presidio_release(text, hits):
    out, last = [], 0
    for hh in sorted(hits, key=lambda x: x["start"]):
        if hh["start"] < last:
            continue
        out += [text[last:hh["start"]], f"[{hh['type']}]"]
        last = hh["end"]
    return "".join(out + [text[last:]])


# ---------------------------------------------------------------- channel payloads
def insurer_payloads(p):
    per = p["person"]
    claim = (f"CLAIM SUBMISSION\nMember: {per['name']}   QID: {per['qid']}   Policy: {p['insurance_policy']}\n"
             f"Date of service: {p['visit_date']}\nPrimary diagnosis (ICD-10): {p['icd10']} {p['condition']}\n"
             f"Services: {'; '.join(p['services'])}\nCharges: QAR {p['charges_qar']:,}")
    full = claim + "\n\nATTACHED CLINICAL NOTE (for medical-necessity review):\n" + p["notes"]["L0"]
    return {"full_note_attached": full, "minimised_claim": claim}


def mentions(text, condition):
    t = (text or "").lower()
    return any(k in t for k in SENSITIVE_KEYWORDS[condition])


def moph_tables(patients):
    """Weekly surveillance extract: counts by condition x municipality x age band, then
    the gateway's small-cell suppression; plus identified notifications only where the law
    requires them (TB, modelled as notifiable)."""
    raw = Counter((p["condition"], p["person"]["municipality"], age_band(p["person"]["age"])) for p in patients)
    granular = [{"condition": c, "municipality": m, "age_band": a, "count": n} for (c, m, a), n in sorted(raw.items())]
    small = sum(1 for r in granular if r["count"] < K_THRESHOLD)
    coarse = Counter((p["condition"], p["person"]["municipality"]) for p in patients)
    coarse_rows = [{"condition": c, "municipality": m, "count": n if n >= K_THRESHOLD else "<5"} for (c, m), n in sorted(coarse.items())]
    by_cond = Counter(p["condition"] for p in patients)
    national = [{"condition": c, "count": n if n >= K_THRESHOLD else "<5"} for c, n in sorted(by_cond.items())]
    notifiable = [{"pid": p["pid"], "name": p["person"]["name"], "qid": p["person"]["qid"], "condition": p["condition"],
                   "municipality": p["person"]["municipality"], "legal_basis": "notifiable communicable disease"}
                  for p in patients if p["condition"] == "Pulmonary tuberculosis"]
    return {"granular": granular, "granular_small_cells": small, "granular_cells": len(granular),
            "coarse": coarse_rows, "coarse_suppressed": sum(1 for r in coarse_rows if r["count"] == "<5"),
            "national": national, "notifiable_identified": notifiable}


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--attack-per-condition", type=int, default=3)
    ap.add_argument("--no-llm", action="store_true", help="deterministic parts only (for testing the demo page)")
    args = ap.parse_args()
    global cached
    if args.no_llm:                       # every agent result comes back empty; nothing is cached
        cached = lambda key, fn: {}

    import agents  # imported late so --help works without a key

    patients = json.loads((ROOT / "data/patients.json").read_text())
    registry = json.loads((ROOT / "data/registry.json").read_text())
    if args.smoke:
        patients = [patients[0], patients[25]]

    # attack subset: first N patients of each condition, plus every small-group patient
    per_cond = defaultdict(list)
    for p in patients:
        per_cond[p["condition"]].append(p["pid"])
    n_attack = 1 if args.smoke else args.attack_per_condition
    attack_ids = {pid for ids in per_cond.values() for pid in ids[:n_attack]}
    if not args.smoke:
        attack_ids |= {p["pid"] for p in patients if p["person"]["nationality"] in SMALL_GROUPS}
    attack_levels = ["L1"] if args.smoke else ["L1", "L2", "L3"]

    # 1) red-team strategist: one playbook per release level
    print("strategist: writing playbooks ...", flush=True)
    playbooks = {}
    for lv in attack_levels:
        samples = [p["notes"][lv] for p in patients[::max(1, len(patients) // 3)][:3]]
        playbooks[lv] = cached(f"playbook|{lv}|{len(samples)}", lambda lv=lv, s=samples: agents.write_playbook(lv, s))

    # 2) utility tests (all patients x all levels) and attacks (subset), concurrently
    jobs = []
    for p in patients:
        jobs.append(("minimize", p, "L0"))
        for lv in LEVELS:
            jobs.append(("diag", p, lv))
        if p["pid"] in attack_ids:
            for lv in attack_levels:
                jobs.append(("attack", p, lv))
    print(f"running {len(jobs)} agent jobs with {args.workers} workers ...", flush=True)

    def run(job):
        kind, p, lv = job
        note = p["notes"][lv]
        if kind == "diag":
            return job, cached(f"diag|{h(note)}", lambda: agents.diagnose(note))
        if kind == "minimize":
            return job, cached(f"minimize|{h(note)}", lambda: agents.minimize_note(note))
        return job, cached(f"attack|{h(note)}|{lv}", lambda: agents.attack(note, registry, playbooks[lv]))

    out = defaultdict(dict)
    done = 0
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = [ex.submit(run, j) for j in jobs]
        for f in as_completed(futs):
            (kind, p, lv), val = f.result()
            out[(p["pid"], kind)][lv] = val
            done += 1
            if done % 25 == 0 or done == len(jobs):
                print(f"  {done}/{len(jobs)}", flush=True)

    # 3) billing channel: profile claims for patients with a sensitive history
    sens = [p for p in patients if p["sensitive_history"]]
    if args.smoke:
        sens = sens[:1]
    print(f"insurer profiler on {len(sens)} members x 2 payloads ...", flush=True)
    billing = []
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {}
        for p in sens:
            for kind, payload in insurer_payloads(p).items():
                futs[ex.submit(cached, f"profile|{h(payload)}", lambda pl=payload: agents.profile_claim(pl))] = (p, kind, payload)
        rows = defaultdict(dict)
        for f in as_completed(futs):
            p, kind, payload = futs[f]
            res = f.result()
            inf = res.get("inference") or {}
            text = " ".join(inf.get("inferred_conditions", []) + inf.get("underwriting_flags", []))
            rows[p["pid"]][kind] = {"payload": payload, "inference": inf, "refused": res.get("refused"),
                                    "sensitive_disclosed_in_payload": mentions(payload, p["sensitive_history"]),
                                    "insurer_inferred_sensitive": mentions(text, p["sensitive_history"])}
        for p in sens:
            billing.append({"pid": p["pid"], "sensitive_history": p["sensitive_history"], "condition": p["condition"], **rows[p["pid"]]})

    # 4) assemble AI-channel records + oversight decisions
    records, audit = [], []
    for p in patients:
        diag = out[(p["pid"], "diag")]
        atk = out.get((p["pid"], "attack"), {})
        top_l0 = (diag.get("L0", {}).get("ranked") or [None])[0]
        levels = {}
        for lv in LEVELS:
            d = diag.get(lv, {})
            ranked = d.get("ranked") or []
            a = atk.get(lv)
            llm_success = None
            if a is not None:
                llm_success = (a.get("submission") or {}).get("pid") == p["pid"]
            k = linkage_k(p, registry, lv)
            levels[lv] = {
                "note": p["notes"][lv], "ranked": ranked, "findings": d.get("findings", ""),
                "top1_correct": bool(ranked) and ranked[0] == p["condition"],
                "top3_correct": p["condition"] in ranked,
                "agrees_with_full_note": bool(ranked) and ranked[0] == top_l0,
                "k": k, "unique": k == 1,
                "llm_attack": a, "llm_reidentified": llm_success,
                "privacy_pass": k >= K_THRESHOLD and not llm_success,
                "utility_pass": bool(ranked) and ranked[0] == top_l0,
            }
        # oversight: least-restrictive level that is both safe and useful
        decision, chosen = None, None
        for lv in ["L1", "L2", "L3"]:
            if levels[lv]["privacy_pass"] and levels[lv]["utility_pass"]:
                chosen = lv
                decision = "RELEASE" if lv == "L1" else "TIGHTEN_AND_RELEASE"
                break
        if not chosen:
            safe = [lv for lv in ["L1", "L2", "L3"] if levels[lv]["privacy_pass"]]
            decision = "ESCALATE" if safe else "BLOCK_KEEP_LOCAL"
        review = [r for r, on in (("escalated", decision == "ESCALATE"),
                                  ("sensitive history", bool(p["sensitive_history"])),
                                  ("small nationality group", p["person"]["nationality"] in SMALL_GROUPS)) if on]
        rec = {"pid": p["pid"], "condition": p["condition"], "nationality": p["person"]["nationality"],
               "context_dependence": (p.get("vignette") or {}).get("context_dependence"),
               "context_reveals": p.get("context_reveals"), "human_review": review,
               "small_group": p["person"]["nationality"] in SMALL_GROUPS, "sex": p["person"]["sex"], "age": p["person"]["age"],
               "sensitive_history": p["sensitive_history"], "segments": p["segments"], "levels": levels,
               "decision": decision, "released_level": chosen, "attacked": p["pid"] in attack_ids}
        records.append(rec)
        audit.append({"ts": datetime.now(timezone.utc).isoformat(timespec="seconds"), "channel": "ai_diagnosis",
                      "record": p["pid"], "decision": decision, "released_level": chosen,
                      "tests": {lv: {"k": levels[lv]["k"], "llm_reid": levels[lv]["llm_reidentified"],
                                     "agrees": levels[lv]["agrees_with_full_note"]} for lv in ["L1", "L2", "L3"]}})

    # escalation memos (a handful)
    esc = [r for r in records if r["decision"] == "ESCALATE"][: (1 if args.smoke else 6)]
    for r in esc:
        case = {"channel": "external AI diagnostic tool", "condition_truth_hidden_from_tool": r["condition"],
                "tests": {lv: {"directory_candidates_k": r["levels"][lv]["k"],
                               "red_team_reidentified": r["levels"][lv]["llm_reidentified"],
                               "tool_top_diagnosis": (r["levels"][lv]["ranked"] or [None])[0],
                               "matches_full_note_answer": r["levels"][lv]["agrees_with_full_note"]} for lv in LEVELS}}
        r["memo"] = cached(f"memo|{h(json.dumps(case))}", lambda c=case: agents.escalation_memo(c)).get("memo")

    for b in billing:
        audit.append({"ts": datetime.now(timezone.utc).isoformat(timespec="seconds"), "channel": "insurer_billing",
                      "record": b["pid"], "decision": "RELEASE minimised claim; BLOCK attached note",
                      "tests": {"full_note_inferred_sensitive": b.get("full_note_attached", {}).get("insurer_inferred_sensitive"),
                                "minimised_inferred_sensitive": b.get("minimised_claim", {}).get("insurer_inferred_sensitive")}})
    moph = moph_tables(patients)
    for n in moph["notifiable_identified"]:
        audit.append({"ts": datetime.now(timezone.utc).isoformat(timespec="seconds"), "channel": "moph_reporting",
                      "record": n["pid"], "decision": "RELEASE identified (legal basis: notifiable disease)"})

    # 5) summary
    summary = {"levels": {}, "groups": {}}
    for lv in LEVELS:
        L = [r["levels"][lv] for r in records]
        A = [x for x in L if x["llm_reidentified"] is not None]
        summary["levels"][lv] = {
            "n": len(L), "top1": round(sum(x["top1_correct"] for x in L) / len(L), 3),
            "top3": round(sum(x["top3_correct"] for x in L) / len(L), 3),
            "agree": round(sum(x["agrees_with_full_note"] for x in L) / len(L), 3),
            "unique_rate": round(sum(x["unique"] for x in L) / len(L), 3),
            "k_lt5_rate": round(sum(x["k"] < K_THRESHOLD for x in L) / len(L), 3),
            "median_k": sorted(x["k"] for x in L)[len(L) // 2],
            "llm_attacks": len(A), "llm_reid_rate": round(sum(bool(x["llm_reidentified"]) for x in A) / len(A), 3) if A else None,
        }
    for grp, test in (("small groups", True), ("large groups", False)):
        R = [r for r in records if r["small_group"] == test]
        summary["groups"][grp] = {lv: {"n": len(R), "unique_rate": round(sum(r["levels"][lv]["unique"] for r in R) / max(1, len(R)), 3),
                                       "top1": round(sum(r["levels"][lv]["top1_correct"] for r in R) / max(1, len(R)), 3)} for lv in LEVELS}
    summary["decisions"] = dict(Counter(r["decision"] for r in records))
    summary["human_review_rate"] = round(sum(bool(r["human_review"]) for r in records) / len(records), 3)
    summary["human_review_reasons"] = dict(Counter(x for r in records for x in r["human_review"]))
    summary["by_context_dependence"] = {}
    for dep in ("high", "medium", "low"):
        R = [r for r in records if r["context_dependence"] == dep]
        if R:
            summary["by_context_dependence"][dep] = {lv: {"n": len(R), "top1": round(sum(r["levels"][lv]["top1_correct"] for r in R) / len(R), 3),
                                                          "agree": round(sum(r["levels"][lv]["agrees_with_full_note"] for r in R) / len(R), 3)} for lv in LEVELS}
    # E1: detection arms scored with one rule
    pres_path = ROOT / "results/presidio.json"
    pres = json.loads(pres_path.read_text()) if pres_path.exists() else None
    arms = defaultdict(list)
    for p in patients:
        m = out[(p["pid"], "minimize")].get("L0") or {}
        if m.get("release_text"):
            arms[f"LLM minimizer ({agents.INHOUSE})"].append(score_release(p, m["release_text"]))
        if pres:
            for cfg, label in (("base", "Presidio (out of the box)"), ("custom", "Presidio + Qatar recognizers")):
                hits = pres["hits"][cfg].get(p["pid"])
                if hits is not None:
                    arms[label].append(score_release(p, presidio_release(p["notes"]["L0"], hits)))
    e1 = {}
    for label, rows in arms.items():
        types = Counter(); tots = Counter()
        for r in rows:
            for t, (f_, n_) in r["by_type"].items():
                types[t] += f_; tots[t] += n_
        e1[label] = {"notes": len(rows), "recall": round(sum(r["removed"] for r in rows) / max(1, sum(r["total"] for r in rows)), 3),
                     "clinical_numbers_kept": round(sum(r["clinical_numbers_kept"] for r in rows) / max(1, sum(r["clinical_numbers"] for r in rows)), 3),
                     "by_type": {t: round(types[t] / tots[t], 3) for t in tots}}
    summary["e1_detection"] = e1
    summary["billing"] = {
        "members": len(billing),
        "full_note_sensitive_inferred": sum(bool(b.get("full_note_attached", {}).get("insurer_inferred_sensitive")) for b in billing),
        "minimised_sensitive_inferred": sum(bool(b.get("minimised_claim", {}).get("insurer_inferred_sensitive")) for b in billing),
    }
    summary["by_condition"] = {c: {lv: round(sum(r["levels"][lv]["top1_correct"] for r in records if r["condition"] == c) /
                                         max(1, sum(1 for r in records if r["condition"] == c)), 3) for lv in LEVELS}
                               for c in agents.TARGET_CONDITIONS}
    tok = defaultdict(Counter)
    for v in cache.values():
        u = v.get("usage") if isinstance(v, dict) else None
        if isinstance(u, dict):
            tok[u.get("model", "?")]["in"] += u.get("in", 0)
            tok[u.get("model", "?")]["out"] += u.get("out", 0)
    summary["tokens"] = {m: dict(c) for m, c in tok.items()}

    result = {"generated": datetime.now(timezone.utc).isoformat(timespec="seconds"), "model": f"{agents.OUTSIDER} (outsider roles) / {agents.INHOUSE} (in-house roles)",
              "k_threshold": K_THRESHOLD, "summary": summary, "playbooks": playbooks, "records": records,
              "billing": billing, "moph": moph, "audit_log": audit}
    name = "pipeline_nollm.json" if args.no_llm else "pipeline_smoke.json" if args.smoke else "pipeline.json"
    (RES / name).write_text(json.dumps(result, indent=1, ensure_ascii=False))
    with open(RES / ("audit_log_nollm.jsonl" if args.no_llm else "audit_log.jsonl"), "w") as fh:
        for a in audit:
            fh.write(json.dumps(a, ensure_ascii=False) + "\n")
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
