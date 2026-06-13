---
type: concept
created: 2026-06-14
updated: 2026-06-14
tags: [llm, quantization, lora, qlora, peft, fine-tuning, memory, efficiency]
aliases: [quantization, lora, qlora, peft, model memory, byte params, precision, fp16, bf16, int8, nf4]
---

# Quantization, LoRA & QLoRA — Bộ nhớ, độ chính xác, và fine-tuning tiết kiệm

Note tổng hợp mọi thứ liên quan tới câu hỏi *"model này cần bao nhiêu VRAM, và làm sao train/serve nó trên GPU nhỏ"*. Mạch chính: **params → bytes → precision → quantization → LoRA → QLoRA**.

> TL;DR: số params là cố định, thứ ta điều khiển được là **số byte trên mỗi param** (precision/quantization) và **số param cần update** (full fine-tune vs [[LoRA]]/[[QLoRA]]). Hai trục đó quyết định bài toán có vừa GPU hay không.

---

## 1. Byte / params — nền tảng tính bộ nhớ

Mỗi parameter (weight) là một con số được lưu theo một **dtype** (kiểu số). Bộ nhớ để chứa weights:

```
memory_weights = num_params × bytes_per_param
```

Quy đổi precision → byte:

| dtype | bits | bytes/param | ghi chú |
|---|---|---|---|
| FP32 (float32) | 32 | 4 | full precision, mặc định "chuẩn vàng" |
| FP16 (float16) | 16 | 2 | half precision |
| BF16 (bfloat16) | 16 | 2 | cùng exponent range FP32, ít mantissa hơn |
| FP8 | 8 | 1 | training/serving thế hệ mới (H100+) |
| INT8 | 8 | 1 | quantization phổ biến |
| INT4 / NF4 | 4 | 0.5 | quantization cực mạnh ([[QLoRA]] dùng NF4) |

**Rule of thumb để nhớ nhanh** (chỉ riêng weights):

| Precision | VRAM ≈ cho mỗi 1B params |
|---|---|
| FP32 | ~4 GB |
| FP16 / BF16 | ~2 GB |
| INT8 | ~1 GB |
| INT4 | ~0.5 GB |

Ví dụ: Llama 7B ở FP16 ≈ 7 × 2 = **14 GB** chỉ riêng weights. Cùng model ở INT4 ≈ 7 × 0.5 = **3.5 GB** → vừa được GPU consumer.

### Inference vs Training — đừng chỉ tính weights

Khi **inference** thì chủ yếu là weights + KV cache + activations (nhỏ). Khi **training** thì bộ nhớ phình ra nhiều lần vì còn:

| Thành phần | FP16 mixed-precision, optimizer Adam |
|---|---|
| Weights | 2 bytes/param |
| Gradients | 2 bytes/param |
| Optimizer state (Adam: m + v) | 8 bytes/param (2× FP32) |
| Master copy weights (FP32) | 4 bytes/param |
| **Tổng** | **~16 bytes/param** |

→ Full fine-tune 7B với Adam ≈ 7B × 16 ≈ **112 GB** chỉ cho model states (chưa tính activations). Đây chính là lý do [[LoRA]]/[[QLoRA]] tồn tại: cắt phần "16 bytes/param" này xuống gần như bằng 0 cho phần lớn weights. (Xem [[Adamw and Adam (optimizer)]] cho vì sao Adam tốn 2 state.)

Activations (cho backprop, xem [[Backpropagation]]) phụ thuộc batch size × sequence length × hidden size × num_layers, và giảm được bằng **gradient checkpointing** (đánh đổi compute lấy memory).

---

## 2. Numeric precision — FP32 / FP16 / BF16

Một floating point số = **sign (1 bit) + exponent (range) + mantissa (precision)**.

| dtype | exponent bits | mantissa bits | range | đặc điểm |
|---|---|---|---|---|
| FP32 | 8 | 23 | rộng | baseline |
| FP16 | 5 | 10 | hẹp | dễ overflow/underflow, cần loss scaling |
| BF16 | 8 | 7 | = FP32 | range rộng như FP32, ít chính xác hơn FP16 nhưng **ổn định khi train** |

**Key insight:** BF16 hi sinh độ chính xác (mantissa) để giữ **range** (exponent) bằng FP32. Với deep learning, range quan trọng hơn precision → BF16 là default cho training LLM hiện đại (tránh được vanishing/exploding khi giá trị quá nhỏ/lớn — liên quan [[Vanishing and Exploding Gradient]]).

**Mixed precision training:** forward/backward chạy FP16/BF16 (nhanh, ít RAM) nhưng giữ một **master copy FP32** của weights để update ổn định. Với FP16 cần **loss scaling** để gradient nhỏ không bị underflow về 0.

---

## 3. Quantization — nén weights xuống integer

**Quantization** = ánh xạ giá trị floating point (liên tục) về tập số rời rạc ít bit hơn (thường integer). Mục tiêu: giảm bộ nhớ + tăng tốc inference, đánh đổi một ít accuracy.

Công thức affine quantization cơ bản:

```
x_int  = round(x_float / scale) + zero_point
x_deq  = (x_int - zero_point) × scale     # dequantize
```

- `scale` (số thực): độ lớn mỗi bước lượng tử.
- `zero_point` (integer): ánh xạ số 0 thực sang miền integer (asymmetric). Symmetric thì zero_point = 0.
- Tính theo **block/group** (vd 64–128 weights chung 1 scale) → "group-wise quantization", giữ accuracy tốt hơn per-tensor.

### Phân loại

**Theo thời điểm:**

| Loại | Khi nào | Đặc điểm |
|---|---|---|
| **PTQ** (Post-Training Quantization) | sau khi train xong | nhanh, không cần train lại; có thể tụt accuracy |
| **QAT** (Quantization-Aware Training) | trong lúc train | mô phỏng quantization khi train → accuracy cao hơn, tốn compute |

**Theo cái gì được nén:**
- **Weight-only**: chỉ nén weights (W8, W4). Phổ biến nhất cho LLM vì memory-bound.
- **Weight + Activation**: nén cả activation (W8A8) → tăng tốc compute thật sự, nhưng khó hơn (activation có outlier).

### Các thuật toán/format hay gặp

| Tên | Bits | Ý tưởng cốt lõi |
|---|---|---|
| **bitsandbytes LLM.int8()** | 8 | tách outlier ra FP16, phần còn lại INT8 → gần như lossless |
| **GPTQ** | 4 (3/2) | PTQ dựa trên Hessian, quantize từng layer giảm thiểu lỗi reconstruction |
| **AWQ** (Activation-aware) | 4 | bảo vệ các weight "quan trọng" (theo activation magnitude) khỏi bị nén mạnh |
| **NF4** (NormalFloat4) | 4 | dtype 4-bit tối ưu cho weights phân phối chuẩn → dùng trong [[QLoRA]] |
| **GGUF / llama.cpp (Q4_K_M...)** | 2–8 | format quantize cho CPU/edge inference |

Trade-off chung: **càng ít bit → càng nhẹ/nhanh nhưng accuracy tụt**, nhất là dưới 4-bit. 8-bit gần như free; 4-bit là "sweet spot" hiện tại; 2–3 bit chỉ cho model rất lớn (lỗi tương đối nhỏ hơn).

---

## 4. LoRA — Low-Rank Adaptation

**Vấn đề:** full fine-tune update *toàn bộ* weights → tốn ~16 bytes/param (mục 1) và lưu nguyên một bản model cho mỗi task.

**Ý tưởng LoRA:** thay vì update ma trận weight `W ∈ ℝ^{d×k}` trực tiếp, **đóng băng W** và học một phần cập nhật **low-rank**:

```
W' = W + ΔW,   ΔW = B · A
A ∈ ℝ^{r×k},  B ∈ ℝ^{d×r},  với r ≪ min(d, k)
```

- Chỉ train `A` và `B` (rank `r` nhỏ, vd 8/16/32). `W` gốc giữ nguyên (frozen).
- Số param train giảm cực mạnh: từ `d×k` xuống `r×(d+k)`. Thực tế thường < **1%** số param.
- Forward: `h = Wx + (B·A)x · (α/r)`, với `α` là scaling factor (`lora_alpha`).
- Khi train xong có thể **merge** `B·A` vào `W` → inference không tốn thêm latency. Hoặc giữ riêng adapter để swap nhiều task trên cùng base model.

**Vì sao low-rank đủ?** Giả thuyết: việc thích nghi (adaptation) cho một downstream task nằm trong một **không gian con chiều thấp** — "intrinsic dimension" của task nhỏ.

**Hyperparams quan trọng:**

| Param | Vai trò | Giá trị thường dùng |
|---|---|---|
| `r` (rank) | dung lượng adapter | 8, 16, 32, 64 |
| `lora_alpha` (α) | scale của ΔW | thường = r hoặc 2r |
| `target_modules` | layer nào gắn LoRA | q_proj, k_proj, v_proj, o_proj (+ MLP) |
| `lora_dropout` | regularization | 0.05–0.1 |

LoRA thuộc họ **PEFT** (Parameter-Efficient Fine-Tuning), cùng nhóm với prefix tuning, prompt tuning, (IA)³, adapters. LoRA là cái thắng phổ biến nhất vì zero inference overhead sau merge.

**Lợi ích bộ nhớ:** vì chỉ `A`, `B` cần gradient + optimizer state, phần "16 bytes/param" giờ chỉ áp lên < 1% params. Base weights chỉ cần giữ ở dạng inference (2 bytes/param FP16). 7B model fine-tune được trên ~1 GPU 24 GB.

---

## 5. QLoRA — Quantized LoRA

**QLoRA = đóng băng base model ở 4-bit + train LoRA adapter ở trên.** Kết hợp mục 3 và mục 4 để fine-tune model lớn trên GPU consumer (vd 65B trên 1× 48 GB, 7B trên ~6–8 GB).

Ba đóng góp kỹ thuật chính:

1. **NF4 (4-bit NormalFloat)** — dtype 4-bit information-theoretically tối ưu cho weights có phân phối ~ chuẩn (mean 0). Base model được quantize xuống NF4 và **giữ frozen**.

2. **Double Quantization** — quantize luôn cả các *quantization constants* (scale) → tiết kiệm thêm ~0.4 bit/param.

3. **Paged Optimizers** — dùng NVIDIA unified memory để offload optimizer state sang CPU RAM khi VRAM spike (tránh OOM ở các batch dài).

**Cơ chế forward/backward:**
- Base weights lưu NF4 (frozen). Khi tính toán, chúng được **dequantize on-the-fly** về BF16 cho phép nhân ma trận.
- Gradient **chỉ** chảy vào LoRA adapter (BF16), không vào base. → base không cần gradient/optimizer state.
- Kết quả: chất lượng gần bằng full 16-bit fine-tune (paper báo cáo gần như không mất accuracy) nhưng VRAM giảm hàng chục lần.

**So sánh nhanh:**

| Tiêu chí | Full FT | LoRA | QLoRA |
|---|---|---|---|
| Base weights | FP16, trainable | FP16, frozen | **NF4 (4-bit), frozen** |
| Params được train | 100% | < 1% (adapter) | < 1% (adapter) |
| VRAM (7B, ước lượng) | ~112 GB+ | ~16–20 GB | **~6–10 GB** |
| Tốc độ train | nhanh nhất/step | nhanh | chậm hơn (do dequantize on-the-fly) |
| Accuracy | baseline | ~baseline | ~baseline (gần như không mất) |

**Lưu ý thực tế:** QLoRA chậm hơn LoRA mỗi step vì phải dequantize liên tục, nhưng đổi lại fit được model mà LoRA thường không fit nổi. Sau khi train, adapter (BF16) có thể merge vào base đã dequantize, hoặc giữ adapter nhỏ (vài chục MB) để phân phối.

---

## 6. Cây quyết định nhanh

- **Chỉ inference, GPU đủ lớn** → FP16/BF16, không cần quantize.
- **Inference, GPU nhỏ / nhiều request** → weight-only quantization (GPTQ/AWQ 4-bit, hoặc GGUF cho CPU/edge).
- **Fine-tune, base fit FP16 trong VRAM** → [[LoRA]].
- **Fine-tune, base KHÔNG fit FP16** → [[QLoRA]] (4-bit base + adapter).
- **Cần accuracy tuyệt đối, có cụm GPU** → full fine-tune (BF16 mixed precision).

---

## Liên hệ

- [[Adamw and Adam (optimizer)]] — vì sao optimizer state tốn 2× memory (m, v).
- [[Backpropagation]] — activations phải lưu để backward → nguồn tốn RAM khác.
- [[Vanishing and Exploding Gradient]] — lý do BF16 (range rộng) được ưa chuộng khi train.
- [[transformer]] — kiến trúc mà ta thường gắn LoRA vào (q/k/v/o projections).
- [[regularization]] — lora_dropout là một dạng regularization cho adapter.

## Nguồn tham khảo (chưa ingest vào `raw/`)

- Hu et al. 2021 — *LoRA: Low-Rank Adaptation of Large Language Models*.
- Dettmers et al. 2023 — *QLoRA: Efficient Finetuning of Quantized LLMs* (NF4, double quant, paged optimizers).
- Dettmers et al. 2022 — *LLM.int8()* (outlier-aware 8-bit).
- Frantar et al. 2022 — *GPTQ*. Lin et al. 2023 — *AWQ*.
