#!/usr/bin/env python3
"""
wb_export.py — export all runs from the W&B project, then build a tidy table
keyed by (arm, domain, problem_index, seed) with the PRE/POST pass metrics, plus
per-step discovery curves for the escape-zero seeds.

Auth: run `wandb login` once in this WSL shell first (key -> ~/.netrc).
Run:  ~/tfig/bin/python wb_export.py
Outputs (next to this script): wandb_all_runs.csv, wandb_tidy.csv, discovery_curves.csv
"""

import json
import pandas as pd
import wandb

ENTITY_PROJECT = "dangmai781-tr-ng-i-h-c-khoa-h-c-t-nhi-n-hqg-hcm/ttt-sdpo-thesis"
HERE = "/mnt/c/Users/Maidanng/Repos/myVault/10_Projects/14_Thesis_SDPO/report/data"

api = wandb.Api()
runs = list(api.runs(ENTITY_PROJECT))
print(f"total runs: {len(runs)}")

# ---- 1. raw dump (the user's original export) -------------------------------
rows = []
for run in runs:
    rows.append({
        "name": run.name,
        "state": run.state,
        "config": json.dumps({k: v for k, v in run.config.items() if not k.startswith("_")}),
        "summary": json.dumps(run.summary._json_dict, default=str),
    })
pd.DataFrame(rows).to_csv(f"{HERE}/wandb_all_runs.csv", index=False)
print(f"wrote wandb_all_runs.csv ({len(rows)} rows)")

# ---- 2. inspect available summary keys --------------------------------------
allkeys = set()
for run in runs:
    allkeys |= set(run.summary._json_dict.keys())
passish = sorted(k for k in allkeys if any(t in k.lower() for t in ("pass", "pre", "post", "greedy", "score", "discov")))
print("\n[summary keys that look like metrics]:")
print(passish)


def arm_of(name: str) -> str:
    if name.startswith("teacherfirst"):
        return "TF"
    if name.startswith("discovery"):
        return "SF"
    return "?"


# ---- 3. tidy table ----------------------------------------------------------
tidy = []
for run in runs:
    cfg = {k: v for k, v in run.config.items() if not k.startswith("_")}
    s = run.summary._json_dict
    rec = {
        "arm": arm_of(run.name),
        "domain": cfg.get("domain"),
        "problem_index": cfg.get("problem_index"),
        "seed": cfg.get("seed"),
        "reprompt_template": cfg.get("reprompt_template"),
        "reference_mode": cfg.get("reference_mode"),
        "fewshot_option": cfg.get("fewshot_option"),
        "judge": cfg.get("judge"),
        "name": run.name,
        "state": run.state,
    }
    for k in passish:
        rec[k] = s.get(k)
    tidy.append(rec)
tdf = pd.DataFrame(tidy)
tdf.to_csv(f"{HERE}/wandb_tidy.csv", index=False)
print(f"\nwrote wandb_tidy.csv ({len(tdf)} rows)")

# print the code-domain frontier problems used in the thesis
view = tdf[tdf["problem_index"].isin([12, 39, 64, 77, 23, 29])]
view = view.sort_values(["problem_index", "arm", "seed"], na_position="last")
cols = ["problem_index", "arm", "seed", "reprompt_template", "fewshot_option", "judge"] + passish
with pd.option_context("display.max_rows", None, "display.width", 200):
    print("\n[frontier code runs]:")
    print(view[cols].to_string(index=False))

# ---- 4. discovery curves for escape-zero seeds ------------------------------
# Identify the per-step batch-reward metric from one run's history.
targets = [("teacherfirst", 39, 1), ("discovery", 39, 1),
           ("teacherfirst", 64, 1), ("discovery", 64, 1),
           ("teacherfirst", 64, 2), ("discovery", 64, 2)]
curve_rows = []
hist_metric = None
for run in runs:
    cfg = {k: v for k, v in run.config.items() if not k.startswith("_")}
    for prefix, idx, seed in targets:
        if run.name.startswith(prefix) and cfg.get("problem_index") == idx and cfg.get("seed") == seed:
            h = run.history()
            if hist_metric is None:
                metric_cols = [c for c in h.columns if any(t in c.lower() for t in ("batch", "reward", "discov", "pass", "mean_r"))]
                print(f"\n[history columns for {run.name}]: {list(h.columns)}")
                print(f"[candidate step-metric columns]: {metric_cols}")
            for _, hr in h.iterrows():
                curve_rows.append({"run": run.name, "arm": arm_of(run.name),
                                   "problem_index": idx, "seed": seed,
                                   "_step": hr.get("_step"), **{c: hr.get(c) for c in h.columns
                                                                 if any(t in c.lower() for t in ("batch", "reward", "discov", "pass", "mean_r"))}})
if curve_rows:
    pd.DataFrame(curve_rows).to_csv(f"{HERE}/discovery_curves.csv", index=False)
    print(f"\nwrote discovery_curves.csv ({len(curve_rows)} rows)")
else:
    print("\n[no escape-zero target runs matched — check problem_index/seed in config]")

print("\nDONE.")
