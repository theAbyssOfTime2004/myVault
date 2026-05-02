---
tags:
  - mlops
  - llm
  - inference
  - serving
  - performance
created: 2026-05-02
---

# vLLM

## Tổng quan

vLLM là một thư viện Python mã nguồn mở dành cho **LLM inference và serving**, được phát triển bởi UC Berkeley. Điểm nổi bật là throughput cao và memory efficiency nhờ kỹ thuật **PagedAttention**.

**Vấn đề vLLM giải quyết:** KV Cache trong transformer inference tiêu tốn rất nhiều VRAM và bị phân mảnh. vLLM quản lý KV Cache như một memory pager trong OS, loại bỏ lãng phí bộ nhớ.

---

## PagedAttention

Cơ chế cốt lõi của vLLM, lấy cảm hứng từ **virtual memory paging** trong OS.

**Vấn đề với KV Cache truyền thống:**
- KV Cache được cấp phát liên tục (contiguous) trong VRAM
- Phải dự trước `max_seq_len` → lãng phí khi sequence ngắn hơn
- Không thể chia sẻ KV Cache giữa các request (prefix sharing)

**Cách PagedAttention hoạt động:**
1. Chia KV Cache thành các **blocks** kích thước cố định (thường 16 tokens/block)
2. Các block không cần liên tục trong bộ nhớ vật lý
3. Mỗi sequence có một **block table** ánh xạ logical block → physical block
4. Blocks được cấp phát động theo nhu cầu thực tế

**Lợi ích:**
- Gần như 0% memory waste (chỉ tối đa ~4% fragmentation)
- Cho phép **copy-on-write** cho parallel sampling
- Prefix caching: các request cùng system prompt chia sẻ block

---

## Continuous Batching

**Static batching** (truyền thống): chờ tất cả request trong batch hoàn thành mới xử lý batch tiếp → GPU idle khi request ngắn hoàn thành sớm.

**Continuous batching** (iteration-level scheduling): sau mỗi forward pass, scheduler có thể:
- Thêm request mới vào batch ngay lập tức
- Loại bỏ request đã hoàn thành
- Preempt request để nhường chỗ cho request ưu tiên hơn

Kết quả: GPU utilization tăng đáng kể, latency trung bình giảm.

---

## Kiến trúc

```
Client
  │  (HTTP / Python SDK)
  ▼
AsyncLLMEngine
  │
  ├── Scheduler          ← quản lý hàng đợi, preemption
  │
  ├── BlockManager       ← PagedAttention, cấp phát KV blocks
  │
  └── Worker(s)
        └── ModelRunner  ← forward pass (CUDA kernels)
```

**Hai chế độ triển khai:**
- **Offline inference**: dùng class `LLM` trực tiếp trong Python
- **Online serving**: chạy server OpenAI-compatible API

---

## Tensor Parallelism & Pipeline Parallelism

| Loại | Mô tả | Khi dùng |
|---|---|---|
| Tensor Parallel | chia weight matrices theo chiều hidden dim | model không vừa 1 GPU |
| Pipeline Parallel | chia các layers giữa nhiều GPU/node | multi-node deployment |
| Data Parallel | nhiều engine instances độc lập | scale throughput |

---

## Các tính năng nổi bật

**Quantization:**
- GPTQ, AWQ, SqueezeLLM (weight-only)
- FP8 (Hopper GPUs, H100)
- GGUF support (thông qua llama.cpp backend)

**Speculative Decoding:**
- Dùng draft model nhỏ generate nhanh → target model verify song song
- Giảm latency (TTFT + TPOT) mà không đổi output quality

**Prefix Caching (Automatic Prefix Caching - APC):**
- Cache KV của prefix phổ biến (system prompt, few-shot examples)
- Reuse ngay khi request mới có cùng prefix

**Structured Output:**
- Tích hợp `outlines`/`lm-format-enforcer` → đảm bảo output theo JSON schema, regex

---

## Cài đặt & sử dụng cơ bản

```bash
pip install vllm
```

**Offline inference:**
```python
from vllm import LLM, SamplingParams

llm = LLM(model="meta-llama/Llama-3.1-8B-Instruct")
params = SamplingParams(temperature=0.8, max_tokens=512)

outputs = llm.generate(["Explain PagedAttention in simple terms"], params)
print(outputs[0].outputs[0].text)
```

**Online serving (OpenAI-compatible):**
```bash
vllm serve meta-llama/Llama-3.1-8B-Instruct \
  --tensor-parallel-size 2 \
  --gpu-memory-utilization 0.9 \
  --max-model-len 8192
```

```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:8000/v1", api_key="token")
response = client.chat.completions.create(
    model="meta-llama/Llama-3.1-8B-Instruct",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

---

## Metrics & Monitoring

vLLM expose Prometheus metrics tại `/metrics`:

| Metric | Ý nghĩa |
|---|---|
| `vllm:num_requests_running` | số request đang được xử lý |
| `vllm:gpu_cache_usage_perc` | % KV cache blocks đã dùng |
| `vllm:time_to_first_token_seconds` | TTFT distribution |
| `vllm:time_per_output_token_seconds` | TPOT (inter-token latency) |
| `vllm:request_success_total` | tổng request thành công |

---

## So sánh với các framework khác

| | vLLM | TGI (HuggingFace) | TensorRT-LLM |
|---|---|---|---|
| PagedAttention | có | có (v2) | không (static paging) |
| OpenAI API compat | có | có | không native |
| Quantization | GPTQ, AWQ, FP8 | GPTQ, AWQ | INT8, FP8, INT4 |
| Ease of use | cao | cao | thấp (build pipeline) |
| Throughput | cao | cao | rất cao (NVIDIA only) |
| Multi-node | có | có | có |

---

## Hạn chế

- Chủ yếu optimize cho NVIDIA GPU (AMD ROCm support còn hạn chế)
- CPU/Apple Silicon performance kém hơn llama.cpp
- Memory overhead của PagedAttention metadata có thể đáng kể ở batch nhỏ
- LoRA serving có overhead context-switching giữa adapter

---

## Liên kết

- [[Model Serving Patterns]]
- [[KServe - Extra Steps (Transformer và Inference Graph)]]

**Tài liệu:** https://docs.vllm.ai  
**Paper:** *Efficient Memory Management for Large Language Model Serving with PagedAttention* (Kwon et al., SOSP 2023)
