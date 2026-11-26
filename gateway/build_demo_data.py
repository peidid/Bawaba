"""Packs pipeline + Presidio results into demo/data.json for the demo page, and
writes demo/gateway_demo_offline.html (data inlined) as a no-network backup."""
import json
import sys
from collections import Counter
from pathlib import Path

from presidio_eval import gold_spans

ROOT = Path(__file__).parent
DEMO = ROOT / "demo"


def presidio_summary(patients, pres):
    by_pid = {p["pid"]: p for p in patients}
    qid_types, missed, over = Counter(), [], Counter()
    for pid, hits in pres["hits"]["base"].items():
        p = by_pid[pid]
        text = p["notes"]["L0"]
        tagged, pos = [], 0
        for s in p["segments"]:
            if s["tag"]:
                tagged.append((pos, pos + len(s["text"])))
            pos += len(s["text"])
        for tag, a, b, txt in gold_spans(p["segments"]):
            cov = [h for h in hits if h["start"] < b and h["end"] > a]
            if tag == "QID":
                qid_types.update(h["type"] for h in cov)
            if tag == "NAME" and not cov:
                missed.append({"name": txt, "nationality": p["person"]["nationality"], "sex": p["person"]["sex"]})
        for h in hits:
            if not any(h["start"] < b and h["end"] > a for a, b in tagged):
                over[(text[h["start"]:h["end"]], h["type"])] += 1
    return {
        "configs": [{"label": r["label"], "overall": r["overall"], "by_type": r["by_type"]} for r in pres["results"]],
        "qid_detected_as": dict(qid_types.most_common()),
        "missed_names": missed,
        "over_redaction_total": sum(over.values()),
        "over_redaction_examples": [{"text": t, "type": ty, "count": n} for (t, ty), n in over.most_common(14)],
        "n_notes": len(pres["hits"]["base"]),
    }


def main():
    name = sys.argv[1] if len(sys.argv) > 1 else "pipeline.json"
    src = ROOT / "results" / name
    pipe = json.loads(src.read_text())
    patients = json.loads((ROOT / "data/patients.json").read_text())
    pres = json.loads((ROOT / "results/presidio.json").read_text())
    by_pid = {p["pid"]: p for p in patients}

    recs = []
    for r in pipe["records"]:
        p = by_pid[r["pid"]]
        levels = {}
        for lv, L in r["levels"].items():
            atk = L.get("llm_attack") or None
            levels[lv] = {k: L[k] for k in ("ranked", "findings", "top1_correct", "top3_correct", "agrees_with_full_note",
                                             "k", "unique", "llm_reidentified", "privacy_pass", "utility_pass")}
            if atk:
                levels[lv]["attack"] = {"trace": atk.get("trace", []), "submission": atk.get("submission", {}),
                                        "refused": atk.get("refused", False)}
        recs.append({
            "pid": r["pid"], "condition": r["condition"], "nationality": r["nationality"], "sex": r["sex"], "age": r["age"],
            "name": p["person"]["name"], "small_group": r["small_group"], "sensitive_history": r["sensitive_history"],
            "decision": r["decision"], "released_level": r["released_level"], "memo": r.get("memo"),
            "attacked": r["attacked"], "segments": [{k: s[k] for k in ("text", "tag", "L1", "L2", "L3")} for s in r["segments"]],
            "levels": levels,
        })
    # attacked patients first, so the demo opens on a full red-team trace
    recs.sort(key=lambda x: (not x["attacked"], x["condition"], x["pid"]))

    data = {
        "generated": pipe["generated"], "model": pipe["model"], "k_threshold": pipe["k_threshold"],
        "registry_size": len(json.loads((ROOT / "data/registry.json").read_text())),
        "summary": pipe["summary"], "playbooks": pipe["playbooks"], "records": recs,
        "billing": pipe["billing"], "moph": pipe["moph"], "audit_log": pipe["audit_log"][:300],
        "presidio": presidio_summary(patients, pres), "source": src.name,
    }
    DEMO.mkdir(exist_ok=True)
    blob = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    (DEMO / "data.json").write_text(blob)
    html = (DEMO / "index.html").read_text()
    safe = blob.replace("</", "<\\/")
    body = html.replace("<!--INLINE_DATA-->", f'<script id="inline-data" type="application/json">{safe}</script>')
    offline = ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
               '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">'
               '<style>:root{color-scheme:light}body{margin:0}[hidden]{display:none!important}</style>'
               f'</head><body>{body}</body></html>')
    (DEMO / "gateway_demo_offline.html").write_text(offline)
    print(f"wrote demo/data.json ({len(blob) / 1024:.0f} KB) from {src.name}; offline copy written")


if __name__ == "__main__":
    main()
