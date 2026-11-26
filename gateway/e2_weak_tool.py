"""E2b: does the utility cost of minimization depend on the strength of the external tool?
Runs the in-house-size model (gpt-5.4-nano) as the diagnostic tool on L0-L3 for every patient."""
import json
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import agents
from run_pipeline import cached, h

ROOT = Path(__file__).parent
patients = json.loads((ROOT / "data/patients.json").read_text())
jobs = [(p, lv) for p in patients for lv in ("L0", "L1", "L2", "L3")]


def run(job):
    p, lv = job
    note = p["notes"][lv]
    return job, cached(f"diagnano|{h(note)}", lambda: agents.diagnose(note, model=agents.INHOUSE))


res = defaultdict(dict)
with ThreadPoolExecutor(12) as ex:
    for (p, lv), v in ex.map(run, jobs):
        res[p["pid"]][lv] = v
out = {"levels": {}, "by_context_dependence": {}}
for lv in ("L0", "L1", "L2", "L3"):
    top1 = [((res[p["pid"]][lv].get("ranked") or [None])[0] == p["condition"]) for p in patients]
    agree = [((res[p["pid"]][lv].get("ranked") or [None])[0] == (res[p["pid"]]["L0"].get("ranked") or [None])[0]) for p in patients]
    out["levels"][lv] = {"top1": round(sum(top1) / len(top1), 3), "agree": round(sum(agree) / len(agree), 3)}
for dep in ("high", "medium", "low"):
    P = [p for p in patients if (p.get("vignette") or {}).get("context_dependence") == dep]
    out["by_context_dependence"][dep] = {lv: round(sum((res[p["pid"]][lv].get("ranked") or [None])[0] == p["condition"] for p in P) / len(P), 3) for lv in ("L0", "L1", "L2", "L3")}
(ROOT / "results/e2_weak_tool.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=1))
