#!/usr/bin/env python3
"""Check whether student-first (discovery) runs were ever run at a matched
generation budget (num_generations=10) like teacher-first (teacher_n=10)."""
import json
import pandas as pd

df = pd.read_csv("wandb_all_runs.csv")


def arm(n):
    return "TF" if str(n).startswith("teacherfirst") else ("SF" if str(n).startswith("discovery") else "?")


rows = []
for _, r in df.iterrows():
    cfg = json.loads(r["config"]) if isinstance(r["config"], str) else {}
    rows.append({
        "arm": arm(r["name"]),
        "idx": cfg.get("problem_index"),
        "seed": cfg.get("seed"),
        "num_generations": cfg.get("num_generations"),
        "teacher_n": cfg.get("teacher_n"),
        "name": r["name"],
    })
t = pd.DataFrame(rows)

print("=== config keys present (sample) ===")
print(sorted(json.loads(df.iloc[0]['config']).keys()))

print("\n=== SF (discovery): num_generations value counts ===")
print(t[t.arm == "SF"]["num_generations"].value_counts(dropna=False))

print("\n=== TF (teacherfirst): teacher_n value counts ===")
print(t[t.arm == "TF"]["teacher_n"].value_counts(dropna=False))
print("\n=== TF: num_generations value counts ===")
print(t[t.arm == "TF"]["num_generations"].value_counts(dropna=False))

print("\n=== ANY SF run with num_generations >= 10 ? ===")
hi = t[(t.arm == "SF") & (t.num_generations.fillna(0) >= 10)]
print(f"count = {len(hi)}")
if len(hi):
    print(hi[["idx", "seed", "num_generations", "name"]].to_string(index=False))

print("\n=== SF num_generations by problem (frontier idx) ===")
sub = t[(t.arm == "SF") & (t.idx.isin([12, 39, 64, 77]))]
print(sub.groupby(["idx", "num_generations"]).size())
