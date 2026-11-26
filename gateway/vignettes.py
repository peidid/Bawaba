"""Generates varied clinical vignettes per condition with the OUTSIDER model and
validates them. Output: data/vignettes.json (used by gen_data.py)."""
import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import agents as A

OUT = Path(__file__).parent / "data" / "vignettes.json"
N = int(sys.argv[1]) if len(sys.argv) > 1 else 10

ELIGIBILITY = {
    "Heat stroke": "adults aged 20-58 doing outdoor manual work in Qatar",
    "Pre-eclampsia": "pregnant women aged 20-40 living in Qatar",
    "Ectopic pregnancy": "women aged 19-40 living in Qatar",
    "Kawasaki disease": "children aged 1-4 living in Qatar (context may only use {country}/{month}; no occupation)",
    "Bronchiolitis": "infants under 1 year living in Qatar (context may only use {country}/{month}; no occupation)",
    "Asthma exacerbation": "people aged 6-40 living in Qatar",
    "Acute myocardial infarction": "adults aged 42 and over living in Qatar",
    "Pulmonary tuberculosis": "expatriate workers aged 20-55 who moved to Qatar from their home country",
    "Diabetic ketoacidosis": "people aged 8-30 living in Qatar",
    "Acute appendicitis": "people aged 8-40 living in Qatar",
    "Gout": "men aged 35 and over living in Qatar",
    "Benign prostatic hyperplasia": "men aged 55 and over living in Qatar",
}
PLACEHOLDER_NOTE = (" Placeholder meanings: everyone lives and works in Qatar. {occupation}/{employer} = the patient's "
                    "job and employer in Qatar; {country} = the patient's HOME country (only for travel, arrival or "
                    "family-visit context, never as the place of work); {month} = the month of the visit. "
                    "Generalized: {occupation_category}, {region} = world region of the home country, {season} = "
                    "'summer' or 'winter'.")
KEEP_OK = {"occupation", "employer", "country", "month"}
GEN_OK = {"occupation_category", "region", "season"}
BANNED = re.compile(r"\b(he|she|his|her|man|woman|boy|girl|male|female|year-old)\b", re.I)


def clean(cond, v):
    issues = []
    keep = set(re.findall(r"\{(\w+)\}", v["context_keep"]))
    gen = set(re.findall(r"\{(\w+)\}", v["context_generalized"]))
    if keep - KEEP_OK or gen - GEN_OK:
        issues.append(f"bad placeholders {keep - KEEP_OK} {gen - GEN_OK}")
    if cond.lower() in v["presentation"].lower():
        issues.append("names the diagnosis")
    if re.search(r"\{\w+\}", v["presentation"]):
        issues.append("placeholder in presentation")
    if cond in ("Kawasaki disease", "Bronchiolitis") and keep & {"occupation", "employer"}:
        issues.append("occupation for a child")
    # strip stray sex words from the presentation, which comes after the record's own sex word
    v["presentation"] = BANNED.sub(lambda m: {"he": "the patient", "she": "the patient", "his": "their",
                                              "her": "their"}.get(m.group(0).lower(), m.group(0)), v["presentation"])
    return issues


def one(cond):
    r = A.write_vignettes(cond, N, ELIGIBILITY[cond] + PLACEHOLDER_NOTE)
    good, dropped = [], []
    for v in r["vignettes"]:
        iss = clean(cond, v)
        (dropped if iss else good).append({**v, "issues": iss})
    return cond, good, dropped, r["usage"]


def main():
    with ThreadPoolExecutor(6) as ex:
        res = list(ex.map(one, A.TARGET_CONDITIONS))
    out, tok = {}, {"in": 0, "out": 0}
    for cond, good, dropped, u in res:
        out[cond] = good
        tok["in"] += u["in"]; tok["out"] += u["out"]
        print(f"{cond:30s} kept {len(good):2d} dropped {len(dropped)} "
              f"high-context {sum(v['context_dependence'] == 'high' for v in good)} "
              + ("; ".join(d["issues"][0] for d in dropped)[:120]))
    OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False))
    print("tokens", tok, "->", OUT)


if __name__ == "__main__":
    main()
