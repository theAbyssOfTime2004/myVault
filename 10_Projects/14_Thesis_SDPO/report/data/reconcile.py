#!/usr/bin/env python3
"""
reconcile.py — from the 192 runs, pick the CANONICAL matched run per
(problem, arm, seed), dedup by latest created_at, and verify the per-seed means
reproduce the published wiki numbers before anything is trusted for a figure.
Also pulls per-step discovery curves (correct metric per arm) for escape-zero seeds.

Run: ~/tfig/bin/python reconcile.py   (after wandb login)
"""
import json
import pandas as pd
import wandb

EP = "dangmai781-tr-ng-i-h-c-khoa-h-c-t-nhi-n-hqg-hcm/ttt-sdpo-thesis"
HERE = "/mnt/c/Users/Maidanng/Repos/myVault/10_Projects/14_Thesis_SDPO/report/data"
T2_STR = "Correctly solve the original question"

# canonical judge per problem (from syn_core_result main matched tables)
CANON_JUDGE = {39: ["difflib", None, "nan"], 12: ["difflib", None, "nan"],
               64: ["llm"], 77: ["difflib"]}
WIKI_MEAN = {  # (SF, TF) targets
    39: (0.094, 0.172), 12: (0.844, 1.000), 64: (0.047, 0.422), 77: (0.203, 0.344)}

api = wandb.Api()
runs = list(api.runs(EP))

rows = []
for r in runs:
    cfg = {k: v for k, v in r.config.items() if not k.startswith("_")}
    s = r.summary._json_dict
    arm = "TF" if r.name.startswith("teacherfirst") else ("SF" if r.name.startswith("discovery") else "?")
    rows.append({
        "name": r.name, "arm": arm, "created": str(r.created_at),
        "problem_index": cfg.get("problem_index"), "seed": cfg.get("seed"),
        "reprompt": str(cfg.get("reprompt_template")),
        "fewshot": cfg.get("fewshot_option"), "judge": str(cfg.get("judge")),
        "post_pass_rate": s.get("post_pass_rate"), "pre_pass_rate": s.get("pre_pass_rate"),
    })
df = pd.DataFrame(rows)


def canonical(prob):
    sub = df[(df.problem_index == prob) & df.post_pass_rate.notna()]
    sf = sub[(sub.arm == "SF") & sub.reprompt.str.contains(T2_STR, na=False)]
    tf = sub[(sub.arm == "TF") & (sub.fewshot == "good_only")
             & sub.judge.isin(CANON_JUDGE[prob])]
    # dedup: latest created per seed
    sf = sf.sort_values("created").groupby("seed", as_index=False).last()
    tf = tf.sort_values("created").groupby("seed", as_index=False).last()
    return sf, tf


print("=== per-seed reconciliation (POST pass@16) ===")
out = {}
for prob in [39, 12, 64, 77]:
    sf, tf = canonical(prob)
    sf_m, tf_m = sf.post_pass_rate.mean(), tf.post_pass_rate.mean()
    w_sf, w_tf = WIKI_MEAN[prob]
    ok = abs(sf_m - w_sf) < 0.03 and abs(tf_m - w_tf) < 0.03
    print(f"\nidx{prob}  [{'OK' if ok else 'MISMATCH'}]  SF mean {sf_m:.3f} (wiki {w_sf})  TF mean {tf_m:.3f} (wiki {w_tf})")
    for arm, t in [("SF", sf), ("TF", tf)]:
        vals = {int(r.seed): round(r.post_pass_rate, 4) for _, r in t.iterrows() if pd.notna(r.seed)}
        print(f"   {arm}: {vals}")
    out[prob] = {"SF": {int(r.seed): r.post_pass_rate for _, r in sf.iterrows() if pd.notna(r.seed)},
                 "TF": {int(r.seed): r.post_pass_rate for _, r in tf.iterrows() if pd.notna(r.seed)}}

with open(f"{HERE}/perseed_canonical.json", "w") as f:
    json.dump(out, f, indent=2)
print(f"\nwrote perseed_canonical.json")

# === discovery curves (per-step) for escape-zero seeds =======================
# TF metric = curve/batch_mean_reward ; SF metric = curve/mean_reward
targets = [(39, 1), (64, 1), (64, 2)]
curve = []
for r in runs:
    cfg = {k: v for k, v in r.config.items() if not k.startswith("_")}
    arm = "TF" if r.name.startswith("teacherfirst") else ("SF" if r.name.startswith("discovery") else "?")
    for prob, seed in targets:
        if cfg.get("problem_index") == prob and cfg.get("seed") == seed and arm in ("TF", "SF"):
            # only canonical arm configs
            if arm == "TF" and (cfg.get("fewshot") != "good_only" and cfg.get("fewshot_option") != "good_only"):
                continue
            if arm == "SF" and T2_STR not in str(cfg.get("reprompt_template")):
                continue
            metric = "curve/batch_mean_reward" if arm == "TF" else "curve/mean_reward"
            try:
                h = r.history(keys=[metric, "curve/step"])
            except Exception:
                continue
            if metric not in h.columns:
                continue
            for _, hr in h.iterrows():
                curve.append({"problem_index": prob, "seed": seed, "arm": arm,
                              "name": r.name, "step": hr.get("curve/step"),
                              "reward": hr.get(metric)})
cdf = pd.DataFrame(curve)
cdf.to_csv(f"{HERE}/escape_curves.csv", index=False)
print(f"wrote escape_curves.csv ({len(cdf)} rows)")
if len(cdf):
    print("\n=== escape-zero per-step (pivot) ===")
    for (prob, seed), g in cdf.groupby(["problem_index", "seed"]):
        print(f"\nidx{prob} seed{seed}:")
        for arm, ga in g.groupby("arm"):
            ga = ga.sort_values("step")
            print(f"   {arm}: " + " ".join(f"{v:.3f}" for v in ga.reward if pd.notna(v)))
print("\nDONE.")
