- trong phần future work của bài báo gốc có nói về 1 hướng đi khá hay: *Long-horizon and agentic settings. RLRF is particularly appealing when trajectories are long or expose information about intermediate states. Evaluating SDPO in agentic environments is a natural next step.*
	- Nhưng để thực hiện được trong phạm vi bachelor thesis này thì rất khó và không khả thi, vì phải dev được một agentic environment with long trajectories, ví dụ:
		- "Input: một GitHub issue thực tế từ một repo Python lớn (django, sympy, scikit-learn, flask, ...) tại một commit cụ thể. Ví dụ: "Bug: when calling Model.objects.filter(x__in=qs), raises TypeError if qs is empty" 
		- Model phải: đọc cấu trúc repo → tìm đúng file chứa bug → đọc code xung quanh → suy luận root cause → edit đúng dòng → chạy test suite của repo → đọc failure → sửa tiếp → ... (có thể 20–100 tool calls trong một attempt)
		- Verifier: apply patch của model, chạy hidden test → pass/fail Một "attempt" = một trajectory dài với nhiều bước tool call, mỗi bước thay đổi state của filesystem"
		=> rất khó để làm trong 3 tháng 
- còn 1 approach khác dễ làm hơn và possible hơn là: *Behavioral differences in reasoning. We observed that SDPO induces qualitatively different reasoning patterns than GRPO, notably avoiding the latter’s tendency toward verbosity and superficial reasoning. Future work should systematically study how individual aspects, such as the reprompt template, influence behavior.*
Pipeline rõ ràng:
1. **Fork** lasgroup/SDPO, reproduce baseline §5 trên subset hard questions của LCBv6 (19 hard tasks: pass@64 < 0.5; 9 very hard: pass@64 < 0.03).
2. **Thiết kế ~5–8 template variants** dựa trên các trục ở bảng trên. Đây là contribution intellectual đầu tiên — tự tay bạn build taxonomy.
3. **Instrument code**: thêm logging vào rollout loop của SDPO để capture per-step:
    - Entropy của self-teacher distribution
    - Magnitude của advantage `A_SDPO = log(π(y|x,f)/π(y|x))` per token
    - Top-K logit overlap giữa teacher và student
    - Response length, "Hmm/Wait" filler count, code/reasoning ratio, edit distance từ attempt trước
4. **Chạy experiments**: với mỗi template × mỗi task × vài seeds → log đầy đủ.
5. **Phân tích định lượng**:
    - **Outcome metrics**: discovery@k, pass@k, **compute-to-correct (CTC)** — metric mới của bạn (đo wall-clock/FLOPs thay vì chỉ số attempts như paper)
    - **Behavior metrics**: response length, filler ratio, diversity giữa các attempts
    - **Teacher dynamics**: entropy curve, advantage distribution, teacher-student KL theo step
6. **Cross-tabulate**: template nào → behavior pattern nào → discovery outcome nào.
7. **Phân tích định tính**: chọn 3–5 case representative, đọc tay xem model thực sự generate gì step-by-step. So sánh template "verbose stack trace" vs "minimal error type" → model có reasoning khác nhau thế nào?
8. **Viết** thesis.

- ngoài ra, mở rộng thêm:
	-  **Đo cả self-teacher dynamics** (entropy, advantage distribution, teacher-student KL theo step) — không chỉ behavior bề mặt như length/filler. 
	- **Thêm metric CTC** (compute-to-correct, đo wall-clock/FLOPs) bên cạnh discovery@k. Paper chỉ đo theo số attempts, che mất chi phí compute thật.



[self-distillation-analysis - a beanie00 Collection](https://huggingface.co/collections/beanie00/self-distillation-analysis): Link trained checkpoint trên qwen3-8b và DeepSeek Distill 7B với GRPO và SDPO 
[Why Does Self-Distillation (Sometimes) Degrade the Reasoning Capability of LLMs?](https://beanie00.notion.site/why-does-self-distillation-degrade-reasoning)
