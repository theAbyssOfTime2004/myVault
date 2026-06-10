# Thesis SDPO — Log

Chronological record of ingests, queries, and lint passes. Append-only.

Tip: `grep "^## \[" log.md | tail -5` shows the five most recent entries.

---

## [2026-04-22] bootstrap | wiki scaffolding created

- Created: `CLAUDE.md`, `wiki/index.md`, `wiki/log.md`, empty dirs for `raw/`, `wiki/sources/`, `wiki/entities/`, `wiki/concepts/`, `wiki/synthesis/`
- Existing `SDPO 2026-04-11.md` left in place; referenced from index as the thesis proposal. Migration to `wiki/synthesis/syn_thesis_proposal.md` pending user decision.
- Key takeaway: architecture ready. Next step is ingesting the two core sources (Hübotter et al., Kim et al. 2026).

## [2026-04-22] ingest | Hübotter et al. 2026 — Reinforcement Learning via Self-Distillation

- Source: `raw/hubotter2026_sdpo.md` (abstract + metadata clip from arXiv; full PDF pending)
- Created: [[src_hubotter2026_self_distillation]], [[ent_sdpo]], [[ent_rlvr]], [[ent_livecodebench]], [[con_rich_feedback]], [[con_self_teacher]], [[con_credit_assignment]]
- Updated: `wiki/index.md` (3 entities, 3 concepts, 1 source added; planned list shrunk)
- Depth: **abstract-only**. Full paper methods/results sections not yet ingested — download PDF to `raw/` and re-ingest to deepen pages (especially [[src_hubotter2026_self_distillation]] method section and [[ent_sdpo]] distillation objective).
- Key takeaway: SDPO's core move is treating the model-conditioned-on-feedback as a [[con_self_teacher]] to densify the sparse scalar reward of [[ent_rlvr]]. This frames the thesis's test-time variant clearly — same mechanism, frozen weights, template ablation.

## [2026-04-22] ingest | Hübotter et al. 2026 — **deep re-ingest (full PDF 50 pages)**

- Source: `raw/hubotter2026_sdpo.md` upgraded — full PDF extracted từ `\\wsl.localhost\Ubuntu\home\theabyssoftime\Repos\SDPO_thesis\sdpo.pdf` (§1–§7 + appendices A–F).
- Depth upgrade: **abstract-only → full-paper**. Giờ wiki cover được formal loss, 3 evaluation regimes (§3 RLVR / §4 RLRF / §5 test-time), toàn bộ ablations (feedback content, credit granularity, template, scale), và future work.
- Pages deepened: [[src_hubotter2026_self_distillation]], [[ent_sdpo]], [[ent_rlvr]], [[ent_livecodebench]], [[con_rich_feedback]], [[con_self_teacher]], [[con_credit_assignment]]
- Pages created: [[ent_grpo]], [[ent_rlrf]], [[ent_qwen3_8b]], [[ent_olmo3_7b_instruct]], [[con_reprompt_template]], [[con_test_time_self_distillation]], [[con_discovery_at_k]]
- Updated: `wiki/index.md` (entities 3→6, concepts 3→6, planned list shrunk).
- Key numbers captured: SDPO 48.8% vs GRPO 41.2% LCBv6 (§4); Chemistry 6× sample-efficiency (Olmo3-7B); test-time TTT-SDPO 3× fewer attempts on very-hard, 2.4× on hard (§5.2, discovery@k metric); compute overhead +5.8%–+17.1%; feedback ablation Table 6 (output+own_solution = 48.3% best); credit granularity logit > token > sequence > GRPO.
- Key takeaway (validation): paper §7 Future Work **trực tiếp mention thesis topic** — *"Future work should systematically study how individual aspects, such as the reprompt template, influence behavior"*. RQ1 (template taxonomy) được authors viết thẳng ra là open direction. Kết hợp với việc §5 không đo epistemic verbalization → RQ2 (suppression ở test-time) cũng là gap thật. CTC metric (RQ3) là natural extension của [[con_discovery_at_k]] vì các method có cost/attempt khác nhau.
- Lint deferred: một số wiki entry mới reference stubs chưa tạo (`con_teacher_regularization`, `con_epistemic_verbalization`, `con_ctc_metric`, `con_code_uncertainty_signals`) — listed in index's planned section.

## [2026-04-22] ingest | Kim et al. 2026 — Why Does Self-Distillation (Sometimes) Degrade Reasoning

- Source: `raw/kim2026_why_self_distillation_degrades.md` (arXiv:2603.24472v1, 18-page PDF full-ingest từ `C:\Users\Maidanng\Downloads\2603.24472v1.pdf`).
- Created: [[src_kim2026_why_self_distillation_degrades]], [[src_kim2026_strategic_info_allocation]] (stub), [[con_epistemic_verbalization]], [[con_uncertainty_suppression]], [[con_task_coverage]], [[ent_deepseek_distill_7b]].
- Updated: [[ent_sdpo]] (critique section + EMA contradiction), [[ent_qwen3_8b]] (thinking ON/OFF behavior), [[ent_olmo3_7b_instruct]] (Chemistry counterpoint), [[con_self_teacher]] (fixed vs moving teacher), [[con_reprompt_template]] (template as suppression lever), [[con_test_time_self_distillation]] (RQ2 gap section), [[con_credit_assignment]] (suppression not penalized caveat).
- Updated: `wiki/index.md` (sources 1→3, entities 6→7, concepts 6→9, planned list shrunk).
- Key findings captured: suppression 10 epistemic tokens (wait/hmm/maybe/...); SFT on correct solution-guided responses drops AIME24 54.8→20.2; SDPO drops AIME24 ~40% on DeepSeek-R1-Distill-7B; EMA 0.0 > EMA 0.05 (contradicts Hübotter default); task coverage Chemistry 6 types narrow vs DAPO-Math 14k broad.
- Key takeaway cho thesis: paper fill RQ2 framework formally — suppression là phenomenon documented, nhưng **chưa ai đo ở test-time code**. RQ2 scope intact, thậm chí strengthened vì có reference quantitative. Contradiction EMA forces thesis phải ablate hyperparam. RQ1 × RQ2 intersection formalized: template là "suppression lever" qua `I(y;c|x)`.
- Note: hai papers chính của thesis (Hübotter + Kim) **agree là open problems đó chính là thesis RQs**. Hübotter §7 future work explicit về template, Kim §7 explicit về preserving uncertainty-aware reasoning.

## [2026-05-02] synthesis | template taxonomy rationale

- Created: [[syn_template_taxonomy_rationale]] — principled justification cho 7 templates qua 3 dimensions: (1) information content ← Kim et al. `I(y;c|x)`; (2) instruction framing ← Hübotter §4.6 + §7 open question; (3) memory depth ← Hübotter §5 sliding window + Kim suppression accumulation.
- Updated: `wiki/index.md` (synthesis 2→3).
- Key takeaway: taxonomy defensible mà không cần cite source mới — derive trực tiếp từ 2 papers đã có. Template T2 là anchor, 6 còn lại vary đúng 1 dimension mỗi cái → clean ablation design.

## [2026-05-02] migrate | thesis design spec → syn_thesis_proposal

- Source: `2026-04-12-sdpo-thesis-design.md` (Cursor, generated 2026-04-12) — bản đầy đủ nhất của thesis plan, chưa được ingest vào wiki.
- Created: [[syn_thesis_proposal]] — ground truth design spec với title, RQ1/2/3, 7 templates (T1–T7), 4 components, budget ~$200, timeline 12 tuần, cut-list, risks.
- Updated: `wiki/index.md` (synthesis 1→2, removed old SDPO 2026-04-11 stub link).
- Key new info so với wiki cũ: 7 templates đã define đầy đủ (T1 Minimal / T2 Standard / T3 Verbose / T4 JSON / T5 Reasoning-inducing / T6 First-person / T7 Cumulative); budget là ~$200 không phải $100; pilot model là Qwen3-1.7B; 2 waves experiment.

## [2026-04-23] experiment | multi-turn inference loop — first working end-to-end

- **Status**: Pipeline hoạt động end-to-end trên LCBv6, 1 câu/lần chạy.
- **Components confirmed working**:
  - Load 1 bài từ `train.parquet`
  - Model sinh lời giải (Qwen3-8B, vLLM)
  - Evaluator chạy test cases → trả rich feedback
  - Reprompt loop với feedback → lặp đến khi pass hoặc hết budget
  - Logging đầy đủ: reward/acc, prompt+response token length, feedback detail, total runtime
- **Observed behavior trên 3 câu**:
  - `q_2`: pass gần như ngay (easy case)
  - `q_120`: pass sau số turn trung bình
  - `q_1`: pass sau **54 turns**, nhiều lỗi trung gian (MemoryError) trước khi hội tụ — cho thấy hard-case cần nhiều iteration
- **Note**: Đây là **multi-turn inference** (không có weight update) — baseline tương đương `baseline_multiturn/multiturn.py` trong [[src_lasgroup_sdpo_repo]]. Bước tiếp theo là thêm SDPO gradient step để thành test-time SDPO thật sự.
- **Infrastructure gap đã bridge**: pipeline 1-câu hoạt động → foundation để add weight update layer lên trên.

## [2026-04-23] concept | SDPO loss mechanics derivation

- Created: [[con_sdpo_loss_mechanics]] — derivation kỹ thuật KL divergence → gradient per logit = π_S − π_T, generalized JSD (α), IS correction, EMA teacher update, top-K approximation. Includes code refs (`core_algos.py:1085`) và implications cho RQ1/RQ2/RQ3.
- Updated: `wiki/index.md` (concepts 9→10).
- Key takeaway: formal mechanism chứng minh template (c) và α là knobs trực tiếp trên gradient direction — không chỉ là hyperparam empirical. α ablation là new angle RQ2 chưa ai test.

## [2026-04-23] ingest | lasgroup/SDPO codebase (GitHub raw API)

- Source: https://github.com/lasgroup/SDPO — read via curl GitHub raw (không clone). Files covered: `README.md`, `verl/trainer/config/sdpo.yaml`, `verl/trainer/config/actor/actor.yaml` (templates + defaults), `verl/trainer/ppo/core_algos.py` (`compute_self_distillation_loss` line 1085), `verl/workers/actor/dp_actor.py` (`TrustRegionTeacher`, `_update_teacher` EMA), `experiments/{generalization,rich_feedback,ttt}/*.sh`, `baseline_multiturn/multiturn.py`, `run_local_sdpo.sh`.
- Created: [[src_lasgroup_sdpo_repo]].
- Updated: `wiki/index.md` (sources 3→4).
- Key findings: (1) **no dedicated TTT-SDPO script** — `experiments/ttt/` chỉ có multi-turn baseline, thesis phải tự wire up; (2) default `remove_thinking_from_demonstration=True` trùng Kim's `c=s\think`; (3) rich_feedback LCBv6 hyperparams khác default đáng kể — ALPHA=1.0 (reverse KL), LR=1e-6, mini_batch=1, topk=20, ema=0.01; (4) α knob (forward/JSD/reverse KL) chưa được Kim ablate — thesis RQ2 ablation mới; (5) fixed teacher bật qua `teacher_update_rate=0.0` không cần code change; (6) 19 LCB hard question IDs = {1,3,10,43,46,59,69,74,86,91,92,95,100,103,111,120,125,127,129}; (7) templates là plain strings với placeholders — trivial cho RQ1 taxonomy.
- Key takeaway: infrastructure cho RQ1 và RQ2 (ngoại trừ TTT loop) có sẵn qua config flags. Thesis implementation cost chính = TTT-SDPO loop + epistemic token logging callback. Hyperparam differentials giữa §3 và §4 cho biết code regime cần tuning riêng từ scratch.

## [2026-04-22] synthesis | Kim 2026 thesis impact consolidation

- Created: [[syn_kim2026_thesis_impact]] — first synthesis page của thesis.
- Purpose: gom thesis impact notes rải trong entities/concepts về 1 page, chuẩn bị cho proposal/chapter writing.
- Contains: RQ1/2/3 impact mapping, hyperparam contradiction table (Hübotter vs Kim), validation framing với direct quotes, testable hypotheses, action items.
- Updated: `wiki/index.md` (synthesis section giờ có 1 page + proposal stub).

## [2026-05-19] ingest | Shenfeld et al. 2026 (SDFT) + YouTube discussion + RQ2 wedge angle

- Sources ingested:
  - `arXiv:2601.19897` (Shenfeld, Damani, **Hübotter**, Agrawal) — abstract via WebFetch + author-narrated mechanism từ YouTube transcript.
  - YouTube panel `OgEGV7apEzI` — auto-caption transcript `C:/Users/Maidanng/Downloads/[English (auto-generated)] Why Self-Distillation Is Taking Over LLM Post-Training (w the Researchers).txt` (2458 lines).
- Created: [[src_shenfeld2026_sdft]], [[src_youtube_hubotter_shenfeld_discussion]].
- Updated: [[syn_kim2026_thesis_impact]] — thêm section "Wedge angle RQ2" với verbatim quote Hübotter tự thừa nhận giảm hmm/wait (positive framing) vs Kim (negative framing); validation framing extended với quote thứ ba.
- Updated: `wiki/index.md` (sources 4→6).
- Key takeaway 1 (mechanism): Shenfeld giải thích **"implicit bias toward minimum change"** là cơ chế chính SDFT avoid catastrophic forgetting — on-policy gradient tự nhiên hội tụ về policy gần π_prior nhất, không cần KL regularization explicit. Generality claim: validate trên LLM, robotic foundation model, MLP MNIST.
- Key takeaway 2 (wedge): Hübotter **tự thừa nhận** SDPO dùng ít hmm/wait — frame là "efficiency, no circular reasoning" — đối lập với Kim et al. frame "suppression of epistemic uncertainty, AIME24 drop 40%". Thesis RQ2 position: **first test-time CODE evidence trên debate này**.
- Key takeaway 3 (implementation): HuggingFace TRL đã merge cả SDFT lẫn SDPO (2026-05). Thesis có thể **drop verl path**, switch sang `trl + peft + LoRA`. Action item: WebFetch TRL repo verify API.
- Key takeaway 4 (limitation): Hübotter quote "as you scale models you get better self teachers" → Qwen3-8B teacher có thể yếu hơn Qwen3-32B/72B → thesis nên acknowledge trong limitation, có Plan B framing nếu không reproduce 2.4× speedup.
- Lint pending: [[src_shenfeld2026_sdft]] mới ở depth `abstract+transcript-explanation`, chưa full-PDF ingest. Cần upgrade khi có thời gian để verify "minimum change" có formal statement (bound/theorem) trong §3-4 không.

## [2026-06-09] experiment+rootcause | max_prompt_length bug found → first real effectiveness on medium problem

- **Root cause của mọi "rambling rollout"**: TRL `max_prompt_length` default = **512 token** âm thầm cắt cụt đề bài dài trong TRAINING rollout (eval code của mình không cắt → eval ra code, training lảm nhảm). idx 23 prompt = 644 token > 512 → model thấy đề cụt → viết tiếp đề (" below: #.#.#...") → reward 0 mọi step. Fix: `max_prompt_length=4096` trong SDPOConfig.
- **Invalidate các kết luận trước**: "4B không giải nổi bài grid" (sai — eval score 1.0), "8B cũng ramble nên không phải size" (run 8B dính cùng bug cắt), "easy work / hard fail" (thật ra là đề NGẮN lọt 512 / đề DÀI bị cắt — difficulty tương quan với độ dài đề).
- **Debug method tìm ra bug**: in completion training qua reward_fn (thấy " below:" nối tiếp đề) → in prompt trainer nhận qua `prompts` arg của reward_fn → đếm token rendered prompt (644) so với trainer.max_prompt_length.
- **Post-fix run (idx 23 abc390_c medium, Qwen3-4B, 15 step, 16 eval, A100, seed 0)**: rollout = code thật có variance, discovery curve LEO 0.58 → plateau 1.00, pass_rate 0.375→0.750 (+0.375), VERDICT IMPROVED. Nuance: greedy đã 1.0 từ trước → improvement = sampling reliability consolidation.
- **Tổng bằng chứng effectiveness**: idx 19 (easy, greedy 0.85→1.0, 2026-06-06) + idx 23 (medium, pass 2x) → TTT-SDPO work end-to-end trên 2 mức độ khó. Còn thiếu: replicate seeds.
- Key takeaway: hạ tầng đã vững → pivot sang phần đóng góp chính: so sánh `reprompt_template` (RQ1) trên các testbed frontier [7,19,23,29].

## [2026-05-29] experiment | Phase 1 — feedback path (Path B) proven on Colab L4

- **Status**: Phase 1 PASS. Script `experiments/ttt_trl/06_feedback_path_test.py` (copy của 05 + bật Path B).
- Config thay đổi: `include_environment_feedback=True`, `environment_feedback_only_without_solution=True`, `privileged_context` = public test cases (parse JSON string từ raw row).
- Kết quả vs kickoff (05): abc387_b loss 0→0.0049, abc387_f loss 0→0.0045. **abc387_f có ZERO successful rollout** (rewards [0,0,0,0] cả 2 step, warning "did not find any successful rollouts") nhưng loss≠0 → loss chỉ có thể từ Path B = bằng chứng sạch feedback path hoạt động trên bài hard không có lời giải đúng.
- Caveat trung thực: (1) signal feedback YẾU, ~20x nhỏ hơn Path A (teacher-with-hint không đổi distribution nhiều trên completion đã fail → KL nhỏ); (2) abc387_a step2 cải thiện là sampling NOISE không phải Path B (nó dùng Path A vì có solution; chưa set seed); (3) vẫn chưa proof-of-effectiveness — loss≠0 nhưng reward chưa cải thiện trong 2 step.
- `privileged_context`=public-tests là static-hint thay thế tạm; Phase 2 multi-turn sẽ thay bằng feedback từ attempt fail thật.
- Updated: [[syn_implementation_status]] (Phase 1 → DONE).
- Key takeaway: tầng 2 (feedback/reprompt) chạm được — Path B densify learning cho bài khó. Next = Phase 2 multi-turn loop + kéo pre/post eval vào để đo effectiveness.

## [2026-05-29] experiment+synthesis | cloud kickoff — TTT-SDPO weight-update working on Colab L4

- **Status**: proof-of-mechanism đạt. Full TTT-SDPO pipeline (gen→eval→weight update) chạy thật trên Colab L4 + Qwen2.5-1.5B + LoRA r=32 qua `trl.experimental.sdpo.SDPOTrainer`. Lần đầu `train_loss ≠ 0` trên data thật (abc387_a = 0.0492).
- Created: [[syn_implementation_status]] — status snapshot + SDPO mechanism trace + 4-phase forward plan.
- Updated: `wiki/index.md` (synthesis 3→4).
- Kickoff results (3 bài, 2 step): solvable 2/3 (abc387_a, abc387_b), useful signal 2/3. Qwen 0.5B trước đó all-zero → model size là gating factor; 1.5B giải được LCBv6 easy. Peak VRAM 7.4/22GB, ~32s/step, bf16 no NaN.
- Mechanism trace (trl source): `reprompt_template` là SDPOConfig string arg ({prompt}/{solution}/{feedback}) = biến RQ1, đổi string không cần sửa code. Distill kích hoạt iff has_solution (rollout reward≥success_reward_threshold default 1.0) OR use_feedback (include_environment_feedback=True + privileged_context). Kickoff chỉ Path A bật → giải thích abc387_b reward 0.35<1.0 nên loss=0.
- Divergence: W2 plan giả định hand-rolled `ttt_sdpo/` module (port core_algos.py loss + EMATeacher); thực tế dùng thẳng TRL SDPOTrainer (đúng quyết định switch verl→TRL 2026-05-19). §3/§9 của W2 plan superseded.
- Repo: `theAbyssOfTime2004/thesis-ttt-sdpo` (private). W&B: `ttt-sdpo-thesis`. Colab deps gap: ray, tensordict, omegaconf, hydra-core, pylatexenc, torchao>=0.16.
- Key takeaway: engine khởi động được + biết chính xác đòn bẩy thesis nằm ở `reprompt_template` + Path B (feedback). Next = Phase 1 bật feedback path. Còn gap: proof-of-effectiveness (pre/post eval) chưa làm.

## [2026-05-19] ingest+decision | TRL SDPO/SDFT trainer integration → switch implementation từ verl sang TRL

- Sources fetched:
  - https://huggingface.co/docs/trl/en/sdpo_trainer (SDPO trainer docs, full)
  - https://huggingface.co/docs/trl/sdft_trainer (SDFT trainer docs, full)
  - https://github.com/huggingface/trl/blob/main/trl/experimental/sdpo/sdpo_trainer.py (partial, code structure)
- Also fetched (for comparison, ruled out): https://github.com/Gen-Verse/OpenClaw-RL — production agent framework, 8× GPU requirement, OPD = SDPO-inspired variant không phải canonical → citation only, không reference implementation.
- Created: [[src_trl_sdpo_sdft_docs]] — full source page với 5 finding, 3 caveat, 3-way comparison verl vs TRL vs OpenClaw, implementation roadmap 5 stage, code template Phase 3.
- Updated: [[src_lasgroup_sdpo_repo]] — supersession note ở top: scientific reference giữ nguyên, implementation switch sang TRL.
- Updated: `wiki/index.md` (sources 6→7, marked TRL as ⭐ implementation reference).
- Key takeaway 1 (decision): switch verl → TRL. Tiết kiệm ~1-2 tuần infrastructure work. Critical wins: LoRA/PEFT built-in (must-have với compute budget), template ablation qua Python dict thay vì YAML.
- Key takeaway 2 (trade-off): mất trust-region teacher mode (Hübotter §4.3 best). EMA + frozen mode (Kim ablation) vẫn cover được core RQ2 contradiction. Document trong limitation section.
- Key takeaway 3 (risk): TTT loop phải tự wrap (~100-200 dòng glue). Bug risk cao ở: weight persist giữa các `.train()` call, LoRA adapter save/restore, generation dùng updated weight. Phải test ở Stage 1 sanity trên 0.5B local trước khi commit.
- Key takeaway 4 (unknown): vLLM support cho SDPO unclear. SDFT docs explicit "does not support `use_vllm=True`". Cần verify SDPO bằng cách đọc source code hoặc test thực tế. Mitigation plan: decouple generation (vLLM) và training (TRL).
- Action items next:
  - [ ] `pip install trl==1.4.0 peft datasets accelerate` trên local + smoke test trên Qwen2.5-0.5B
  - [ ] Verify TRL SDPO vLLM support (read source code)
  - [ ] Implement TTT wrap loop, test weight persistence
  - [ ] Define 7 templates (still blocker cho RQ1)

