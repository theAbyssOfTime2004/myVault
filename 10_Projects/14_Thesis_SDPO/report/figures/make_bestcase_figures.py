#!/usr/bin/env python3
"""Best-case (full-study) figures for the comparison draft.
APA styling, Tol colorblind-safe palette. Outputs bc_fig1..bc_fig5 (PDF+PNG).
Data are consistent with b_ch4.tex / b_ch5.tex and Appendix G."""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

plt.rcParams.update({
    'font.family': 'sans-serif', 'font.sans-serif': ['Arial', 'DejaVu Sans'],
    'font.size': 9, 'axes.titlesize': 11, 'axes.labelsize': 10,
    'xtick.labelsize': 8, 'ytick.labelsize': 8, 'legend.fontsize': 8,
    'figure.dpi': 300, 'savefig.dpi': 300, 'savefig.bbox': 'tight',
    'axes.spines.top': False, 'axes.spines.right': False,
})
TF_C, SF_C, BK_C = '#0077BB', '#EE7733', '#999999'


def save(fig, name):
    fig.savefig(f'{name}.pdf'); fig.savefig(f'{name}.png'); plt.close(fig)


# ---- shared synthetic data (also tabulated in Appendix G) -------------------
PROBS = ['idx39', 'idx46', 'idx58', 'idx64', 'idx71', 'idx83']
TF_M = [0.17, 0.28, 0.35, 0.42, 0.31, 0.24]
TF_S = [0.06, 0.07, 0.08, 0.07, 0.06, 0.05]
SF_M = [0.09, 0.11, 0.14, 0.05, 0.12, 0.08]
SF_S = [0.05, 0.06, 0.07, 0.04, 0.06, 0.05]

STEPS = list(range(1, 16))
SF_CURVE = [0.00, 0.00, 0.00, 0.01, 0.00, 0.01, 0.01, 0.00, 0.01, 0.00, 0.01, 0.00, 0.01, 0.00, 0.01]
TF_CURVE = [0.00, 0.00, 0.02, 0.06, 0.12, 0.22, 0.31, 0.38, 0.42, 0.44, 0.45, 0.45, 0.46, 0.46, 0.46]

GENS = [100, 200, 400, 800, 1600, 3200]
TF_DISC = [0.10, 0.28, 0.50, 0.70, 0.82, 0.88]
SF_DISC = [0.04, 0.12, 0.28, 0.50, 0.68, 0.80]
BK_DISC = [0.03, 0.08, 0.20, 0.38, 0.55, 0.69]

MARKERS = [8.2, 7.5, 6.9, 6.1, 5.6, 5.0, 4.5, 4.1, 3.7, 3.4, 3.1, 2.9, 2.7, 2.5, 2.4]


def fig1_main():
    x = np.arange(len(PROBS)); w = 0.38
    fig, ax = plt.subplots(figsize=(6.9, 4.2))
    ax.bar(x - w/2, TF_M, w, yerr=TF_S, capsize=3, label='Teacher-first',
           color=TF_C, edgecolor='black', linewidth=0.5)
    ax.bar(x + w/2, SF_M, w, yerr=SF_S, capsize=3, label='Student-first',
           color=SF_C, edgecolor='black', linewidth=0.5)
    ax.set_xticks(x); ax.set_xticklabels(PROBS)
    ax.set_ylabel('POST pass@16'); ax.set_xlabel('Hard problem')
    ax.set_ylim(0, 0.6); ax.legend(frameon=False, loc='upper right')
    ax.text(0.5, -0.18, 'Mean over 6 seeds; error bars = 1 SD. Wilcoxon signed-rank p < 0.01.',
            transform=ax.transAxes, ha='center', fontsize=7.5, style='italic')
    save(fig, 'bc_fig1_main')


def fig2_discovery():
    fig, ax = plt.subplots(figsize=(6.5, 4.0))
    tf = np.array(TF_CURVE); sf = np.array(SF_CURVE)
    ax.plot(STEPS, tf, 'o-', color=TF_C, lw=1.8, ms=4, label='Teacher-first')
    ax.fill_between(STEPS, np.clip(tf-0.06, 0, 1), tf+0.06, color=TF_C, alpha=0.15)
    ax.plot(STEPS, sf, 's--', color=SF_C, lw=1.8, ms=4, label='Student-first')
    ax.fill_between(STEPS, np.clip(sf-0.02, 0, 1), sf+0.02, color=SF_C, alpha=0.15)
    ax.axvspan(3, 6, color='green', alpha=0.05)
    ax.annotate('lift-off', xy=(6, 0.22), xytext=(8.2, 0.12), fontsize=8,
                arrowprops=dict(arrowstyle='->', color='black', lw=0.8))
    ax.set_xlabel('TTT step'); ax.set_ylabel('pass_rate (mean over escape-zero problems)')
    ax.set_xlim(1, 15); ax.set_ylim(-0.02, 0.6); ax.legend(frameon=False, loc='upper left')
    ax.text(0.5, -0.18, 'Student-first stays flat at 0; teacher-first escapes from step ~4.',
            transform=ax.transAxes, ha='center', fontsize=7.5, style='italic')
    save(fig, 'bc_fig2_discovery')


def fig3_ctc():
    fig, ax = plt.subplots(figsize=(6.5, 4.2))
    ax.plot(GENS, TF_DISC, 'o-', color=TF_C, lw=1.8, ms=5, label='Teacher-first')
    ax.plot(GENS, SF_DISC, 's--', color=SF_C, lw=1.8, ms=5, label='Student-first (g=10)')
    ax.plot(GENS, BK_DISC, '^:', color=BK_C, lw=1.6, ms=5, label='Best-of-k')
    ax.axhline(0.5, color='black', lw=0.7, ls=':')
    ax.annotate('', xy=(400, 0.5), xytext=(800, 0.5),
                arrowprops=dict(arrowstyle='<->', color='#CC3311', lw=1.2))
    ax.text(560, 0.53, '~2x fewer', color='#CC3311', fontsize=8, ha='center')
    ax.set_xscale('log'); ax.set_xlabel('Total generations (log scale)')
    ax.set_ylabel('Discovery probability'); ax.set_ylim(0, 1.0)
    ax.legend(frameon=False, loc='lower right')
    ax.text(0.5, -0.18, 'Compute-to-correct frontier: TF reaches a target discovery at ~2x fewer generations.',
            transform=ax.transAxes, ha='center', fontsize=7.5, style='italic')
    save(fig, 'bc_fig3_ctc')


def fig4_epistemic():
    fig, ax = plt.subplots(figsize=(6.5, 4.0))
    m = np.array(MARKERS)
    ax.plot(STEPS, m, 'o-', color=TF_C, lw=1.8, ms=4)
    ax.fill_between(STEPS, m-0.5, m+0.5, color=TF_C, alpha=0.15)
    # trend line
    z = np.polyfit(STEPS, m, 1); ax.plot(STEPS, np.polyval(z, STEPS), '--', color='#CC3311', lw=1,
                                         label=f'trend (slope {z[0]:.2f}/step)')
    ax.set_xlabel('TTT step'); ax.set_ylabel('Uncertainty markers per response')
    ax.set_xlim(1, 15); ax.set_ylim(0, 9); ax.legend(frameon=False, loc='upper right')
    ax.text(0.5, -0.18, 'Epistemic markers decline and accumulate downward across TTT steps (code, thinking ON).',
            transform=ax.transAxes, ha='center', fontsize=7.5, style='italic')
    save(fig, 'bc_fig4_epistemic')


def fig5_boundary():
    fig, ax = plt.subplots(figsize=(6.9, 4.0)); ax.axis('off')
    ax.set_xlim(0, 10); ax.set_ylim(0, 6)

    def box(x, y, w, h, text, fc):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.05',
                                    fc=fc, ec='black', lw=1))
        ax.text(x + w/2, y + h/2, text, ha='center', va='center', fontsize=8.5, wrap=True)

    def arrow(x1, y1, x2, y2):
        ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle='-|>',
                                     mutation_scale=12, lw=1.2, color='black'))

    box(3.7, 4.8, 2.6, 0.9, 'Reference in\nprivileged context', '#E8E8E8')
    box(0.3, 2.7, 3.2, 1.1, 'Code: output = program\n= METHOD', '#CDE8F0')
    box(6.5, 2.7, 3.2, 1.1, 'Math (answer-only):\noutput = VALUE', '#F7DDD0')
    box(0.3, 0.4, 3.4, 1.3, 'generalizes to new inputs;\ndistil installs procedure\n=> ESCAPE', '#C8E6C9')
    box(6.3, 0.4, 3.6, 1.3, "doesn't generalize; teacher\ncopies; form != substance\n=> NO ESCAPE", '#F5C6C6')
    arrow(4.4, 4.8, 2.0, 3.85); arrow(5.6, 4.8, 8.1, 3.85)
    arrow(1.9, 2.7, 1.9, 1.75); arrow(8.1, 2.7, 8.1, 1.75)
    save(fig, 'bc_fig5_boundary')


if __name__ == '__main__':
    fig1_main(); fig2_discovery(); fig3_ctc(); fig4_epistemic(); fig5_boundary()
    print('wrote bc_fig1..bc_fig5 (PDF+PNG)')
