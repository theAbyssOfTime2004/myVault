#!/usr/bin/env python3
"""
Export all runs from the W&B project into a tidy CSV.

Auth: run `wandb login` once in this shell (stores key in ~/.netrc), or set
WANDB_API_KEY. This script never prints the key.

Output: wandb_runs.csv next to this file — one row per run, with arm/seed/
problem split into columns and every scalar summary metric flattened to sum_*.
"""

import os
import pandas as pd
import wandb

ENTITY_PROJECT = "dangmai781-tr-ng-i-h-c-khoa-h-c-t-nhi-n-hqg-hcm/ttt-sdpo-thesis"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "wandb_runs.csv")

CONFIG_KEYS = [
    "domain", "problem_index", "seed", "reprompt_template", "reference_mode",
    "fewshot_option", "judge", "max_steps", "eval_samples", "teacher_n",
    "policy_loss_mode", "model_name",
]


def arm_of(name: str) -> str:
    n = (name or "").lower()
    if "teacherfirst" in n:
        return "TF"
    if "discovery" in n:
        return "SF"
    return "?"


def main():
    api = wandb.Api()
    runs = api.runs(ENTITY_PROJECT)
    rows = []
    for run in runs:
        cfg = {k: v for k, v in run.config.items() if not k.startswith("_")}
        summ = run.summary._json_dict
        row = {
            "name": run.name,
            "id": run.id,
            "state": run.state,
            "created_at": str(run.created_at),
            "arm": arm_of(run.name),
        }
        for k in CONFIG_KEYS:
            row[k] = cfg.get(k)
        # flatten scalar summary metrics
        for k, v in summ.items():
            if not k.startswith("_") and isinstance(v, (int, float, bool)):
                row[f"sum_{k}"] = v
        rows.append(row)

    df = pd.DataFrame(rows)
    # stable, useful sort
    sort_cols = [c for c in ("domain", "problem_index", "arm", "seed") if c in df.columns]
    if sort_cols:
        df = df.sort_values(sort_cols, na_position="last")
    df.to_csv(OUT, index=False)
    print(f"Wrote {len(df)} runs -> {OUT}")
    print("Summary metric columns:", [c for c in df.columns if c.startswith("sum_")])


if __name__ == "__main__":
    main()
