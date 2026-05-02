---
tags:
  - pytorch
  - llm
  - flash-attention
  - kv-cache
  - lora
  - peft
created: 2026-05-02
---

# PyTorch LLM Techniques

## 1. Flash Attention

### Vấn đề với standard attention

Standard attention tính:

```
Attention(Q, K, V) = softmax(QKᵀ / √d) · V
```

Với sequence length `N` và hidden dim `d`:
- Ma trận `QKᵀ` có shape `[N, N]` → **O(N²) memory**
- Với N=4096, d=64: ma trận attention chiếm ~1GB VRAM chỉ cho 1 layer

Vấn đề sâu hơn: bottleneck không phải là FLOP mà là **memory bandwidth**. GPU phải:
1. Tính `QKᵀ` → ghi `[N,N]` ra HBM (High Bandwidth Memory)
2. Tính softmax → đọc lại `[N,N]` từ HBM
3. Nhân với V → đọc/ghi lại

→ Rất nhiều lần đọc/ghi HBM chậm dù GPU cores thực ra rảnh.

### Flash Attention: tiling + recomputation

**Ý tưởng cốt lõi:** chia Q, K, V thành các tile nhỏ vừa SRAM (on-chip, cực nhanh), tính attention từng tile mà không cần lưu toàn bộ `[N,N]` ra HBM.

```
HBM (chậm, lớn)          SRAM (nhanh, nhỏ)
─────────────────         ──────────────────
Q, K, V matrices   →→→   tile của Q, K, V
                          tính attention local
O (output)        ←←←    cộng dồn kết quả
```

**Trick softmax online:** softmax cần biết toàn bộ hàng để normalize. Flash Attention dùng thuật toán online softmax — cập nhật running max và sum khi scan qua từng tile, cho kết quả chính xác mà không cần lưu full matrix.

**Kết quả:**
- Memory: O(N²) → **O(N)** (không lưu attention matrix)
- Speed: 2–4x nhanh hơn standard attention trên A100
- Gradient: dùng **recomputation** — không lưu attention matrix cho backward, tính lại từ Q,K,V khi cần (tradeoff: thêm FLOP, nhưng tiết kiệm HBM read/write nhiều hơn)

### Dùng trong PyTorch

PyTorch 2.0+ tích hợp Flash Attention vào `scaled_dot_product_attention` (SDPA):

```python
import torch
import torch.nn.functional as F

# PyTorch tự chọn kernel tối ưu nhất (Flash Attention, xFormers, hoặc math)
output = F.scaled_dot_product_attention(
    query,          # [B, H, T, d]
    key,            # [B, H, S, d]
    value,          # [B, H, S, d]
    attn_mask=None,
    dropout_p=0.0,
    is_causal=True  # causal mask cho autoregressive LM
)
```

Xem kernel nào được chọn:

```python
with torch.backends.cuda.sdp_kernel(
    enable_flash=True,
    enable_math=False,
    enable_mem_efficient=False
):
    output = F.scaled_dot_product_attention(q, k, v, is_causal=True)
```

**Flash Attention 2 / 3** (thư viện riêng, nhanh hơn):

```python
from flash_attn import flash_attn_func

# Input phải là BF16 hoặc FP16
output = flash_attn_func(q, k, v, causal=True)
```

---

## 2. KV Cache

### Tại sao cần KV Cache

Trong autoregressive generation, mỗi token mới phải attend đến **tất cả token trước**:

```
Token 1: attend to []
Token 2: attend to [tok1]
Token 3: attend to [tok1, tok2]
Token 4: attend to [tok1, tok2, tok3]
...
```

Không có cache: mỗi bước phải tính lại K, V của tất cả token cũ → **O(N²) tổng FLOP** cho N token.

**Observation:** K và V của token cũ không đổi qua các bước → cache lại, chỉ tính K, V của token mới.

### Implement KV Cache từ đầu

```python
import torch
import torch.nn as nn

class CachedAttention(nn.Module):
    def __init__(self, d_model, n_heads):
        super().__init__()
        self.n_heads = n_heads
        self.d_head = d_model // n_heads
        self.qkv = nn.Linear(d_model, 3 * d_model)
        self.out = nn.Linear(d_model, d_model)

    def forward(self, x, kv_cache=None):
        B, T, C = x.shape
        H, D = self.n_heads, self.d_head

        # Tính Q, K, V cho token mới
        qkv = self.qkv(x).reshape(B, T, 3, H, D).permute(2, 0, 3, 1, 4)
        q, k, v = qkv[0], qkv[1], qkv[2]   # mỗi cái: [B, H, T, D]

        # Nối với cache từ bước trước
        if kv_cache is not None:
            past_k, past_v = kv_cache
            k = torch.cat([past_k, k], dim=2)   # [B, H, T_total, D]
            v = torch.cat([past_v, v], dim=2)

        # Lưu cache mới để trả về
        new_cache = (k, v)

        # Attention: q attend đến toàn bộ k, v (bao gồm cả past)
        scale = D ** -0.5
        attn = (q @ k.transpose(-2, -1)) * scale       # [B, H, T, T_total]
        attn = torch.softmax(attn, dim=-1)
        out = attn @ v                                  # [B, H, T, D]

        out = out.transpose(1, 2).reshape(B, T, C)
        return self.out(out), new_cache


# Sử dụng trong generation loop
model = CachedAttention(512, 8)
cache = None

for step in range(max_new_tokens):
    next_token_embed = embedding(next_token_id).unsqueeze(1)  # [B, 1, C]
    output, cache = model(next_token_embed, kv_cache=cache)
    next_token_id = sample(output)
```

### Memory của KV Cache

Mỗi layer lưu K và V với shape `[B, H, T, D]`:

```
Memory per layer = 2 (K,V) × B × H × T × D × bytes_per_element
```

Ví dụ Llama-3 8B (32 layers, H=32, D=128, BF16):
- Sequence 4096 tokens, batch 1:
  `2 × 1 × 32 × 4096 × 128 × 2 bytes = 67MB per layer × 32 = ~2GB`

→ KV Cache có thể chiếm lượng VRAM đáng kể, là lý do vLLM cần PagedAttention.

### Multi-Query Attention (MQA) & Grouped-Query Attention (GQA)

Reduce KV Cache size bằng cách chia sẻ K, V giữa nhiều query heads:

```
Standard MHA: Q=32 heads, K=32 heads, V=32 heads
MQA:          Q=32 heads, K=1 head,   V=1 head    → KV cache ÷ 32
GQA:          Q=32 heads, K=8 heads,  V=8 heads   → KV cache ÷ 4
```

Llama-3 dùng GQA. PyTorch SDPA hỗ trợ GQA natively:

```python
# K, V có ít head hơn Q — PyTorch tự repeat K, V khi cần
output = F.scaled_dot_product_attention(
    query,   # [B, 32, T, D]
    key,     # [B, 8, T, D]   ← ít head hơn
    value,   # [B, 8, T, D]
    is_causal=True
)
```

---

## 3. PEFT & LoRA

### Vấn đề: fine-tuning model lớn

Full fine-tuning LLM 7B tham số yêu cầu lưu gradient và optimizer states cho tất cả tham số:
- Weights: 7B × 2 bytes (BF16) = 14GB
- Gradients: 14GB
- Adam states (m, v): 28GB
- **Tổng: ~56GB** — không khả thi với GPU thông thường

### LoRA — Low-Rank Adaptation

**Giả thuyết:** khi fine-tune, weight update `ΔW` có **intrinsic low rank** — tức là chỉ cần không gian nhỏ để biểu diễn sự thay đổi cần thiết.

Thay vì học `ΔW ∈ R^{d×k}` trực tiếp, LoRA phân tách:

```
ΔW = B · A    (B ∈ R^{d×r}, A ∈ R^{r×k}, r << min(d,k))
```

Trong inference:
```
h = W₀x + ΔWx = W₀x + BAx
```

**Số tham số trainable:**
- Original: d × k (ví dụ: 4096 × 4096 = 16.7M)
- LoRA (r=8): d×r + r×k = 4096×8 + 8×4096 = 65K → giảm **256x**

### Implement LoRA từ đầu

```python
import torch
import torch.nn as nn
import math

class LoRALinear(nn.Module):
    def __init__(self, linear: nn.Linear, rank: int = 8, alpha: float = 16):
        super().__init__()
        d_out, d_in = linear.weight.shape

        self.weight = linear.weight   # giữ nguyên pretrained weight
        self.bias = linear.bias
        self.weight.requires_grad_(False)   # freeze

        # LoRA matrices
        self.lora_A = nn.Parameter(torch.empty(rank, d_in))
        self.lora_B = nn.Parameter(torch.zeros(d_out, rank))
        self.scale = alpha / rank

        # A init với Kaiming, B init về 0 → ΔW = 0 lúc đầu
        nn.init.kaiming_uniform_(self.lora_A, a=math.sqrt(5))

    def forward(self, x):
        base = x @ self.weight.T
        if self.bias is not None:
            base = base + self.bias
        lora_update = x @ self.lora_A.T @ self.lora_B.T
        return base + self.scale * lora_update


def inject_lora(model, rank=8, alpha=16, target_modules=("q_proj", "v_proj")):
    for name, module in model.named_modules():
        for target in target_modules:
            if name.endswith(target) and isinstance(module, nn.Linear):
                parent_name, child_name = name.rsplit(".", 1)
                parent = model.get_submodule(parent_name)
                setattr(parent, child_name, LoRALinear(module, rank, alpha))
    return model
```

### Dùng thư viện PEFT (Hugging Face)

```python
from peft import LoraConfig, get_peft_model, TaskType
from transformers import AutoModelForCausalLM

model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.1-8B")

config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    r=16,                    # rank
    lora_alpha=32,           # scaling factor
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    lora_dropout=0.05,
    bias="none",
)

model = get_peft_model(model, config)
model.print_trainable_parameters()
# trainable params: 20,971,520 || all params: 8,051,380,224 || trainable%: 0.26%
```

### Merge LoRA weights sau training

```python
# Khi deploy: merge B·A vào W để không thêm latency
merged_model = model.merge_and_unload()
# Bây giờ merged_model là model thường, không có LoRA overhead
```

### QLoRA — LoRA + Quantization

Fine-tune model 4-bit quantized + LoRA adapters FP16 → train 65B model trên 1x A100 80GB:

```python
from transformers import BitsAndBytesConfig

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",      # NormalFloat4
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True, # nested quantization
)

model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.1-70B",
    quantization_config=bnb_config,
    device_map="auto"
)
# Sau đó inject LoRA như bình thường
```

---

## Tóm tắt

| Technique | Vấn đề giải quyết | Cơ chế |
|---|---|---|
| Flash Attention | O(N²) memory, bandwidth bottleneck | Tiling trên SRAM, không lưu attention matrix |
| KV Cache | Tính lại K,V cũ mỗi step | Cache K,V của token đã generate |
| GQA | KV Cache quá lớn | Nhiều Q heads chia sẻ 1 K,V head |
| LoRA | Full fine-tune quá tốn VRAM | Phân tách ΔW = BA, rank thấp |
| QLoRA | LoRA + VRAM hơn | 4-bit quantization cho base model |

---

## Liên kết

- [[PyTorch Autograd]]
- [[PyTorch Data Pipeline]]
- [[Attention Mechanism]]
- [[transformer]]
- [[vLLM]]
