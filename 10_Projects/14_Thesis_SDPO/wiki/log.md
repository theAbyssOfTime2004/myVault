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

## [2026-06-14] experiment+concept | RQ1 template pilot + advisor's teacher-first idea

- **RQ1 pilot (code, Qwen3-4B, A100):** added `--reprompt_template` presets (T1/T2/T5/T6) to `07_discovery_curve.py`, pushed. Ran 3 templates × idx19(easy)/idx23(medium) × 1 seed = 6 runs, all IMPROVED.
  - Tentative signal: T5_reasoning yếu nhất ở cả 2 bài/2 metric; T1≈T2. **1 seed → chưa kết luận**, cần seeds. idx19 ceiling effect (base mean 0.906) → ít discriminate; idx23 informative hơn.
  - Confirmed: flat-reward warning xuất hiện đúng ở near-ceiling steps (variance = 0 → GRPO advantage collapse).
- **Created: [[con_teacher_first_judge]]** — method idea advisor đề xuất 2026-06-14. Teacher-first: teacher sinh N trajectory → judge/verifier lọc good/bad → few-shot good (Option 2) hoặc good+bad+label (Option 1) vào prompt teacher để steer → student học KL trên y_good. Mục tiêu: tránh information leak (Kim degradation).
- **Verl verifier check:** `feedback/math.py` là drop-in sibling của `feedback/code.py` → math wiring rẻ. Phát hiện: math reward **binary (0/1)** + "rich feedback" = đọc luôn đáp án → math là case leak cực đoan, lý tưởng để chứng minh + nối Kim.
- Plan chốt: teacher-first chạy **code + math**; student-first math làm baseline đối chứng (cần cho claim Kim). Ablation Option 1 vs 2 = contrastive vs positive = leak vs no-leak.
- Updated: `wiki/index.md` (concepts 10→11).
- Key takeaway: thesis từ empirical-thuần (RQ1 template) thêm **method contribution** (teacher-first anti-leak) — đúng hướng advisor muốn. Rủi ro: 3 trục mới (method + math + RQ2 metric) chồng lên 4 tuần → ưu tiên P0 code teacher-first.

## [2026-06-14] spec | teacher-first implementation spec → Cursor handoff

- Created: [[syn_teacher_first_impl_spec]] — spec cho `09_teacher_first.py` (custom loop, không dùng SDPOTrainer). Components: teacher_generate (few-shot good/bad), filter_trajectories (verifier + difflib similarity), teacher_first_step (KL reverse top-k, stopgrad teacher, căn token y_good), main loop (good_pool tích lũy, cold-start handling).
- Updated: `wiki/index.md` (synthesis 4→5).
- 2 quyết định treo cho Cursor surface: (1) reference_text cho code (LCBv6 có solution field không? → in row.keys()), (2) trl loss_utils có KL tái dùng không.
- Flow: Claude viết spec → user đưa Cursor implement → Claude review (checklist mục 7: token alignment, stopgrad, few-shot không lọt eval, cold-start).
- Key takeaway: P0 = code teacher-first, idx23, good_only, difflib similarity. P1 = good_bad ablation. P2 = math.

## [2026-06-14] experiment | teacher-first P0 first result (idx23) — pipeline verified, beats student-first (1 seed)

- `09_teacher_first.py` ran end-to-end on Colab A100 (Qwen3-4B, idx23, T2, good_only, best_in_batch, 15 steps, seed 0). 24 min, peak 13.8 GB, no crash.
- **Pipeline verified:** KL-sanity `KL(token-mean)=0.200` (>0, finite); token alignment correct (student_prefix=644, teacher_prefix=1617, both slices L=469 -> same y_good positions); stopgrad/filter/pool/cold-start all functioning.
- **Result (teacher-first):** pass_rate 0.500 -> **1.000** (Δ+0.500), mean 0.819 -> **1.000** (Δ+0.181). VERDICT IMPROVED.
- **vs student-first baseline (07, idx23 T2):** 0.500->0.750 (+0.250), 0.819->0.909 (+0.091). Teacher-first ~**doubled** both deltas; even beat student-first's best template (T1, +0.375 pass).
- **Caveats (do NOT overclaim):** (1) 1 seed, 1 problem, eval n=8. (2) NOT compute-matched — teacher_n=10 -> ~2.5x generations vs 07's num_generations=4; advantage may be partly "more samples" (-> RQ3/CTC). (3) Fast convergence: from step 2 batch_r=1.0, mean_sim≈0.9, n_good stuck at 1 (diversity collapse) -> anti-copy filter barely exercised; idx23 too easy. (4) greedy unchanged 1.0->1.0 -> gain is reliability, not discovery.
- Bugs fixed en route: wrong-version import (`SelfDistillationMixin` -> `trl.experimental.sdpo.loss_utils.compute_topk_self_distillation_loss`, 1.6.0 API); dangling `k` -> `kl_topk` in sanity print; `apply_chat_template(return_tensors="pt")` returns BatchEncoding -> render `tokenize=False` then `tokenizer(text)`.
- Next: (1) `08_frontier_scan` to find a real frontier problem (pass ~0.15-0.45, doesn't converge at step 2); (2) both arms × 2 seeds there; (3) log total generations -> CTC for fair compute comparison. Then Option 1 (good_bad) ablation + math P2.

## [2026-06-16] experiment | MATCHED comparison idx39 (hard) — teacher-first weakly dominates student-first

- **Setup:** frontier scan picked idx39 (abc393_d, hard, base pass≈0.1). Ran BOTH arms × **4 seeds** × **eval_samples=16** on **L4** (Qwen3-4B, 15 steps, T2). PRE-eval is identical per seed across arms (same base+seed) → clean matched comparison.
- **Result (POST pass_rate):**
  - seed0: PRE 0.000 → TF **0.438** / SF 0.188
  - seed1: PRE 0.000 → TF 0.062 / SF 0.000
  - seed2: PRE 0.062 → TF 0.125 / SF 0.125
  - seed3: PRE 0.188 → TF 0.062 / SF 0.062
  - **Mean POST: TF 0.172 vs SF 0.094 (~1.8×); mean Δ: TF +0.109 vs SF +0.031 (~3.5×).**
- **Verdict:** teacher-first **≥ student-first on ALL 4 seeds**, strictly > on 2/4 (paired diff +0.250/+0.062/0/0, never negative). NOT a wash, NOT noise — consistent directional signal. = **core positive result** (weak dominance).
- **Two honest findings:**
  1. **seed3 (high PRE 0.188) → BOTH arms degrade** to 0.062, identically → over-distillation when base already decent, **affects both arms equally** (not TF-specific). Confirms "start-high → degrade" pattern.
  2. Earlier "student-first stalls at 0" (eval 8) was eval noise; with eval16/4seed student-first does improve slightly on some seeds but **always ≤ TF**.
- **Caveats:** single problem; gains modest + noisy (per-seed diffs ~1 eval sample); strongest signal = mean + seed0. → need **≥1 more hard problem** to confirm "TF ≥ SF" generalizes.
- **Method confirmed on L4** (~13-18 min/run; teacher-first heavier). eval_samples=16 + 4 seeds = the rigor floor that distinguished signal from the earlier eval-8 noise.
- Next: 1 more hard problem (both arms × 4 seed × eval16) to confirm generalization; ask advisor whether his POC was train-time (would reconcile test-time instability as a regime difference).

## [2026-06-16] experiment | idx12 matched + 2-problem conclusion — teacher-first weakly dominates (REPLICATED)

- idx12 (abc389_b, nhãn "easy" nhưng model pass≈0.12 → model-hard; "frontier" tính theo MODEL pass-rate, không phải nhãn contest). Both arms × 4 seed × eval16, L4, T2. PRE khớp từng seed.
- **idx12 POST pass:** TF = 1.000/1.000/1.000/1.000 (mean 1.000); SF = 0.938/0.500/1.000/0.938 (mean 0.844). TF ≥ SF cả 4 seed, strictly > 3/4 (seed1: TF 1.0 vs SF 0.5). TF cũng **variance thấp hơn** (1.0 đều vs SF dao động).
- **TỔNG 2 bài × 4 seed = 8 matched comparisons:** TF ≥ SF **8/8**, strictly > **5/8**, tie 3/8, **TF < SF: 0/8**. Sign test thô (5 thắng / 0 thua trên cặp không-hòa) → p≈0.03.
- **CORE RESULT:** teacher-first weakly dominates student-first SDPO ở test-time discovery — ≥ mọi seed/bài, thường hơn, không bao giờ tệ hơn, ổn định hơn. Pattern **replicated qua 2 bài độc lập** → refute "kết quả ngẫu nhiên". Cơ chế: TF (off-policy-leaning) bơm solution đúng từ teacher → student học chắc/ổn hơn SF (on-policy, kém ổn khi rollout hiếm trúng).
- Caveat: weak dominance (nhiều hòa, margin nhỏ); 2 bài / 4B / T2 only; TF ~2.5× generation (CTC caveat); idx12 fixable-bug → margin nhỏ; idx39 harder → SF yếu hơn.
- Updated [[con_teacher_first_judge]] với idx12 matched + tổng 2 bài.
- Next options: (a) write-up core result; (b) RQ1 template ablation (T1/T5 vs T2) trên 2 arm; (c) more problems để tăng power; (d) math P2. Vẫn nên hỏi advisor POC regime.

## [2026-06-16] synthesis | core result write-up → syn_core_result.md

- Created [[syn_core_result]] — bản nháp Results: câu hỏi, setup, 2 bảng matched (idx39+idx12), tổng 8/8, kết luận weak-dominance, cơ chế on/off-policy + SDFT positioning, qualitative (discovery, collapse), limitations, hướng mở rộng.
- Updated `index.md` (synthesis 5→6).
- Dùng làm base để viết Method+Results thesis + mang đi bàn advisor.

## [2026-06-16] experiment | judge ablation (difflib vs LLM) — judge-invariant

- Implemented LLM-judge: provider chain groq(`llama-3.3-70b`) primary + gemini fallback + difflib final (cache, retry, key-filter). **Gemini free tier = 20 req/DAY** (quá thấp — tôi ước lượng sai trước đó) → groq primary. Ran good_only × {idx39,idx12} × 4 seed, all clean (judge_fallbacks=0).
- **mean POST pass (good_only):** idx39 — SF 0.094, TF-difflib 0.172, TF-LLM 0.266. idx12 — SF 0.844, TF-difflib 1.000, TF-LLM 0.984.
- **Conclusion: judge-invariant** — TF ≥ SF cả 2 bài cả 2 judge; difflib vs LLM cho POST ~như nhau. NHƯNG hai judge dán nhãn khác rõ: LLM (semantic) gọi ít copy hơn difflib (string≥0.9) → idx12 LLM n_good tới 10 vs difflib n_good=1. Labeling khác, outcome không đổi.
- rq luôn 4–5 (gemini+groq) + thinking off → judge = semantic copy-detector, KHÔNG đo reasoning.
- good_bad (Option 1) chưa chạy — optional, kỳ vọng cũng invariant.
- Updated [[con_teacher_first_judge]]. Recommendation: ablation đủ, chuyển sang viết.

## [2026-06-16] experiment | Option 1 (good_bad) judge LLM — Option 1 ≈ Option 2

- Ran good_bad × {idx39,idx12} × 4 seed, judge LLM-groq, T2, eval16, matched PRE (judge_fallbacks=0 cả 8 run).
- **mean POST pass (good_bad·LLM):** idx39 **0.250**, idx12 **1.000**.
- **So Option 1 vs Option 2 (good_only·LLM):** idx39 0.250 vs 0.266 (chênh trong noise), idx12 1.000 vs 0.984 (good_bad nhỉnh cực nhẹ). → **Option 1 ≈ Option 2: mối lo "leak" của advisor KHÔNG xuất hiện trên data này.** Thêm exemplar bad/copy vào few-shot teacher không đổi outcome.
- Matched vs SF: **7 thắng / 1 hòa / 0 thua** (idx39 thắng cả 4 — matched-win sạch nhất trên bài khó; idx12 thắng 3 + hòa 1). Sign test thô p ≈ 0.5⁷ ≈ 0.008. Vẫn weak dominance (n=2 bài).
- Updated [[syn_core_result]] (thêm section ablation Judge × Option). **Ablation phase ĐÓNG. Chuyển sang viết.**

## [2026-06-17] experiment | hard-frontier matched (idx64, idx77) — escape-zero trap

- Frontier scan idx0-90 (lưu scan.json): frontier mới = [46,58,59,64,69,77,78]. Chọn 2 bài hard pass-thấp (idx64 abc397_e 0.25, idx77 abc399_f 0.25) chạy matched SF+TF × 4 seed eval16.
- **idx64** (judge LLM-groq, sạch): SF TB 0.047 vs TF TB 0.422 — TF thắng 4/4, escape-zero seed1+seed2 (SF kẹt 0, TF thoát 0.375/0.062). Ca mạnh nhất (~9×).
- **idx77** (judge difflib, groq cạn TPD nên chuyển difflib): SF TB 0.203 vs TF TB 0.344 — TF thắng 3/1 hòa. Không escape-zero (SF không kẹt 0 ở bài này).
- **Tổng 3 bài hard (+ idx39 cũ): TF > SF cả 3, 9 thắng/3 hòa/0 thua, p≈0.002, escape-zero 3 instance.** Claim nâng từ "weak dominance" → "TF thoát flat-reward trap trên hard".
- **Bài học vận hành**: groq 100K TPD ≈ chỉ ~4 TF-run/ngày → idx64 LLM đã ăn hết budget; idx77 buộc difflib. Re-run idx64 LLM cho số khác (LLM judge non-deterministic) → KHÔNG đè data cũ. difflib là lựa chọn reproducible cho bảng chính.
- Updated [[syn_core_result]] (section hard-frontier extension).

## [2026-06-24] experiment | Math pilot AIME2026 (Gemma-4-E4B, thinking ON) — clean run, KHÔNG escape, judge bắt leak

- Migrate sang **Modal A100-80GB** (Colab CU hết). Hạ tầng giải quyết: `.spawn()`+`--detach` (miễn nhiễm crash máy), `PYTHONUNBUFFERED=1`, full `requirements.txt`. Bug fix: `get_reference_text` nhận int answer; judge `TimeoutError` không catch → crash (cap candidate `[-10000:]` + timeout 180s); 8192→**16384** chống truncate (8192 cụt → mất `\boxed` → score 0 giả).
- **Frontier scan 30 bài AIME2026**: frontier=[8,11,21,25], too-hard=15 bài, ceiling nhiều. Độ khó rải rác.
- **Run idx9 (aime2026_10, too-hard, đáp án 156)** — clean run TF math đầu tiên (judge chạy trọn 3 step + POST, không crash): **PRE 0 → POST 0, KHÔNG escape**. Boxed 148→168 (đều sai). `n_good=1 n_bad=3` mỗi step, `judge_calls=4`.
- **Phát hiện chính**: (1) judge bắt leak — teacher leaked-answer → **75% trajectory is_copy=true** (chỉ khẳng định 156, không derive); (2) idx9 beyond-capability (thinking-đầy-đủ vẫn sai → không phải thiếu compute); (3) "too hard" ≠ regime escape-zero của code (code=reachable, AIME too-hard=beyond-capability); (4) epistemic: satisficing số đẹp, suppression, self-correction theater, **TTT đổi form ≠ substance** (POST ngắn hơn + tự tin hơn nhưng vẫn sai = vegetative mimicry).
- Created [[syn_math_pilot]]. **Negative SẠCH + judge-leak finding → viết được làm pilot/contrast với code.**
- Next: thử frontier idx8 (regime đúng) HOẶC chốt report. Budget còn ~$50.

## [2026-06-24] experiment | Math idx8 replication — 2/2 bài AIME KHÔNG escape, chốt pilot

- idx8 (aime2026_9, đáp án 29): chạy trọn 4.1h (sau khi thêm `retries=2` chống preempt + monitoring sạch — crash trước là preempt/cancel ngắt quãng). **PRE 0 → POST 0, NO IMPROVEMENT.** PRE boxed 40201, POST boxed 17 (sai). Nhãn "frontier" từ scan n=2 sai — thực tế PRE=0/4 = beyond-capability.
- **Nuance**: POST idx8 rigorous HƠN (casework đếm, p=4/13) — ngược idx9 (POST lười shortcut 2K). Cả hai sai → TTT đổi form không đổi substance, **replicated 2 bài**.
- **Kết luận math pilot (idx9 + idx8, 2/2 KHÔNG escape)**: teacher-first cần *reachable capability* để escape (như code), không escape được khi teacher chỉ có đáp án trên bài beyond-capability → chỉ copy (judge bắt ~75%). Updated [[syn_math_pilot]].
- **DỪNG đốt AIME.** Report = code escape-zero (lõi) + math pilot (judge-leak + epistemic mimicry + contrast). Budget còn ~$35.

## [2026-06-25] experiment | RQ1 template ablation (SF/code, Modal) — T5 > T2 > T1 trên bài hard

- Smoke code-path trên Modal OK (sandbox execute, score non-trivial, ~20 phút/run Qwen-4B/15step). Dùng $20 dư cho RQ1.
- RQ1: SF (07, Qwen3-4B thinking-off, 15step eval16) × {T1_minimal, T2_standard, T5_reasoning} × {idx12, idx39} × 2 seed = 12 run (~$8). 1 lệnh chained, single-quote bash loop.
- **Kết quả POST pass@16**: idx39 (hard) **monotone T5(0.13) > T2(0.06) > T1(0.03)**, T5 ổn định 2 seed; idx12 (easy) T2≈T5 bão hòa 0.97, T1 tụt 0.66. → **template formulation CÓ ảnh hưởng, rõ nhất ở bài khó** (reprompt ép reasoning > anchor > tối giản). **RQ1 (titular) giờ có data.**
- Caveat: n=2 seed, số tuyệt đối nhỏ → directional. SF arm; chưa probe TF×template.
- Updated [[syn_core_result]] (section RQ1). Budget còn ~$12. **Thí nghiệm đóng — chuyển sang viết.**

## [2026-06-26] synthesis | Report writing hub + Discussion/Limitations tinh chỉnh

- Tạo [[syn_report_outline]] = writing hub: outline 30+ trang (tới subsection) + Discussion notes (3 điều kiện teacher-first work, value-vs-procedure, rich-feedback nối tiền đề SDPO) + Limitations (model confound code=Qwen/math=Gemma, judge degrade beyond-capability, fallback ép distill copy) + Future Work (Qwen3-4B+thinking CẢ 2 domain → 8B, MATH-500 + worked-solution reference).
- Thêm Phát hiện 4 vào [[syn_math_pilot]]: log idx8 chứng minh good_pool = bản chép fallback-rescued (mọi verdict is_copy=true) → fallback vô hiệu hóa judge khi beyond-capability.
- Cài skill `academic-paper` (Imbad0202/academic-research-skills) thủ công vào `.claude/skills/` (Desktop không có /plugin) — 12-agent pipeline viết paper. Discovery work.
- **Trạng thái: thí nghiệm + synthesis ĐÓNG. Sẵn sàng viết report.** Mọi context của thảo luận 2026-06-26 đã vào wiki → phiên mới đọc wiki là đủ.


- [2026-07-01] QUERY query="check current status of thesis - latest progress, POC status, TTT-SDPO implementation" result_pages=3 mode=normal escalated=true
