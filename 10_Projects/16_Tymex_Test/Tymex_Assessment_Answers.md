---
title: Tymex Assessment — MCQ Answers
date: 2026-05-10
tags: [interview, assessment, tymex]
---

# Tymex Assessment — Phần Trắc Nghiệm Kiến Thức

> Tổng cộng **32 câu**: 22 câu trắc nghiệm + 10 câu code (Q5, Q7, Q8, Q11, Q14, Q15, Q17, Q23, Q25, Q26).
> Note này chỉ làm **22 câu trắc nghiệm**.

## Bảng tổng hợp đáp án nhanh

| Q | Đáp án | Q | Đáp án | Q | Đáp án | Q | Đáp án |
|---|--------|---|--------|---|--------|---|--------|
| 1 | A | 10 | A | 20 | A | 29 | A |
| 2 | C | 12 | C | 21 | A | 30 | A |
| 3 | B | 13 | D | 22 | A | 31 | C |
| 4 | A | 16 | C | 24 | A | 32 | A |
| 6 | B | 18 | A | 27 | D |   |   |
| 9 | D | 19 | A | 28 | A |   |   |

---

## Q1 — Root cause latency tăng trong AI inference pipeline

**Original question:**
> *Passage:* You are an intern on an engineering team responsible for maintaining an AI inference pipeline used in a production recommendation system. After a recent update that included a new model version and minor changes to preprocessing logic, the system's end-to-end latency has increased by 35%, breaching SLA targets. The pipeline consists of data ingestion, preprocessing, model inference, and post-processing stages, deployed across containerized services with autoscaling enabled. Logs show no obvious errors, but resource utilization has increased unevenly across components. Senior engineers are debating whether to optimize each component individually or redesign the pipeline architecture entirely, but no clear root cause has been identified.
> *Question:* As an intern tasked with contributing to the investigation, which approach best demonstrates sound technical reasoning for diagnosing the root cause of the latency increase?
> A. Instrument and profile each stage of the pipeline with fine-grained latency and resource metrics, compare against historical baselines, and identify bottlenecks before deciding whether localized optimization or architectural changes are needed.
> B. Scale up compute resources across all pipeline components to reduce latency quickly, and defer root cause analysis until after performance stabilizes under higher capacity, assuming scaling alone will resolve the issue.
> C. Focus only on optimizing the model inference stage by rewriting it for higher throughput and parallelization, assuming it is the main bottleneck without validating other pipeline stages or comparing against historical baseline metrics.
> D. Propose a full pipeline redesign using asynchronous processing and event-driven architecture as a long-term fix, without first identifying whether the latency increase originates from a specific stage or verifying the actual bottleneck.

**Phân tích:** Đề bài có hai signal then chốt: (1) "no clear root cause has been identified" → cấm patch mù, (2) "sound technical reasoning" → ưu tiên phương án có method luận. B/C/D đều bypass diagnose: B scale tiền, C giả định inference là bottleneck, D redesign khi chưa biết nguyên nhân. Chỉ A có chuỗi instrument → compare baseline → identify → mới quyết định.

**Đáp án: A** — Instrument and profile each stage, compare against historical baselines, identify bottlenecks first.

---

## Q2 — Sprint, dev không trả lời clarification, PO bận

**Original question:**
> *Passage:* You are an intern working on a cross-functional Agile team developing an AI-powered recommendation feature for a product in the competitive AI market. During a sprint, you are assigned to integrate a data preprocessing module. However, you notice that the requirements in the task ticket differ from what the developer working on the model expects. The product owner is currently busy preparing for a stakeholder demo and has not responded to your clarification message. The sprint deadline is approaching, and your work depends on aligning with both the developer and the product owner.
> *Question:* What is the most effective action you should take to handle this situation?
> A. Escalate the issue immediately to your manager, emphasizing the product owner's unresponsiveness, without attempting to align directly with the developer or clarify assumptions first.
> B. Proceed with the implementation strictly based on the task ticket to avoid delays, assuming any inconsistencies can be identified and fixed later without immediate clarification.
> C. Initiate a quick alignment discussion with the developer and attempt to clarify assumptions, document the agreed approach, and share it with the product owner for confirmation while continuing progress.
> D. Pause your work entirely until the product owner provides explicit instructions, avoiding any interim assumptions or alignment efforts to ensure correctness.

**Phân tích:** Hai constraint chính: deadline gấp + cần align cả dev lẫn PO. A escalate sớm là thiếu chủ động và làm xấu quan hệ. B coding mù → tech debt. D pause → trễ sprint. C chủ động unblock với dev (người available), document, vẫn loop PO bằng async — đúng tinh thần Agile.

**Đáp án: C** — Quick alignment với dev, document, share với PO, vẫn tiếp tục progress.

---

## Q3 — Startup AI văn hóa self-directed, framework mới

**Original question:**
> *Passage:* You are an intern at a fast-growing AI startup that values learning agility, self-directed research, and the ability to quickly adopt emerging technologies with minimal supervision. The company encourages interns to proactively explore new tools and frameworks, share insights with the team, and take initiative rather than wait for structured guidance. During your internship, a new open-source AI framework gains traction in the industry, and your team is considering whether to adopt it for an upcoming project. However, no one has been assigned to evaluate it, and your manager is busy with tight deadlines.
> *Question:* What would you most appropriately do to align with the company's culture?
> A. Briefly read about the framework from online sources and mention it in a team discussion, without conducting deeper investigation or validating its relevance through hands-on experimentation.
> B. Independently explore the new framework, build a small prototype to test its relevance, and share a concise summary of findings and recommendations with the team.
> C. Focus entirely on your current assigned tasks to ensure delivery and avoid overstepping your role, deliberately ignoring opportunities to explore new tools that are not explicitly required.
> D. Wait for your manager to formally assign a task related to the new framework before investing time in learning it, prioritizing alignment with assigned responsibilities over proactive exploration and experimentation.

**Phân tích:** Đề bài liệt kê đúng các keyword văn hóa: "self-directed research", "proactively explore", "take initiative rather than wait". A là half-effort (chỉ đọc). C, D đều ngược culture. B là full loop: hands-on prototype + share findings → fit nhất.

**Đáp án: B** — Independently explore, build small prototype, share concise findings.

---

## Q4 — Teammate xây giải pháp tương tự không tương thích

**Original question:**
> *Passage:* You are an AI intern integrating a machine learning model into an internal product. Midway through development, you discover that another teammate has independently built a similar solution using a different architecture and data pipeline. Both implementations partially solve the problem but are not fully compatible, and merging them would require changes from both sides. The team is under tight deadlines, and leadership has not yet decided which approach to prioritize. Your teammate is continuing to refine their version, while you are close to completing yours.
> *Question:* What is the most effective action you should take to ensure the best team outcome under these conditions?
> A. Initiate a focused discussion with your teammate to compare both approaches against project requirements, identify overlap and gaps, and collaboratively propose a short-term integration or decision plan to the team, balancing delivery timelines with technical alignment.
> B. Modify your solution to incorporate parts of your teammate's approach without discussion, aiming to produce a hybrid version quickly without validating compatibility or alignment.
> C. Continue finalizing your own implementation independently to ensure at least one complete solution is delivered on time, assuming alignment decisions can be deferred to leadership after the deadline.
> D. Pause your work entirely and wait for leadership to clarify ownership and direction before making further progress, avoiding potential rework at the cost of delivery speed.

**Phân tích:** "Best team outcome" + tight deadline + leadership chưa quyết. B (hybrid mù) có rủi ro tích hợp gãy. C ích kỷ, gây rework lớn. D thụ động, trễ deadline. A là phương án collaborative + có proposal cho team — vừa nhanh vừa technical.

**Đáp án: A** — Focused discussion, compare approaches, propose integration plan.

---

## Q6 — Fintech fraud detection 98% acc nhưng class imbalance

**Original question:**
> *Passage:* A fintech company is developing an AI-based fraud detection service for real-time payment processing. As an IT intern on the backend team, you are asked to help evaluate whether a newly trained model should be deployed. The dataset used is highly imbalanced (fraud cases are less than 1%). The model shows 98% overall accuracy during testing. However, initial analysis shows that some fraudulent transactions are still being missed, and there are concerns about customer experience if legitimate transactions are incorrectly flagged. The system must operate under low latency constraints and comply with banking regulations on transaction monitoring.
> *Question:* What is the most technically appropriate approach to evaluate and decide on deploying this AI model for business impact in this scenario?
> A. Evaluate the model solely based on ROC-AUC and overall benchmark comparisons, and proceed with deployment if it exceeds industry standards, without analyzing precision-recall trade-offs or class imbalance effects in real-world scenarios.
> B. Assess the model using precision-recall metrics and cost-sensitive evaluation, then simulate threshold tuning and run a shadow deployment to observe real-world fraud detection and false positive trade-offs before full rollout.
> C. Proceed with deployment based on the high overall accuracy and test results, assuming the model generalizes well, and plan to monitor performance after rollout without conducting segment-level analysis or evaluating fraud detection trade-offs beforehand.
> D. Focus primarily on reducing latency by simplifying model complexity and optimizing real-time inference speed, without evaluating the impact on fraud detection performance, false negatives, or compliance requirements.

**Phân tích:** Class imbalance <1% → accuracy là metric mù; phải dùng precision/recall. Fintech regulated → cần shadow deployment để quan sát real-world impact trước khi rollout. A bỏ qua imbalance, C deploy mù, D tối ưu sai metric. B đầy đủ: cost-sensitive + threshold tuning + shadow deploy.

**Đáp án: B** — Precision-recall + cost-sensitive eval + threshold tuning + shadow deployment.

---

## Q9 — API latency spikes, structured experimentation culture

**Original question:**
> *Passage:* You are an intern in an AI engineering team working on an API that recently started experiencing intermittent latency spikes. Senior engineers suspect a database query inefficiency, but no clear root cause has been identified. You are asked to assist by investigating the issue. The system has logging enabled, access to query execution plans, and a staging environment where controlled tests can be run. The team emphasizes the importance of structured experimentation and documenting findings to avoid assumptions.
> *Question:* What is the most appropriate approach you should take to investigate and help resolve the latency issue?
> A. Wait for senior engineers to complete their investigation and only assist once they provide explicit instructions, avoiding independent hypothesis testing or structured analysis to prevent making incorrect assumptions.
> B. Rely on intuition and past experience to identify likely causes such as scaling limitations or cache inefficiency, then recommend infrastructure upgrades and caching strategies without validating assumptions through controlled experiments or log-based analysis.
> C. Immediately optimize a complex query by refactoring joins, adding indexes, and deploy changes directly to production to test improvements in real traffic, without isolating variables or validating the root cause in a controlled staging environment first.
> D. Formulate a hypothesis about possible causes (e.g., slow queries), design controlled experiments in the staging environment to isolate variables, analyze query execution plans and logs, and document each finding systematically before suggesting optimizations.

**Phân tích:** Đề bài cho rõ "structured experimentation" + có sẵn staging + query plans + logs. A thụ động. B đoán mò. C deploy thẳng prod là cấm kỵ. D dùng đủ resource sẵn có theo đúng method.

**Đáp án: D** — Hypothesis → controlled experiment in staging → analyze plans/logs → document.

---

## Q10 — AI-first culture, prototype mới vs refining model cũ

**Original question:**
> *Passage:* You are an intern at an AI startup that emphasizes an AI-first, experimentation-driven culture. The company values rapid prototyping, data-informed iteration, openness to failure as a learning tool, and proactive knowledge sharing. Interns are encouraged to challenge assumptions and contribute ideas, even if they are not fully formed, as long as they are grounded in evidence or testing. You are assigned to a team working on improving a recommendation model. You notice a potential improvement using a newer algorithm, but it has not yet been tested within the company. Your team is currently focused on refining the existing model to meet a tight deadline.
> *Question:* What is the most appropriate action to take that best aligns with the company's AI-first and innovation-driven culture?
> A. Quickly prototype the new algorithm on a subset of data, document your findings, and share results with the team to evaluate its potential alongside current work.
> B. Continue refining the existing model only, assuming introducing new ideas could disrupt workflow and avoiding experimentation despite the team's AI-first culture.
> C. Wait until the current project deadline is over before introducing the idea, unnecessarily delaying experimentation and missing opportunities for parallel validation of improvements.
> D. Immediately push for replacing the current model without validation, incorrectly assuming external research guarantees superiority without internal testing.

**Phân tích:** "Grounded in evidence or testing" + AI-first → small-scale prototype để có data trước khi đề xuất. B/C ngược culture. D push không validation → reckless.

**Đáp án: A** — Quickly prototype on subset, document, share with team.

---

## Q12 — Identified improvement, manager bận, không deadline

**Original question:**
> *Passage:* You are an intern at an AI-driven company that prioritizes rapid experimentation, data-informed decisions, and continuous learning. The culture encourages employees to prototype quickly, validate ideas using real user data, and openly share learnings — even from failed attempts. Perfection is considered less valuable than iteration speed and insight generation. During your internship, you identify a potential improvement but are unsure if it will significantly enhance performance. Your manager is busy, and there is no immediate deadline.
> *Question:* What is the most appropriate action to take in this situation to align with the company's AI-first and innovation-driven culture?
> A. Spend excessive time refining the idea before testing, incorrectly prioritizing theoretical optimization over rapid experimentation and early feedback.
> B. Decide not to pursue the idea due to uncertainty, incorrectly assuming only fully validated improvements are worth exploring in an experimentation-driven environment.
> C. Build a simple prototype of the improvement, test it with a small dataset or user sample, and document and share the results with the team for feedback.
> D. Wait for managerial approval before taking any action, avoiding initiative despite the culture encouraging independent experimentation and learning.

**Phân tích:** "Iteration speed > perfection" + không có deadline ép → nên prototype ngay. A trì hoãn dạng cầu toàn. B từ bỏ. D thụ động. C đúng cycle: build → test → document → share.

**Đáp án: C** — Build simple prototype, test on small dataset, document, share.

---

## Q13 — Model mới unstable trong production, team disagree về root cause

**Original question:**
> *Passage:* You are an AI intern working on an internal prediction model used by multiple business teams. You recently implemented a new modeling approach from a research paper that significantly improved performance on validation datasets. However, when deployed on live production data, the model exhibits instability, including fluctuating predictions and occasional extreme outputs. Logs show no overt data drift, and team members disagree on whether the issue is due to implementation, data mismatch, or inherent model sensitivity. You are expected to both improve the model and demonstrate sound technical judgment while continuing to learn from this situation.
> *Question:* Given the conflicting signals between experimental success and production instability, what is the most technically appropriate next step to refine your understanding and improve the model?
> A. Adopt an ensemble of the new and old models to smooth out instability, assuming averaging predictions will improve robustness, without diagnosing the root cause or understanding failure modes under production conditions.
> B. Tune hyperparameters of the new model only, assuming the root cause is suboptimal configuration without validating behavior on production-like data.
> C. Roll back to the previous stable model immediately and avoid validating the new approach until more documentation or external validation becomes available, without investigating whether instability is due to data mismatch, implementation issues, or model sensitivity.
> D. Design controlled experiments to isolate sources of instability by comparing the new model and baseline across segmented production-like data (e.g., distribution shifts, edge cases), while instrumenting prediction variance and input sensitivity to identify failure modes before deciding on modifications.

**Phân tích:** Team disagree giữa 3 nguyên nhân (impl/data/sensitivity) → phải có experiment để phân biệt. A patch (ensemble) che vấn đề. B đoán mò. C trốn việc. D dùng segmentation + instrumentation đúng nghĩa root cause analysis.

**Đáp án: D** — Controlled experiments isolate sources of instability across segmented data.

---

## Q16 — Documentation review về DB optimization papers

**Original question:**
> *Passage:* An AI engineering team at a mid-sized SaaS company conducted a review of several research papers on database optimization techniques. The intern assigned to summarize the findings noted that while most papers emphasized performance improvements through indexing and caching, a few highlighted the trade-offs in maintainability and system complexity. The team recommended adopting aggressive caching strategies across all services, arguing that performance gains were consistently prioritized in the literature. However, a senior engineer countered that the summary overlooked important nuances discussed in the research, particularly regarding long-term system scalability and debugging challenges. The team plans to revise the documentation before presenting it to stakeholders.
> *Question:* Which of the following best identifies the issue in the intern's documentation approach?
> A. It overgeneralizes the research findings by prioritizing performance gains without adequately considering the documented trade-offs.
> B. It incorrectly assumes that caching and indexing were universally applied across all reviewed papers, overextending conclusions beyond what was explicitly discussed.
> C. It fails to incorporate critical trade-offs related to maintainability and system complexity, focusing only on performance improvements discussed in the literature.
> D. It incorrectly suggests avoiding indexing techniques despite their consistent emphasis in the literature, contradicting the core findings of the research.

**Phân tích:** Senior engineer cụ thể nói: "summary overlooked important nuances discussed in research, particularly regarding long-term system scalability and debugging challenges". Đây chính là trade-off về maintainability/complexity → C khớp 1-1. A đúng nhưng general hơn. D sai logic (intern không suggest avoiding indexing). C cụ thể nhất với feedback của senior.

**Đáp án: C** — Fails to incorporate critical trade-offs related to maintainability and system complexity.

> *Note:* A và C khá gần. Nếu phải chọn 1, C cụ thể hơn vì match trực tiếp với "long-term system scalability and debugging challenges" mà senior engineer nêu.

---

## Q18 — Vendor AI fraud detection, recall 60% / FP 8%

**Original question:**
> *Passage:* A fintech company is evaluating an AI-based fraud detection service to integrate into its backend transaction processing system. The vendor claims a 98% accuracy rate using a pre-trained model. During a pilot, the intern team observes that while overall accuracy is high, the model flags only 60% of fraudulent transactions (recall) and incorrectly blocks 8% of legitimate transactions (false positive rate). The business team is concerned about customer experience and regulatory compliance, especially regarding missed fraud cases and unnecessary transaction declines.
> *Question:* As an IT intern asked to recommend whether to proceed with this AI solution, what is the most technically appropriate action based on AI-first thinking and fintech risk considerations?
> A. Recommend further evaluation focusing on recall and false positive trade-offs, including threshold tuning and cost-sensitive metrics aligned with fraud risk and customer impact before deployment.
> B. Deploy the model as-is and rely on manual review of flagged transactions later, without tuning thresholds or validating whether the system meets regulatory and business requirements.
> C. Approve the solution based on high overall accuracy and vendor validation, without evaluating recall performance or false positive trade-offs relevant to fraud risk and customer impact.
> D. Reject the solution solely because the false positive rate is non-zero, without analyzing acceptable thresholds or balancing fraud detection effectiveness with user experience.

**Phân tích:** Recall 60% nghĩa là bỏ sót 40% fraud → cao rủi ro compliance. FP 8% → customer impact. Phải tune threshold + chọn cost-sensitive metric phản ánh chi phí thực. B/C deploy mù. D reject cứng nhắc, không đánh giá threshold.

**Đáp án: A** — Further evaluation: recall + FP trade-offs + threshold tuning + cost-sensitive metrics.

---

## Q19 — Model X (98%, edge weak) vs Model Y (92%, recall rare + explainable)

**Original question:**
> *Passage:* A fintech startup is building a backend fraud detection system for real-time payment transactions. As an IT intern, you are part of a team evaluating two AI-based solutions. Model X has higher overall accuracy (98%) but was trained on a limited dataset with low representation of edge-case fraud scenarios. Model Y has slightly lower overall accuracy (92%) but demonstrates better recall for rare fraud patterns and provides explainable outputs for each flagged transaction. The business operates in a regulated banking environment where false negatives (missed fraud) carry high financial and compliance risk. The system must also support auditability for regulatory recommendation for selecting an AI solution in this scenario?
> A. Recommend Model Y because its higher recall on rare fraud cases and explainability better align with regulatory requirements and the high cost of missed fraud in banking systems.
> B. Recommend Model X based on higher overall accuracy, without evaluating performance on rare fraud cases or considering the cost of false negatives in a regulated environment.
> C. Deploy both models in parallel assuming that combining their outputs will improve detection rates, without evaluating conflicts, calibration, or operational complexity.
> D. Select Model X and rely on manual review to handle missed fraud cases, without addressing model limitations or ensuring scalability and regulatory compliance.

**Phân tích:** Trong regulated banking: (1) missed fraud cost > overall accuracy, (2) auditability bắt buộc → cần explainability. Model Y match cả hai. Model X yếu edge case → bị tình huống rare fraud xử tử. B/D chọn X là sai prior. C deploy parallel mù → ops complexity.

**Đáp án: A** — Recommend Model Y (recall rare fraud + explainability fit regulatory + missed fraud cost).

---

## Q20 — Deployment readiness document, validation vs inference

**Original question:**
> *Passage:* The deployment document distinguishes several stages that are often conflated. During validation, the model is assessed against a holdout dataset to ensure that design choices generalize beyond the training data; however, this step is explicitly described as an internal checkpoint rather than evidence of real-world performance. Evaluation, by contrast, is defined as a broader process that may include validation results but also incorporates post-deployment monitoring signals, user feedback, and drift analysis. The document cautions that strong validation metrics should not be interpreted as guarantees of downstream reliability, particularly when input distributions are expected to evolve.
> Similarly, the document differentiates inference from prediction. Inference refers to the operational act of running the model on incoming data within the production system, including preprocessing, model execution, and postprocessing steps. Prediction, however, is characterized as the model's output in response to a specific input instance. The text notes that failures in inference pipelines (e.g., data schema mismatches) may occur even when the underlying predictive model remains unchanged, leading to degraded system behavior without any alteration in prediction logic.
> Finally, the document emphasizes that deployment readiness is not established by any single metric or stage, but by the consistency between validation assumptions, evaluation signals, and the robustness of the inference pipeline under realistic conditions.
> *Question:* Which of the following statements is most consistent with the distinctions and cautions presented in the document?
> A. A model can show strong validation results yet still perform poorly after deployment if real-world conditions diverge from validation assumptions and the inference pipeline encounters issues.
> B. It incorrectly treats evaluation as a simple extension of validation, failing to account for post-deployment signals such as user feedback and data drift.
> C. If validation metrics remain stable, it incorrectly assumes inference behavior will also remain consistent, ignoring real-world system variability and deployment risks.
> D. It assumes that once inference runs correctly, deployment readiness is guaranteed, ignoring external signals and system-level uncertainties.

**Phân tích:** Câu B/C/D dùng từ "incorrectly" — đó là mô tả lỗi sai chứ không phải phát biểu được document support. A là phát biểu thuần khớp với 3 phần document: validation strong ≠ deployment ok khi (1) real-world diverges + (2) inference pipeline fail.

**Đáp án: A** — Strong validation results yet poor post-deployment if real-world diverges + inference pipeline issues.

---

## Q21 — AI-driven startup, manual script vs experimental AI tool

**Original question:**
> *Passage:* You are an intern at an AI-driven startup that emphasizes an AI-first culture. The company encourages rapid experimentation, learning from failure, and proactively integrating AI into workflows rather than relying on traditional approaches. Interns are expected to take initiative, question existing processes, and propose AI-based improvements. During a project, you notice that your team is manually processing large datasets using an older script, which is time-consuming but reliable. You recently explored a new AI tool that could automate much of this work, but it is still experimental and may require iteration.
> *Question:* What is the most appropriate action to take in this situation that best aligns with the company's AI-first and innovation-driven culture?
> A. Propose a small-scale pilot using the AI tool alongside the existing process, clearly outlining potential benefits and risks, and seek feedback from the team to iterate quickly.
> B. Wait until you have complete certainty about the tool's effectiveness before suggesting it, unnecessarily delaying feedback and iterative learning cycles.
> C. Replace the current process independently with the AI tool without informing the team, bypassing collaboration and risking misalignment with production constraints.
> D. Continue using the existing process exclusively, incorrectly assuming stability is more important than experimentation even in an AI-first, innovation-driven environment.

**Phân tích:** Tool experimental → không thể replace toàn bộ (loại C). AI-first → không thể wait (B) hoặc giữ status quo (D). A: pilot song song giữ reliability + thử nghiệm AI + có feedback loop → fit nhất.

**Đáp án: A** — Small-scale pilot alongside existing process, outline benefits/risks, seek team feedback.

---

## Q22 — Cross-functional thread về deploy recommendation model

**Original question:**
> *Passage:* In a cross-functional thread about deploying a new recommendation model, the product manager (PM) notes that "early user feedback is promising, though we should be careful not to over-index on a small beta group." An engineer responds that "from an infrastructure standpoint, we can support a gradual rollout, but a full launch this quarter might stretch reliability targets unless we simplify some components." A data scientist adds that "while the offline metrics are strong, we've seen similar patterns before where real-world drift reduces impact after a few weeks." Later, the PM suggests, "perhaps we frame this as an experiment tied to specific engagement goals," to which the engineer replies, "that would give us room to monitor system behavior without committing to full-scale guarantees." No one explicitly opposes deployment, but no one strongly advocates immediate full release either.
> *Question:* What is the most reasonable inference about the group's underlying consensus regarding deployment?
> A. They are implicitly aligning around a cautious, limited rollout framed as an experiment to manage both technical and performance uncertainties.
> B. They are preparing for full deployment immediately, incorrectly downplaying the risks and uncertainties discussed during the conversation.
> C. They are primarily concerned with infrastructure limitations and assume deployment should be delayed until all constraints are resolved.
> D. They are strongly divided, with no alignment, despite multiple signals suggesting convergence toward a controlled rollout.

**Phân tích:** Đọc kỹ sub-text: PM lo over-index small beta → cẩn trọng. Engineer chấp nhận gradual rollout. DS lo drift. PM đề xuất frame as experiment, engineer đồng ý. Không ai oppose, không ai push full → đó chính là consensus ngầm về limited rollout/experiment. B/C/D đều mâu thuẫn với signal trong thread.

**Đáp án: A** — Implicitly aligning around cautious, limited rollout framed as experiment.

---

## Q24 — Vendor fraud API, FP cao đặc biệt với new users

**Original question:**
> *Passage:* A fintech company is evaluating an AI-based fraud detection API to integrate into its backend payment processing system. The vendor claims a 98% accuracy rate based on their internal testing. During a pilot, your team observes that while overall accuracy is high, the model flags a large number of legitimate transactions as fraudulent, especially for new users with limited transaction history. This leads to increased customer complaints and transaction delays. The business team is concerned about customer experience, while the risk team prioritizes fraud prevention. As an intern on the backend engineering team, you are asked to recommend the next step before full deployment.
> *Question:* What is the most technically appropriate action to evaluate the AI solution's business impact before deciding on full deployment?
> A. Analyze precision and recall separately, especially false positive rates for different customer segments, and adjust thresholds or request model retraining based on these metrics.
> B. Proceed with deployment based on the high overall accuracy and vendor benchmarks, without analyzing false positives across segments or evaluating the impact on customer experience and transaction friction.
> C. Make the model stricter to reduce fraud cases further, without evaluating false positive impact across customer segments or balancing fraud prevention with customer experience metrics.
> D. Disable the AI model entirely and switch to manual fraud review processes to eliminate customer complaints, without assessing operational scalability, fraud risk exposure, or long-term efficiency.

**Phân tích:** Đề bài flag rõ "especially for new users" → đòi hỏi segment-level analysis. A đúng vì có segment + threshold + retraining option. B deploy mù. C "stricter" sẽ làm FP tệ hơn. D bỏ AI là phá ROI.

**Đáp án: A** — Analyze precision/recall by segment, adjust thresholds or request retraining.

---

## Q27 — Internal tool prototype, edge cases inconsistent

**Original question:**
> *Passage:* You are an AI intern building an internal tool to automate parts of a business workflow. Your prototype demonstrates strong potential in standard scenarios but produces inconsistent outputs in certain edge cases. There is no formal policy on release readiness. Some team members advocate for releasing early to gather real-world feedback, while others emphasize the importance of reliability before exposure. The team culture values rapid experimentation, responsible deployment, and collaborative decision-making across stakeholders.
> *Question:* Given the team's culture of balancing experimentation with responsibility and collaboration, what is the most appropriate course of action?
> A. Release the prototype broadly to maximize feedback quickly, assuming real-world usage will naturally surface issues without structured monitoring or controlled experimentation safeguards.
> B. Delay the release until the prototype is fully stable across all edge cases, incorrectly prioritizing perfection over iterative validation and ignoring the team's emphasis on learning through controlled exposure.
> C. Independently refine the model further without sharing interim results, avoiding stakeholder input and delaying cross-functional learning despite the team's collaborative culture.
> D. Propose a limited pilot release to a small, informed user group, clearly communicate known limitations, implement monitoring for edge cases, and invite cross-functional feedback to guide iterative improvements.

**Phân tích:** "Balancing experimentation + responsibility + collaboration" — câu trả lời phải có cả ba. A chỉ experimentation. B chỉ responsibility. C bỏ collaboration. D đầy đủ: limited pilot (experiment) + monitoring + comm limitations (responsibility) + cross-functional feedback (collaboration).

**Đáp án: D** — Limited pilot + communicate limitations + monitoring + cross-functional feedback.

---

## Q28 — Rule-based system vs AI approach, tight deadlines

**Original question:**
> *Passage:* You are an AI intern at a fast-growing AI startup that emphasizes an AI-first, experimentation-driven culture. The company values rapid prototyping, learning from failure, and proactively exploring how AI can enhance every product feature. Interns are encouraged to question existing approaches, test new ideas quickly, and share learnings openly, even if results are imperfect. During a team meeting, you notice that a current feature relies on a traditional rule-based system that seems inefficient compared to newer AI-driven approaches you recently studied. However, the team is under tight deadlines, and no one has proposed changes to this feature yet.
> *Question:* What is the most appropriate action you should take to align with the company's culture?
> A. Quickly build a small prototype using an AI-based approach in your own time, then share the results with the team to spark discussion about potential improvements.
> B. Continue following the existing rule-based system strictly to ensure stability and avoid disrupting the current workflow, without exploring potential improvements using AI-based approaches.
> C. Wait until after the deadline to suggest replacing the system with an AI-based solution, avoiding immediate experimentation to reduce delivery pressure.
> D. Inform your manager that the current system should be replaced with an AI solution immediately, without building a prototype or validating feasibility through experimentation.

**Phân tích:** Tight deadline → không thể disrupt sprint hiện tại. AI-first → vẫn cần proactive. A là solution: prototype "in your own time" để không cản team + share để spark discussion → win-win.

**Đáp án: A** — Build small prototype in own time, share results to spark discussion.

---

## Q29 — Open-source AI framework gains attention

**Original question:**
> *Passage:* You are an intern at an AI startup that values learning agility, self-directed research, and the ability to quickly adapt to emerging technologies. The company encourages employees to experiment with new tools, independently explore solutions, and share insights with the team. During your internship, a new open-source AI framework gains attention in the industry. Your team has not yet adopted it, but leadership has expressed interest in staying ahead of trends.
> *Question:* What is the most appropriate action to take that aligns with the company's culture?
> A. Independently explore the new framework, build a small prototype to test its relevance, and share your findings and recommendations with the team.
> B. Wait for your manager to formally assign a task related to the new framework before investing time in exploring it, prioritizing alignment with assigned work over proactive learning and experimentation.
> C. Focus only on your current assigned tasks to ensure delivery and avoid potential distraction, deliberately ignoring opportunities to explore new tools that are not explicitly required.
> D. Briefly review documentation about the framework and suggest that the team adopt it, without building a prototype or validating its relevance through hands-on experimentation.

**Phân tích:** Tương tự Q3. Self-directed + leadership đã interest → nên proactive prototype + share. B/C ngược culture. D suggest mà chưa validate hands-on là half-effort.

**Đáp án: A** — Independently explore, build small prototype, share findings/recommendations.

---

## Q30 — Sprint, model output format đổi, dev/PO chưa biết

**Original question:**
> *Passage:* You are an intern working on an AI-powered recommendation feature in an Agile team. The team includes developers, a product owner (PO), and a data science team. During the sprint, you notice that the model output format recently changed by the data science team, which is causing integration issues with the frontend. The developers are continuing their work based on the old format, while the PO is unaware of the issue and pushing for sprint completion. There is limited time left before the sprint review, and no one has formally addressed the mismatch.
> *Question:* What is the most effective action you should take to support teamwork and project alignment?
> A. Proactively inform both the developers and the product owner about the mismatch, suggest a quick sync with the data science team, and help clarify the updated format so the team can realign before the sprint review.
> B. Focus on completing your assigned tasks and assume the developers or product owner will eventually notice and resolve the mismatch, avoiding proactive communication to prevent disrupting the workflow.
> C. Wait until the sprint review to highlight the mismatch issue, assuming it may not significantly impact the demonstration and can be addressed later without immediate coordination.
> D. Directly message the data science team to revert the format change without informing your immediate team, assuming this will quickly resolve the issue without requiring broader alignment.

**Phân tích:** Issue cross-team (frontend dev + DS team), PO không aware, deadline gấp. Cần cross-functional align ngay. B/C thụ động → vỡ sprint review. D đi ngang qua đầu PO/dev → phá process. A bao trùm cả 3 stakeholder.

**Đáp án: A** — Inform devs + PO, suggest sync với DS team, clarify format.

---

## Q31 — Documentation về DB scalability, team yêu cầu connect to company context

**Original question:**
> *Passage:* An AI engineering intern at a cloud services company reviewed several technical papers on database scalability and documented the findings for the internal team. The intern noted that while horizontal scaling improves availability, it often introduces complexity in data consistency. In presenting the findings to senior developers, the intern emphasized trade-offs rather than recommending a single approach. Feedback from the team highlighted that the documentation was clear but could better connect theoretical insights to the company's existing infrastructure constraints. The intern plans to revise the document accordingly before sharing it with stakeholders.
> *Question:* Which of the following best reflects an appropriate revision the intern should make based on the feedback?
> A. Expand theoretical explanations of scaling techniques without grounding them in real system constraints, making the document less practical and actionable.
> B. Focus on recommending a single scalability approach, ignoring trade-offs and reducing the quality of architectural decision-making.
> C. Incorporate specific examples showing how the discussed scalability trade-offs apply to the company's current systems and limitations.
> D. Remove discussion of trade-offs to simplify communication, incorrectly assuming stakeholders do not need to understand system limitations.

**Phân tích:** Feedback nguyên văn: "could better connect theoretical insights to the company's existing infrastructure constraints" → đúng nghĩa là incorporate specific examples linking trade-offs to company systems. Đó chính là C.

**Đáp án: C** — Incorporate specific examples of trade-offs applied to company's current systems.

---

## Q32 — Intern đánh giá paper về caching strategy

**Original question:**
> *Passage:* An AI engineering intern at a mid-sized SaaS company was assigned to evaluate a recently published technical paper proposing a new caching strategy for distributed systems. The intern summarized the paper's methodology, highlighted its assumptions about traffic patterns, and compared it with the company's current implementation in internal documentation. During a team meeting, the intern explained that while the paper showed performance improvements in controlled environments, its results depended heavily on stable request distributions, which might not reflect the company's real-world usage. The intern recommended conducting a limited internal experiment before adopting the approach and documented potential risks, including cache invalidation complexity and increased memory overhead.
> *Question:* Which of the following statements is best supported by the passage?
> A. The intern critically evaluated the research and communicated both its potential benefits and its limitations in a practical business context.
> B. The intern concluded that immediate adoption was appropriate, incorrectly assuming experimental results fully translate to production performance.
> C. The intern rejected the research entirely, ignoring its potential value despite acknowledging its limitations.
> D. The intern focused only on summarizing the paper's findings without connecting them to the company's system context or constraints.

**Phân tích:** Passage liệt kê đầy đủ: highlighted assumptions, compared with company's impl, mentioned both benefits (controlled env improvements) và limits (real-world drift, invalidation complexity, memory overhead), đề xuất limited experiment. Đây chính là critical evaluation. B sai (intern không recommend adoption). C sai (không reject). D sai (có connect to company).

**Đáp án: A** — Critically evaluated research, communicated benefits + limitations in business context.

---

## Pattern chung của bộ đề (rút ra để dùng cho các tình huống tương tự)

1. **Văn hóa AI-first + experimentation:** chọn **prototype nhỏ + document + share team**, KHÔNG chờ approval, KHÔNG bỏ qua, KHÔNG thay thế độc lập.
2. **Root cause / debugging:** **instrument → hypothesis → controlled experiment → document**, KHÔNG patch (ensemble, scale up, hyperparam tuning) trước diagnose.
3. **Fintech / regulated domain:** **precision-recall theo segment + cost-sensitive metric + threshold tuning + shadow deploy**, KHÔNG dùng accuracy tổng.
4. **Deployment readiness:** validation tốt ≠ production-ready; phải account for drift + real-world distribution + inference pipeline robustness.
5. **Communication / teamwork:** **proactive sync + document + cross-functional feedback** thắng "đợi", "escalate ngay", "tự quyết một mình".
6. **Documentation review:** giá trị nằm ở **trade-offs cụ thể + connect to company context**, không phải tóm tắt một chiều.

## TODO tiếp theo
- [ ] Phần code 10 câu: Q5 (select_model), Q7 (clean_predictions), Q8 (get_stable_models), Q11 (calculate_model_costs), Q14 (evaluate_model), Q15 (analyze_model_logs), Q17 (evaluate_model precision/recall/macro_f1), Q23 (evaluate_model logits→accuracy), Q25 (aggregate_tokens), Q26 (compute_avg_response_time).
