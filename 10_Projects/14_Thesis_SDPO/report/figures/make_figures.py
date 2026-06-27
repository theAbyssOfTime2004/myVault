#!/usr/bin/env python3
"""
make_figures.py — generates all data-plot figures for the thesis report.

APA 7.0 styling, Tol qualitative palette (colorblind-safe), saves PDF + PNG.
Run:  python make_figures.py     (outputs into the current folder)

Data are transcribed verbatim from the experiment records (syn_core_result,
syn_math_pilot). Where only means are available (idx64/idx77, no per-seed),
bars are drawn without error bars and the limitation is noted in the caption.
Figures requiring data not yet exported (15-step per-step escape-zero curves,
trajectory exemplars) are NOT produced here; see report TODOs.
"""

import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'font.size': 9, 'axes.titlesize': 11, 'axes.labelsize': 10,
    'xtick.labelsize': 8, 'ytick.labelsize': 8, 'legend.fontsize': 8,
    'figure.dpi': 300, 'savefig.dpi': 300, 'savefig.bbox': 'tight',
    'axes.spines.top': False, 'axes.spines.right': False,
})

# Tol qualitative palette (colorblind-safe)
TF_C, SF_C = '#0077BB', '#EE7733'      # teacher-first / student-first
CB = ['#0077BB', '#33BBEE', '#009988', '#EE7733', '#CC3311', '#EE3377', '#BBBBBB']


def save(fig, name):
    fig.savefig(f'{name}.pdf', format='pdf')
    fig.savefig(f'{name}.png', format='png')
    plt.close(fig)


# ----------------------------------------------------------------------
# Per-seed records (idx39, idx12) — eval-16
SEED = {
    'idx39': {'PRE': [0.000, 0.000, 0.062, 0.188],
              'TF':  [0.438, 0.062, 0.125, 0.062],
              'SF':  [0.188, 0.000, 0.125, 0.062]},
    'idx12': {'PRE': [0.000, 0.062, 0.062, 0.125],
              'TF':  [1.000, 1.000, 1.000, 1.000],
              'SF':  [0.938, 0.500, 1.000, 0.938]},
}
# Means only (no per-seed exported)
MEAN_ONLY = {'idx64': {'TF': 0.422, 'SF': 0.047},
             'idx77': {'TF': 0.344, 'SF': 0.203}}


# ----------------------------------------------------------------------
def fig_4_1_main_result():
    """Grouped bar: TF vs SF mean POST across 4 problems; seed points where available."""
    probs = ['idx39', 'idx12', 'idx64', 'idx77']
    tf_mean = [np.mean(SEED['idx39']['TF']), np.mean(SEED['idx12']['TF']),
               MEAN_ONLY['idx64']['TF'], MEAN_ONLY['idx77']['TF']]
    sf_mean = [np.mean(SEED['idx39']['SF']), np.mean(SEED['idx12']['SF']),
               MEAN_ONLY['idx64']['SF'], MEAN_ONLY['idx77']['SF']]
    tf_sd = [np.std(SEED['idx39']['TF']), np.std(SEED['idx12']['TF']), 0, 0]
    sf_sd = [np.std(SEED['idx39']['SF']), np.std(SEED['idx12']['SF']), 0, 0]

    x = np.arange(len(probs)); w = 0.38
    fig, ax = plt.subplots(figsize=(6.9, 4.3))
    ax.bar(x - w/2, tf_mean, w, yerr=tf_sd, capsize=3, label='Teacher-first',
           color=TF_C, edgecolor='black', linewidth=0.5)
    ax.bar(x + w/2, sf_mean, w, yerr=sf_sd, capsize=3, label='Student-first',
           color=SF_C, edgecolor='black', linewidth=0.5)
    # overlay seed points for idx39, idx12
    for i, p in enumerate(['idx39', 'idx12']):
        jit = (np.random.RandomState(0).rand(4) - 0.5) * 0.12
        ax.scatter(np.full(4, x[i]-w/2)+jit, SEED[p]['TF'], s=14, color='black', zorder=3)
        ax.scatter(np.full(4, x[i]+w/2)+jit, SEED[p]['SF'], s=14, color='black', zorder=3)
    ax.set_xticks(x); ax.set_xticklabels(probs)
    ax.set_ylabel('POST pass@16'); ax.set_xlabel('Problem')
    ax.set_ylim(0, 1.15); ax.legend(frameon=False, loc='upper center', ncol=2)
    ax.text(0.5, -0.22, 'Dots = per-seed (idx39, idx12, n=4). idx64/idx77: means only, no error bars.',
            transform=ax.transAxes, ha='center', fontsize=7.5, style='italic')
    save(fig, 'fig_4_1_main_result')


def fig_4_2_per_seed_slope():
    """PRE→POST slope per seed, two panels (idx39, idx12)."""
    fig, axes = plt.subplots(1, 2, figsize=(6.9, 3.8), sharey=True)
    for ax, p in zip(axes, ['idx39', 'idx12']):
        d = SEED[p]
        for k in range(4):
            ax.plot([0, 1], [d['PRE'][k], d['TF'][k]], '-o', color=TF_C, lw=1, ms=4, alpha=0.85)
            ax.plot([0, 1], [d['PRE'][k], d['SF'][k]], '--s', color=SF_C, lw=1, ms=4, alpha=0.85)
        ax.set_xticks([0, 1]); ax.set_xticklabels(['PRE', 'POST'])
        ax.set_title(p); ax.set_xlim(-0.2, 1.2); ax.set_ylim(-0.05, 1.1)
    axes[0].set_ylabel('pass@16')
    axes[0].plot([], [], '-o', color=TF_C, label='Teacher-first')
    axes[0].plot([], [], '--s', color=SF_C, label='Student-first')
    axes[0].legend(frameon=False, loc='upper left')
    save(fig, 'fig_4_2_per_seed_slope')


def fig_4_3_escape_zero():
    """Escape-zero instances: SF POST = 0 vs TF POST > 0 (endpoint view)."""
    inst = ['idx39 s1', 'idx64 s1', 'idx64 s2']
    pre = [0.000, 0.062, 0.000]
    tf = [0.062, 0.375, 0.062]
    sf = [0.000, 0.000, 0.000]
    x = np.arange(len(inst)); w = 0.38
    fig, ax = plt.subplots(figsize=(6.5, 4.0))
    ax.bar(x - w/2, tf, w, label='Teacher-first POST', color=TF_C, edgecolor='black', linewidth=0.5)
    ax.bar(x + w/2, sf, w, label='Student-first POST', color=SF_C, edgecolor='black', linewidth=0.5)
    ax.scatter(x, pre, marker='_', s=300, color='black', linewidth=1.5, label='PRE (both arms)')
    ax.set_xticks(x); ax.set_xticklabels(inst)
    ax.set_ylabel('pass@16'); ax.set_xlabel('Seed instance')
    ax.set_ylim(0, 0.45); ax.legend(frameon=False)
    ax.text(0.5, -0.20, 'Student-first stays at 0 while teacher-first escapes. '
            'Per-step 15-step curve pending log export.',
            transform=ax.transAxes, ha='center', fontsize=7.5, style='italic')
    save(fig, 'fig_4_3_escape_zero')


def fig_4_4_template():
    """RQ1: T1/T2/T5 POST pass@16 on idx12 (easy) and idx39 (hard)."""
    templates = ['T1\nminimal', 'T2\nstandard', 'T5\nreasoning']
    easy = [0.66, 0.97, 0.97]
    hard = [0.03, 0.06, 0.13]
    x = np.arange(len(templates)); w = 0.38
    fig, ax = plt.subplots(figsize=(6.3, 4.0))
    ax.bar(x - w/2, easy, w, label='idx12 (easy)', color=CB[1], edgecolor='black', linewidth=0.5)
    ax.bar(x + w/2, hard, w, label='idx39 (hard)', color=CB[4], edgecolor='black', linewidth=0.5)
    for i, v in enumerate(hard):
        ax.text(x[i] + w/2, v + 0.02, f'{v:.2f}', ha='center', fontsize=7.5)
    ax.set_xticks(x); ax.set_xticklabels(templates)
    ax.set_ylabel('POST pass@16'); ax.set_xlabel('Reprompt template')
    ax.set_ylim(0, 1.1); ax.legend(frameon=False)
    ax.text(0.5, -0.22, 'Monotone T5 > T2 > T1 on the hard problem (n = 2 seeds, directional).',
            transform=ax.transAxes, ha='center', fontsize=7.5, style='italic')
    save(fig, 'fig_4_4_template')


def fig_4_5_ablation():
    """Judge x few-shot ablation, mean POST pass (4 seeds)."""
    arms = ['SF\nbaseline', 'TF good_only\ndifflib', 'TF good_only\nLLM', 'TF good_bad\nLLM']
    idx39 = [0.094, 0.172, 0.266, 0.250]
    idx12 = [0.844, 1.000, 0.984, 1.000]
    x = np.arange(len(arms)); w = 0.38
    fig, ax = plt.subplots(figsize=(6.9, 4.2))
    ax.bar(x - w/2, idx12, w, label='idx12', color=CB[2], edgecolor='black', linewidth=0.5)
    ax.bar(x + w/2, idx39, w, label='idx39', color=CB[3], edgecolor='black', linewidth=0.5)
    ax.set_xticks(x); ax.set_xticklabels(arms)
    ax.set_ylabel('Mean POST pass@16'); ax.set_ylim(0, 1.15)
    ax.legend(frameon=False)
    ax.text(0.5, -0.24, 'TF >= SF under both judges and both few-shot options (leak-null).',
            transform=ax.transAxes, ha='center', fontsize=7.5, style='italic')
    save(fig, 'fig_4_5_ablation')


def fig_4_6_math_discovery():
    """Math discovery curves over 3 steps; eval pass stays 0 (form != substance)."""
    steps = [1, 2, 3]
    idx9 = [1.00, 1.00, 1.00]
    idx8 = [0.50, 0.75, 1.00]
    fig, ax = plt.subplots(figsize=(6.5, 4.0))
    ax.plot(steps, idx9, 'o-', color=CB[0], lw=1.5, ms=6, label='idx9 (boxed 148→168, ans 156)')
    ax.plot(steps, idx8, 's--', color=CB[4], lw=1.5, ms=6, label='idx8 (boxed 40201→17, ans 29)')
    ax.set_xticks(steps); ax.set_xlabel('TTT step'); ax.set_ylabel('Batch discovery (teacher)')
    ax.set_ylim(0, 1.1); ax.legend(frameon=False, loc='lower right')
    ax.annotate('Student eval pass@4 = 0 PRE and POST (no escape)',
                xy=(2, 0.05), fontsize=8, style='italic', color='#CC3311')
    ax.text(0.5, -0.22, 'Teacher batch "discovers" (copies answer) but the student never escapes 0.',
            transform=ax.transAxes, ha='center', fontsize=7.5, style='italic')
    save(fig, 'fig_4_6_math_discovery')


def fig_4_7_frontier_bands():
    """Math frontier scan: band membership counts (AIME 2026, 30 problems)."""
    bands = ['Frontier\n(0<pass<1)', 'Too-hard\n(pass=0)', 'Ceiling\n(pass=1)']
    counts = [4, 15, 11]
    colors = [CB[3], CB[4], CB[2]]
    fig, ax = plt.subplots(figsize=(6.0, 4.0))
    bars = ax.bar(bands, counts, color=colors, edgecolor='black', linewidth=0.5)
    for b, c in zip(bars, counts):
        ax.text(b.get_x() + b.get_width()/2, c + 0.3, str(c), ha='center', fontsize=9)
    ax.set_ylabel('Number of problems'); ax.set_ylim(0, 17)
    ax.text(0.5, -0.16, 'AIME 2026, Gemma-4-E4B thinking ON, n_samples = 2. Pilot problems idx9/idx8 are too-hard.',
            transform=ax.transAxes, ha='center', fontsize=7.5, style='italic')
    save(fig, 'fig_4_7_frontier_bands')


if __name__ == '__main__':
    fig_4_1_main_result()
    fig_4_2_per_seed_slope()
    fig_4_3_escape_zero()
    fig_4_4_template()
    fig_4_5_ablation()
    fig_4_6_math_discovery()
    fig_4_7_frontier_bands()
    print('Wrote fig_4_1 .. fig_4_7 (PDF + PNG).')
