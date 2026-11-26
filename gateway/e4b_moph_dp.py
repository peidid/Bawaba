"""E4b: Ministry tables, small-cell suppression vs differential privacy (no LLM).

The weekly surveillance extract counts patients by condition x municipality x age band. GW-MOPH-01
offers two protections, chosen by the DPO in the policy library:
  method = suppress   cells below cell_min are hidden ("<5")
  method = dp         every cell gets Laplace noise of scale 1/epsilon (sensitivity 1: one patient
                      changes one count by 1), then is rounded and clipped at 0
Both parameters are read from policies/gateway_rules.md, so changing the rule changes the table.

    python e4b_moph_dp.py        # writes results/e4b_moph_dp.json
"""
import json
import random
from collections import Counter
from pathlib import Path

import rag
from policy import age_band

ROOT = Path(__file__).parent
TRIALS = 2000


def laplace(rng, scale):
    return rng.expovariate(1 / scale) - rng.expovariate(1 / scale)


def main():
    lib = rag.Library()
    prof = lib.profile("moph_reporting")
    cell_min, eps0 = prof["params"]["cell_min"], prof["params"]["dp_epsilon"]
    patients = json.loads((ROOT / "data/patients.json").read_text())
    table = Counter((p["condition"], p["person"]["municipality"], age_band(p["person"]["age"])) for p in patients)
    # DP needs a fixed, public domain: every condition x municipality x age band, including empty cells,
    # otherwise the mere presence of a cell would reveal that someone is in it
    conds = sorted({c for c, _, _ in table}); munis = sorted({m for _, m, _ in table}); bands = sorted({b for _, _, b in table})
    cells = [((c, m, b), table.get((c, m, b), 0)) for c in conds for m in munis for b in bands]
    small = [(c, n) for c, n in cells if 0 < n < cell_min]
    out = {"source": {"rules": {k: prof["param_source"][k] for k in ("cell_min", "method", "dp_epsilon")},
                      "cell_min": cell_min, "dp_epsilon": eps0},
           "cells": len(cells), "nonzero_cells": sum(1 for _, n in cells if n), "patients": sum(table.values()),
           "suppress": {"cells_hidden": len(small), "share_nonzero_cells_hidden": round(len(small) / max(1, sum(1 for _, n in cells if n)), 3),
                        "patients_in_hidden_cells": sum(n for _, n in small),
                        "share_patients_hidden": round(sum(n for _, n in small) / sum(table.values()), 3)},
           "dp": {}}
    rng = random.Random(41)
    for eps in sorted({0.5, 1.0, 2.0, eps0}):
        abs_err, within1, small_err, total_err = [], 0, [], []
        for _ in range(TRIALS):
            noisy = {c: max(0, round(n + laplace(rng, 1 / eps))) for c, n in cells}
            errs = [abs(noisy[c] - n) for c, n in cells]
            abs_err += errs
            within1 += sum(e <= 1 for e in errs)
            small_err += [abs(noisy[c] - n) for c, n in small]
            total_err.append(abs(sum(noisy.values()) - sum(n for _, n in cells)))
        out["dp"][str(eps)] = {"mean_abs_error_per_cell": round(sum(abs_err) / len(abs_err), 3),
                               "share_cells_within_1": round(within1 / (TRIALS * len(cells)), 3),
                               "mean_abs_error_small_cells": round(sum(small_err) / max(1, len(small_err)), 3),
                               "mean_abs_error_total_count": round(sum(total_err) / TRIALS, 2),
                               "cells_hidden": 0}
    (ROOT / "results/e4b_moph_dp.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
