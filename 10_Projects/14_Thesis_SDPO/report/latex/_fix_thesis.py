# -*- coding: utf-8 -*-
"""Apply advisor feedback to the thesis LaTeX:
  1. remove inline code/variable/function names from the body (ch2, ch3) -> plain prose;
     concrete code identifiers stay only in the appendix.
  2. move the shared-loop pseudocode from ch3 body into Appendix A.
  3. replace the section symbol '§' with 'Section~' everywhere (no special chars).
  4. clean a citation that embedded a codebase note.
Applied identically to the modular build (b_ch*.tex, b_appendix.tex) and the
flattened Overleaf single file (main_bestcase_overleaf.tex)."""
import re, io, os

BASE = "/mnt/c/Users/Maidanng/Repos/myVault/10_Projects/14_Thesis_SDPO/report/latex"
FILES = ["b_ch1.tex", "b_ch2.tex", "b_ch3.tex", "b_ch4.tex", "b_ch5.tex",
         "b_ch6.tex", "b_ch7.tex", "b_appendix.tex", "main_bestcase_overleaf.tex"]

# ---- literal (old, new) replacements: code identifiers -> prose ------------
PAIRS = [
    # ch2: stopgrad
    (r"where \passthrough{\lstinline!stopgrad!} prevents the teacher",
     r"where the stop-gradient operator prevents the teacher"),

    # ch3 §3.2 student-first
    (r"realized through the \passthrough{\lstinline!SDPOTrainer!} of TRL {[}5{]} (script \passthrough{\lstinline!07\_discovery\_curve.py!}).",
     r"realized through the self-distillation trainer of TRL {[}5{]}."),
    (r"The \passthrough{\lstinline!stopgrad!} blocks gradient flow through the teacher",
     r"The stop-gradient operator blocks gradient flow through the teacher"),

    # ch3 §3.3 motivation / implementation
    (r"Because \passthrough{\lstinline!SDPOTrainer!} hard-codes the student-first rollout internally, teacher-first is implemented as a custom training loop (script \passthrough{\lstinline!09\_teacher\_first.py!}) that reuses the helpers of \passthrough{\lstinline!07!} (\passthrough{\lstinline!build\_privileged\_context!}, \passthrough{\lstinline!build\_dynamic\_feedback!}, \passthrough{\lstinline!evaluate\_solution!}, evaluation).",
     r"Because the baseline trainer hard-codes the student-first rollout internally, teacher-first is implemented as a custom training loop that reuses the baseline's feedback-construction and evaluation helpers (Appendix A)."),

    # tf-step figure node labels
    (r"\node(j) at (0,1){judge: is\_copy / independence};",
     r"\node(j) at (0,1){judge: copy / independent};"),
    (r"\node(fs) at (4.8,3){few-shot good\_only / good\_bad};",
     r"\node(fs) at (4.8,3){few-shot good-only / good-bad};"),

    # ch3 §3.3.2 teacher rollout
    (r"the teacher samples \(N\) trajectories (\passthrough{\lstinline!teacher\_n!}) at high temperature",
     r"the teacher samples \(N\) trajectories at high temperature"),
    (r"The \passthrough{\lstinline!privileged\_context!} \(c\) is the concrete realization of ``feedback'' from {[}1{]}; the name belongs to the thesis codebase, the concept to the paper. The content of \(c\) is domain-dependent (§3.5). The few-shot block is inserted before the final directive (``Respond with ONLY\ldots{}''), with at most \passthrough{\lstinline!max\_fewshot = 3!} exemplars so the context does not overflow, and the token count is logged each step.",
     r"The privileged context \(c\) is the concrete realization of ``feedback'' from {[}1{]}. The content of \(c\) is domain-dependent (§3.5). The few-shot block is inserted before the final directive (``Respond with ONLY\ldots{}''), with at most three exemplars so the context does not overflow, and the token count is logged each step."),

    # ch3 §3.3.3 verifier/judge
    (r"For code (LCBv6), \passthrough{\lstinline!evaluate\_solution!} runs the public and private tests",
     r"For code (LCBv6), the verifier runs the public and private tests"),
    (r"\passthrough{\lstinline!difflib!} & \passthrough{\lstinline!SequenceMatcher!} string similarity on normalized code",
     r"String similarity & sequence-matching similarity on normalized code"),
    (r"LLM & groq \passthrough{\lstinline!llama-3.3-70b!} (code) or \passthrough{\lstinline!glm-4.5-flash!} (math), a derive-vs-copy prompt returning \passthrough{\lstinline!is\_copy!} and \passthrough{\lstinline!reasoning\_quality!} 1--5 & API cost, semantic",
     r"LLM & Llama-3.3-70B (code) or GLM-4.5-Flash (math), a derive-vs-copy prompt returning a copy flag and a reasoning-quality score (1--5) & API cost, semantic"),
    (r"so \passthrough{\lstinline!reasoning\_quality!} grades that trace rather than saturating at 4--5. The LLM judge therefore serves two roles: \passthrough{\lstinline!is\_copy!} is the independence gate for the good pool, while \passthrough{\lstinline!reasoning\_quality!} provides the signal",
     r"so the reasoning-quality score grades that trace rather than saturating at 4--5. The LLM judge therefore serves two roles: the copy flag is the independence gate for the good pool, while the reasoning-quality score provides the signal"),

    # ch3 §3.3.4 few-shot steering (condition labels)
    (r"\subsection{Few-shot teacher steering (good\_only vs good\_bad)}",
     r"\subsection{Few-shot teacher steering (good-only vs good-bad)}"),
    (r"Option 2: \passthrough{\lstinline!good\_only!}",
     r"Option 2: good-only"),
    (r"Option 1: \passthrough{\lstinline!good\_bad!}",
     r"Option 1: good-bad"),
    (r"Since \passthrough{\lstinline!bad ≈ reference!}, putting bad exemplars",
     r"Since a bad exemplar is by construction close to the reference, putting bad exemplars"),

    # ch3 §3.3.5 distillation step
    (r"the loss gradient with respect to a student logit is {[}1; derivation in \passthrough{\lstinline!con\_sdpo\_loss\_mechanics!}{]}:",
     r"the loss gradient with respect to a student logit is {[}1{]}:"),
    (r"The student prompt (\passthrough{\lstinline!x + y\_good!}) and the teacher prompt (\passthrough{\lstinline!x + c + y\_good!}) have different prefix lengths, so the logits at the positions of \(y_{\text{good}}\) must be extracted on each side before the KL is taken. An off-by-one here corrupts the KL silently, so the code asserts that the two lengths match and logs \passthrough{\lstinline!(student\_prefix\_len, teacher\_prefix\_len)!}.",
     r"The student prompt (problem plus good trajectory) and the teacher prompt (problem plus context plus good trajectory) have different prefix lengths, so the logits at the positions of \(y_{\text{good}}\) must be extracted on each side before the KL is taken. An off-by-one here corrupts the KL silently, so the implementation asserts that the two lengths match and logs both prefix lengths."),
    (r"Hyperparameters: AdamW \passthrough{\lstinline!lr = 1e-5!}, \passthrough{\lstinline!kl\_topk = 20!}, \passthrough{\lstinline!kl\_alpha = 1.0!}, \passthrough{\lstinline!is\_clip = 2.0!}. The teacher is always detached (self-distillation with shared weights, so the teacher is the student forward pass under context \(c\), run under \passthrough{\lstinline!no\_grad!}).",
     r"Hyperparameters (full list in Appendix A): AdamW with learning rate \(10^{-5}\), top-K of 20, reverse KL (\(\alpha = 1.0\)), and importance-sampling clip 2.0. The teacher is always detached (self-distillation with shared weights, so the teacher is the student forward pass under context \(c\), run without gradients)."),

    # ch3 §3.5 domains table + prose
    (r"\passthrough{\lstinline!reference\_mode!} & \passthrough{\lstinline!best\_in\_batch!} (best-scoring trajectory as proxy) & \passthrough{\lstinline!ground\_truth!} (teacher always sees the correct answer) \\",
     r"Reference mode & best-in-batch (best-scoring trajectory as proxy) & ground-truth answer (teacher always sees the correct answer) \\"),
    (r"\passthrough{\lstinline!privileged\_context!} & execution feedback (failing test, expected/actual, error type) + the correct best-in-batch trajectory & the correct answer (a number); the teacher need only copy \passthrough{\lstinline!\\boxed\{\}!} \\",
     r"Privileged context & execution feedback (failing test, expected/actual, error type) + the correct best-in-batch trajectory & the correct answer (a number); the teacher need only copy the boxed final answer \\"),
    (r"A note on the \passthrough{\lstinline!reference\_text!} choice for code: LCBv6 has no reliable reference-solution field, so the thesis uses best\_in\_batch (the highest-scoring trajectory in the teacher's batch each step) as the reference against which the judge measures independence.",
     r"A note on the reference choice for code: LCBv6 has no reliable reference-solution field, so the thesis uses the best-in-batch trajectory (the highest-scoring trajectory in the teacher's batch each step) as the reference against which the judge measures independence."),
    (r"which explains why the good\_bad ablation is leak-null for code",
     r"which explains why the good-bad ablation is leak-null for code"),
    (r"code runs 15 steps, eval 16 samples, teacher\_n = 10; math runs 3 steps, eval 4 samples, teacher\_n = 4, max\_new\_tokens = 16384 (8192 truncated the \passthrough{\lstinline!\\boxed!} answer and produced spurious zero scores).",
     r"code runs 15 steps, 16 eval samples, and 10 teacher samples; math runs 3 steps, 4 eval samples, 4 teacher samples, and a longer generation limit of 16384 tokens (8192 truncated the boxed answer and produced spurious zero scores)."),
    (r"MATH-500 (which has a \passthrough{\lstinline!solution!} field) is the route",
     r"MATH-500 (which provides a worked-solution field) is the route"),

    # ch3 §3.6 metrics
    (r"for each condition we draw \passthrough{\lstinline!N\_eval!} samples (16 for code, 4 for math) and report \passthrough{\lstinline!pass\_rate!}, the fraction correct.",
     r"for each condition we draw a fixed number of samples (16 for code, 4 for math) and report the fraction correct."),
    (r"A single deterministic \passthrough{\lstinline!greedy!} sample is reported alongside as a noisy secondary signal.",
     r"A single deterministic greedy sample is reported alongside as a noisy secondary signal."),

    # ch3 shared-loop intro sentence (listing itself removed by regex below)
    (r"Both arms share one skeleton. The single thing that differs between them is \emph{which trajectories are distilled}:",
     r"Both arms share one skeleton, and the single thing that differs between them is \emph{which trajectories are distilled}. Each run loads the base model with its LoRA adapter and optimizer, evaluates the student once before training (PRE), and then repeats \(K\) test-time steps: it builds execution feedback from the student's attempt, generates trajectories (the arm-specific step), selects the distillation targets (the core difference between the two arms), and takes one optimizer step on the per-token KL loss whenever a target exists. After the loop it evaluates the student again (POST) and reports the PRE-to-POST change and the discovery curve. The full pseudocode is listed in Appendix A."),
]

APPENDIX_SECTION = r"""token-aligned over the target trajectory (§3.3.5).

\section{Shared test-time training loop (pseudocode)}\label{a.3-shared-ttt-loop}

Both arms (student-first and teacher-first) share the skeleton below and differ only in the two arm-specific lines (trajectory generation and target selection). In the codebase, student-first is realized with the library trainer \texttt{SDPOTrainer} (script \texttt{07\_discovery\_curve.py}); teacher-first is a custom training loop (script \texttt{09\_teacher\_first.py}) that reuses the baseline's feedback-construction and evaluation helpers.

\begin{lstlisting}
load base model + LoRA + optimizer (AdamW, lr = 1e-5)
PRE-eval (student pi_theta(*|x) only, N_eval samples)        # baseline
for step in 1..K:
    feedback        <- build_feedback(student attempt, verifier)   # rich feedback
    {trajectories}  <- generate(...)                               # arm-specific
    {distill_targets} <- select(...)                               # arm-specific (the core difference)
    if distill_targets != {}:
        theta <- theta - lr * grad_theta L_KL(distill_targets)                    # one optimizer step
    log step stats -> W&B
POST-eval (student pi_theta(*|x) only, N_eval samples)       # after TTT
report PRE->POST and the discovery curve
\end{lstlisting}

\chapter{Reprompt templates (verbatim)}"""

def process(text, fname):
    report = {}
    # 1. remove the shared-loop pseudocode listing from the body
    n = 0
    def _rm(m):
        nonlocal n; n += 1; return ""
    text = re.sub(r"\\begin\{lstlisting\}\nload base model.*?\\end\{lstlisting\}\n\n",
                  _rm, text, flags=re.S)
    report["body_listing_removed"] = n
    # 2. insert the pseudocode section into Appendix A (anchor still has §)
    anchor = "token-aligned over the target trajectory (§3.3.5).\n\n\\chapter{Reprompt templates (verbatim)}"
    c = text.count(anchor)
    if c:
        text = text.replace(anchor, APPENDIX_SECTION)
    report["appendix_section_inserted"] = c
    # 3. literal code->prose replacements
    for old, new in PAIRS:
        cnt = text.count(old)
        if cnt:
            text = text.replace(old, new)
        report[old[:38]] = cnt
    # 4. awkward bare "§5" self-reference -> parent-paper citation
    old55 = "The §5 setup uses a fixed sliding window"
    report["the_S5_setup"] = text.count(old55)
    text = text.replace(old55, "The test-time setup {[}1, §5{]} uses a fixed sliding window")
    # 5. global § -> Section~ (done last so anchors above still matched)
    report["section_symbols"] = text.count("§")
    text = text.replace("§", "Section~")
    return text, report

for fn in FILES:
    p = os.path.join(BASE, fn)
    with io.open(p, encoding="utf-8") as f:
        txt = f.read()
    out, rep = process(txt, fn)
    with io.open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(out)
    hits = {k: v for k, v in rep.items() if v}
    print(f"== {fn} ==")
    for k, v in hits.items():
        print(f"   {v:>2}  {k}")
print("done")
