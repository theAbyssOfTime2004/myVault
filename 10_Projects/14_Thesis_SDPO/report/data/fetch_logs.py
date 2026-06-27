#!/usr/bin/env python3
"""Inspect files of finished code TF runs and download output.log if present."""
import os
import wandb

P = "dangmai781-tr-ng-i-h-c-khoa-h-c-t-nhi-n-hqg-hcm/ttt-sdpo-thesis"
HERE = "/mnt/c/Users/Maidanng/Repos/myVault/10_Projects/14_Thesis_SDPO/report/data"
api = wandb.Api()

for rid in ["jg610jqm", "usiu1tde", "uldu0lv0", "jqt1zwwk"]:
    r = api.run(f"{P}/{rid}")
    cfg = {k: v for k, v in r.config.items() if not k.startswith("_")}
    print(f"=== {r.name} | idx{cfg.get('problem_index')} seed{cfg.get('seed')} | {r.state} ===")
    names = []
    for f in r.files():
        names.append(f.name)
        print("   ", f.name, f.size)
    # try common console-log names
    for cand in ("output.log",):
        if cand in names:
            dst = f"{HERE}/log_{rid}.txt"
            r.file(cand).download(root=HERE, replace=True)
            os.replace(f"{HERE}/{cand}", dst)
            print(f"   -> downloaded {cand} as log_{rid}.txt")
            break
