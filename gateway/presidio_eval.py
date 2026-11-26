"""How much of the direct-identifier layer does Microsoft Presidio catch on
Qatar-style notes - out of the box, and with Qatar-specific recognizers added?

Gold spans come from the tagged segments in data/patients.json, so recall is
exact. Also records "over-redaction": Presidio hits on clinical text that is not
an identifier (these destroy utility, e.g. eponymous disease names).
"""
import json
from collections import defaultdict
from pathlib import Path

from presidio_analyzer import AnalyzerEngine, Pattern, PatternRecognizer

ROOT = Path(__file__).parent
DIRECT = {"NAME", "QID", "MRN", "DOB", "ADDRESS", "PHONE", "RELATIVE", "CLINICIAN", "DATE"}


def qatar_recognizers():
    return [
        PatternRecognizer(supported_entity="QA_QID", patterns=[Pattern("qid", r"\b[23]\d{10}\b", 0.8)], context=["QID"]),
        PatternRecognizer(supported_entity="QA_PHONE", patterns=[Pattern("phone", r"\+974\s?[3-7]\d{3}\s?\d{4}", 0.9)]),
        PatternRecognizer(supported_entity="QA_ADDRESS", patterns=[Pattern("addr", r"Zone \d{1,2}, Street \d{1,4}, Building \d{1,4}(, [A-Z][a-z]+( [A-Z][a-z]+)?)?", 0.9)]),
        PatternRecognizer(supported_entity="MRN", patterns=[Pattern("mrn", r"(?<=MRN: )\d{7}", 0.9)]),
    ]


def gold_spans(segments):
    spans, pos = [], 0
    for s in segments:
        n = len(s["text"])
        if s["tag"] in DIRECT:
            start, end = pos, pos + n
            if s["tag"] == "RELATIVE":            # only the name part is PHI
                rel = s["text"].split(" ", 1)
                start = pos + len(rel[0]) + 1
            spans.append((s["tag"], start, end, s["text"]))
        pos += n
    return spans


def coverage(span, hits):
    _, a, b, _ = span
    covered = set()
    for h in hits:
        covered.update(range(max(a, h.start), min(b, h.end)))
    return len(covered) / max(1, b - a)


def evaluate(analyzer, patients, label):
    found, total = defaultdict(int), defaultdict(int)
    over, examples = defaultdict(int), {}
    for p in patients:
        text = p["notes"]["L0"]
        hits = analyzer.analyze(text=text, language="en")
        gold = gold_spans(p["segments"])
        for g in gold:
            total[g[0]] += 1
            if coverage(g, hits) >= 0.5:
                found[g[0]] += 1
        # hits that overlap no gold span and no structural header = over-redaction
        for h in hits:
            if not any(h.start < g[2] and h.end > g[1] for g in gold):
                frag = text[h.start:h.end]
                if frag.strip() and frag not in ("Male", "Female"):
                    over[f"{frag} -> {h.entity_type}"] += 1
        examples[p["pid"]] = [{"start": h.start, "end": h.end, "type": h.entity_type, "score": round(h.score, 2)} for h in hits]
    recall = {t: {"found": found[t], "total": total[t], "recall": round(found[t] / total[t], 3)} for t in sorted(total)}
    all_f, all_t = sum(found.values()), sum(total.values())
    print(f"\n== {label}: overall recall {all_f}/{all_t} = {all_f / all_t:.1%}")
    for t, r in recall.items():
        print(f"  {t:10s} {r['found']:3d}/{r['total']:3d}  {r['recall']:.0%}")
    top_over = sorted(over.items(), key=lambda kv: -kv[1])[:15]
    print("  over-redaction (clinical text flagged):", top_over[:8])
    return {"label": label, "overall": round(all_f / all_t, 3), "by_type": recall,
            "over_redaction": [{"text": k, "count": v} for k, v in top_over]}, examples


def main():
    patients = json.loads((ROOT / "data/patients.json").read_text())
    base = AnalyzerEngine()
    res_base, ex_base = evaluate(base, patients, "Presidio (out of the box)")
    custom = AnalyzerEngine()
    for r in qatar_recognizers():
        custom.registry.add_recognizer(r)
    res_custom, ex_custom = evaluate(custom, patients, "Presidio + Qatar recognizers")
    out = {"results": [res_base, res_custom],
           "hits": {"base": ex_base, "custom": ex_custom}}
    (ROOT / "results").mkdir(exist_ok=True)
    (ROOT / "results/presidio.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
