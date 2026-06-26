---
type: synthesis
created: 2026-06-17
updated: 2026-06-17
tags: [inference, deployment, mlops, onnx, tensorrt, vllm, quantization, serving, llm, roadmap]
aliases: [inference engineering, inference optimization, model serving, onnx, tensorrt, vllm, deployment roadmap]
---

# Inference Engineering — Lộ trình học & bản đồ khái niệm

Note tổng hợp cho câu hỏi *"muốn làm Inference Engineer thì học gì, theo thứ tự nào"*. Tập trung vào **deployment/inference** (chạy model nhanh, rẻ, ổn định trên production) — khác với train. Lộ trình được sắp riêng cho hoàn cảnh: phần cứng **Colab L4 (24GB) + WSL local**, ngân sách **$0**, đã có sẵn **Qwen 1.5B + pipeline TTT-SDPO** (xem [[quantization_lora_qlora]] cho nền memory/precision).

> TL;DR: Inference Engineer trả lời *"làm sao model chạy nhanh nhất, tốn ít tài nguyên nhất, chịu tải tốt nhất"*. Hai habit nền: **(1) đo trước khi tối ưu**, **(2) hiểu decode của LLM là memory-bound**. Mọi tool (KV cache, quantization, batching) đều tấn công vào nút thắt bộ nhớ đó.

---

## 0. Nguyên tắc nền — quan trọng hơn mọi tool

Hai thứ phân biệt người *hiểu* inference với người chỉ *chạy* tool:

1. **Đo trước khi tối ưu.** Không "cảm giác nó nhanh hơn". Phải đọc được:
   - `latency p50/p99` — độ trễ 1 request (median và đuôi).
   - `throughput` — số request/token xử lý được mỗi giây.
   - Với LLM: `TTFT` (time-to-first-token, do prefill) + `ITL` (inter-token latency, tokens/sec, do decode).

2. **Roofline: memory-bound vs compute-bound.** Insight cốt lõi: **giai đoạn decode của LLM bị nghẽn bởi băng thông bộ nhớ, không phải sức tính.** Mỗi token decode phải đọc lại toàn bộ weights từ VRAM nhưng chỉ làm 1 phép nhân nhỏ → GPU chờ bộ nhớ, không chờ compute. Hiểu chỗ này mới hiểu *vì sao*:
   - **KV cache** hiệu quả (không tính lại key/value cũ),
   - **quantization** hiệu quả (ít byte để đọc → đọc nhanh hơn),
   - **batching** hiệu quả (chia sẻ 1 lần đọc weights cho nhiều request).

---

## 1. Graph optimization cổ điển (Vision) — *làm lite*

Mục tiêu: đủ để *nói chuyện được* về ONNX/TensorRT trong phỏng vấn. Đừng sa đà.

**Phân biệt 3 thứ hay bị gộp:**

| Tên | Bản chất |
|---|---|
| **ONNX** | Định dạng file `.onnx` (chuẩn chung, cầu nối giữa các framework). Không tự chạy. |
| **ONNX Runtime (ORT)** | Engine *chạy* file ONNX. Có execution provider cho CPU / CUDA / TensorRT. Đây mới là thứ cạnh tranh ở tầng serving. |
| **TensorRT** | SDK của NVIDIA biên dịch model thành engine tối ưu cho 1 GPU cụ thể. **Chỉ chạy trên GPU NVIDIA.** ORT có thể gọi TensorRT làm backend. |

**TensorRT tối ưu bằng:** quantization (FP32→FP16/INT8), layer & tensor fusion (gộp tầng giảm I/O), kernel auto-tuning theo kiến trúc GPU.

| Học gì | Build gì | Verify |
|---|---|---|
| `PyTorch → ONNX` export; chạy bằng ORT | ResNet18 / YOLOv8n → ONNX → ORT | So FPS PyTorch vs ORT cùng input |
| PTQ (xem [[quantization_lora_qlora]]); TRT build engine FP16/INT8 | Build TRT engine từ ONNX | Bảng: accuracy giảm bao nhiêu vs FPS tăng bao nhiêu |

**Outcome CV:** "Quantize YOLOv8n FP32→INT8 qua TensorRT, ↑X% throughput, ↓Y% accuracy."

---

## 2. LLM inference — *làm sâu, vùng vàng*

Giá trị kép: vừa là kỹ năng inference engineer, vừa cắm thẳng vào thesis (Qwen 1.5B trên L4). Nền precision/quantization đã có ở [[quantization_lora_qlora]].

| Học gì | Build gì | Verify |
|---|---|---|
| **KV cache** — vì sao decode memory-bound | Tự implement KV cache cho 1 forward loop nhỏ | tokens/sec có vs không cache |
| Quantization LLM: GPTQ, AWQ, GGUF (llama.cpp) | Quantize Qwen 1.5B xuống 4-bit | VRAM giảm; perplexity còn giữ |
| **vLLM**: PagedAttention + continuous batching | Serve Qwen bằng vLLM trên L4 | Throughput batch=1 vs batch=N; quan sát TTFT |
| **Speculative decoding** | Model nhỏ làm drafter cho model lớn | Đo tăng tốc decode |

**Khái niệm cốt lõi:**
- **KV cache** — lưu key/value của token đã sinh để không tính lại; nguồn tốn VRAM thứ 2 sau weights, tăng tuyến tính theo độ dài context.
- **PagedAttention** (vLLM) — quản lý KV cache theo "page" như virtual memory của OS → giảm phân mảnh VRAM, cho phép batch lớn hơn.
- **Continuous batching** — ghép/tách request vào batch *động* theo từng step decode, thay vì chờ cả batch xong → throughput cao hơn nhiều static batching.
- **Speculative decoding** — model nhỏ (drafter) đoán trước k token, model lớn verify 1 lần → giảm số bước decode đắt đỏ.

**Liên hệ thesis:** TTT-SDPO phải *generate* nhiều lần để eval rồi update weight → đó là bài toán inference throughput thuần. Wrap phần generate bằng **vLLM** thay vì HF `.generate()` thì vòng lặp test-time nhanh hơn nhiều — cải tiến *thật* cho thesis, không phải bài tập.

---

## 3. Serving & hạ tầng — *đủ dùng cho CV*

| Học gì | Build gì |
|---|---|
| vLLM OpenAI-compatible server; dynamic batching | Endpoint `/v1/chat/completions`, gọi như API thật |
| Docker hóa | Đóng model + server thành 1 container |
| Monitoring: latency, GPU util, throughput | Log metrics, vẽ biểu đồ tải |

**Triton Inference Server** là "ông trùm" enterprise (đa model, đa framework, dynamic batching), nhưng với fresher thì **vLLM server là đủ** và phổ biến hơn ở startup VN. Để Triton lại sau.

---

## 4. Kernel (CUDA / Triton lang) — *chỉ khi muốn khác biệt mạnh*

Tầng sâu nhất, tốn thời gian nhất. **Fresher không cần.** Đụng tới nếu nhắm hẳn vị trí "performance/systems" và đã vững GĐ 1–3.

> Lưu ý dễ nhầm: **Triton language** = ngôn ngữ viết GPU kernel của OpenAI. **Triton Inference Server** = serving framework của NVIDIA. Trùng tên, khác hẳn nhau.

---

## Thứ tự ưu tiên (cho hoàn cảnh hiện tại)

```
Nền (đo + roofline)  →  GĐ2 LLM (sâu)  →  GĐ1 Vision (lite)  →  GĐ3 Serving  →  [GĐ4 nếu còn sức]
```

Đảo GĐ2 lên trước GĐ1 (khác lời khuyên mặc định) vì LLM là thứ đã có sẵn đồ chơi (Qwen + L4 + thesis) → ROI cao nhất, động lực tốt nhất.

---

## Tài nguyên lõi ($0)

- **MIT 6.5940 — TinyML & Efficient Deep Learning** (Han Song): chuẩn vàng cho quantization/pruning/distillation. Đủ phần lý thuyết tối ưu.
- **vLLM docs** + blog PagedAttention gốc.
- **llama.cpp** repo: chạy được cả trên CPU/WSL, tốt cho thí nghiệm quantization khi không có Colab.
- **TensorRT quick-start** + **ONNX Runtime docs**.
- Models: Qwen (đã có) + bất kỳ model nhỏ nào trên HuggingFace.

---

## Liên hệ

- [[quantization_lora_qlora]] — nền byte/params, precision, PTQ/QAT, GPTQ/AWQ/NF4/GGUF; là tiền đề cho GĐ1 & GĐ2.
- [[transformer]] — kiến trúc mà KV cache / attention optimization gắn vào.
- [[Attention Mechanism]] — nền để hiểu PagedAttention / flash attention.
- [[AI Engineering]] — workflow practitioner tổng quát, deployment là một mảnh.
- [[Creating ML pipeline from scratch]] — pipeline end-to-end mà inference là khâu cuối.

## Nguồn tham khảo (chưa ingest vào `raw/`)

- Kwon et al. 2023 — *Efficient Memory Management for LLM Serving with PagedAttention* (vLLM).
- Leviathan et al. 2023 — *Fast Inference from Transformers via Speculative Decoding*.
- NVIDIA TensorRT & Triton Inference Server docs.
- MIT 6.5940 (Song Han) — TinyML and Efficient Deep Learning Computing.
