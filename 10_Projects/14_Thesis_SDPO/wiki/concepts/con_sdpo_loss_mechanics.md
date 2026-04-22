---
type: concept
created: 2026-04-23
updated: 2026-04-23
tags: [sdpo, loss, gradient, kl-divergence, math]
sources: [src_hubotter2026_self_distillation, src_lasgroup_sdpo_repo]
---

# SDPO loss mechanics — student match teacher distribution

Derivation kỹ thuật của cách student học match teacher distribution trong SDPO. Gom chi tiết toán học + code mapping về một chỗ để reference khi viết thesis methodology.

## Bước 1 — Distribution tại mỗi token

LLM sinh 1 token ở vị trí $t$ → output logits $z \in \mathbb{R}^V$ (V ≈ 150k vocab size). Softmax ra distribution:

$$\pi(v) = \frac{\exp(z_v)}{\sum_{v'} \exp(z_{v'})}$$

Hai distributions quan tâm tại cùng vị trí $t$:

- $\pi_S$ (**student**): model params $\theta$, prompt $= x$ (câu hỏi gốc)
- $\pi_T$ (**teacher**): cùng model (hoặc EMA version params $\theta_T$), prompt $= x + c$ với $c$ = feedback + successful demonstration

Teacher "nhìn thấy" $c$ → distribution dồn về token đúng hơn.

## Bước 2 — KL divergence giữa 2 distributions

$$D_{\text{KL}}(\pi_T \| \pi_S) = \sum_{v} \pi_T(v) \log \frac{\pi_T(v)}{\pi_S(v)}$$

SDPO loss = sum KL qua mọi token response:

$$\mathcal{L}(\theta) = \sum_{t=1}^{|y|} D_{\text{KL}}\big(\pi_T^{(t)} \,\|\, \pi_S^{(t)}\big)$$

Loss càng nhỏ ⇒ student càng giống teacher.

## Bước 3 — Gradient tại logit: công thức cốt lõi

Khai triển KL (forward direction làm ví dụ):

$$\mathcal{L}(\theta) = -\sum_v \pi_T(v) \log \pi_S(v \mid \theta) + \text{const}$$

Teacher `detach()` → const bỏ qua. Đạo hàm theo logit $z_v$ của student:

$$\boxed{\frac{\partial \mathcal{L}}{\partial z_v^S} = \pi_S(v) - \pi_T(v)}$$

**Đọc công thức**:
- $\pi_T(v) > \pi_S(v)$ (teacher tin token $v$ đúng hơn) → gradient âm → optimizer **tăng** $z_v$ → student probable hơn lần sau.
- $\pi_T(v) < \pi_S(v)$ → gradient dương → **giảm** $z_v$.

Qua nhiều AdamW step (LR=1e-5), logits student dịch dần về logits teacher.

## Bước 4 — So sánh density với GRPO

**GRPO gradient** (scalar reward $\hat{A}(y)$, 1 số cho cả câu):

$$\frac{\partial \mathcal{L}_{\text{GRPO}}}{\partial z_v^S} = \hat{A}(y) \cdot \big(\pi_S(v) - \underbrace{\mathbb{1}[v = y_t]}_{\text{one-hot}}\big)$$

Target là one-hot tại token đã sample. Mọi token trong câu share cùng $\hat{A}$.

| Method | Target per token | Info per sequence |
|---|---|---|
| GRPO | scalar × one-hot | $O(1)$ |
| SDPO sequence | scalar × soft dist | $O(1)$ |
| SDPO token | soft dist per token | $O(T)$ |
| **SDPO logit** | soft dist $V$ chiều per token | $O(T \cdot V)$ |

Paper dùng **top-K=100** + tail bucket → thực tế $O(T \cdot 101)$ (K=20 cho LCBv6).

## Bước 5 — Generalized JSD ($\alpha$ parametrization)

Code (`core_algos.py:1085`) parametrize qua $\alpha \in [0,1]$ với mixture $M = (1-\alpha)\pi_S + \alpha\pi_T$:

- $\alpha = 0$ → **forward KL** $D_{KL}(\pi_S \| \pi_T)$ — **mode-covering**, student cover mọi mode teacher, giữ được cả `wait/hmm/...`
- $\alpha = 1$ → **reverse KL** $D_{KL}(\pi_T \| \pi_S)$ — **mode-seeking**, student dồn vào mode lớn nhất, **dễ suppress epistemic tokens**
- $\alpha = 0.5$ → **JSD** $\frac{1}{2}D_{KL}(\pi_S\|M) + \frac{1}{2}D_{KL}(\pi_T\|M)$ — cân bằng (default)

**Thesis hypothesis**: $\alpha$ modulate suppression rate. LCBv6 rich-feedback dùng $\alpha = 1.0$ → dự đoán suppression mạnh nhất. Chưa ai test dimension này — new angle cho RQ2 (xem [[src_lasgroup_sdpo_repo]] insight #7).

Code (`core_algos.py` lines ~1145–1170):
```python
if alpha == 0.0:
    kl_loss = F.kl_div(student_logp, teacher_logp, reduction="none", log_target=True)
elif alpha == 1.0:
    kl_loss = F.kl_div(teacher_logp, student_logp, reduction="none", log_target=True)
else:
    mixture_logp = logsumexp(stack([student_logp + log(1-α), teacher_logp + log(α)]), dim=0)
    kl_teacher = F.kl_div(mixture_logp, teacher_logp, ...)
    kl_student = F.kl_div(mixture_logp, student_logp, ...)
    kl_loss = lerp(kl_student, kl_teacher, α)
```

## Bước 6 — Importance sampling correction

Student sample $y$ với params cũ $\theta_{\text{old}}$, loss tính với $\theta$ hiện tại. Cần IS ratio:

$$r_t(\theta) = \frac{\pi_\theta(y_t)}{\pi_{\theta_{\text{old}}}(y_t)}, \quad r_t \leftarrow \min(r_t, c_{\text{clip}})$$

với `is_clip = 2.0` (default). Per-token loss nhân $r_t$ clipped. Code:

```python
neg_approx_kl = (student_log_probs - old_log_probs).detach().clamp(-20, 20)
ratio = torch.exp(neg_approx_kl).clamp(max=is_clip)
per_token_loss = per_token_loss * ratio
```

## Bước 7 — Teacher update

Teacher params $\theta_T$ update qua EMA sau mỗi optimizer step:

$$\theta_T \leftarrow (1-\eta)\,\theta_T + \eta\,\theta_S$$

- $\eta = 0$ → teacher **đóng băng** ở base model (Kim 2026 recommend để tránh feedback loop).
- $\eta = 0.05$ → Hübotter default.
- $\eta = 0.01$ → LCBv6 rich-feedback config.

Teacher luôn `.detach()` → không nhận gradient. Xem [[con_self_teacher]] section "Teacher update regime".

Alternative: `trust-region` mode — teacher logits = `lerp(ref_logits, student_logits, μ)` thay vì EMA của weights.

## Top-K approximation (memory trade-off)

Full-vocab KL quá tốn memory với $V = 150k$. Paper dùng top-K=100 (hoặc K=20 cho LCBv6):

1. Lấy top-K logits của teacher theo value.
2. Renormalize thành distribution trên K+1 buckets (K + 1 tail bucket):

$$\text{tail}_T = 1 - \sum_{v \in \text{topK}} \pi_T(v)$$

3. Student project logits lên cùng K indices + tail.
4. KL tính trên (K+1)-dim distribution thay vì $V$-dim.

`distillation_add_tail=True` → dùng tail bucket. Nếu `False` → chỉ renormalize top-K, drop mass ngoài.

## Tóm tắt cơ chế học

Student học bằng cách **minimize KL với teacher distribution tại mỗi token**. Về gradient, optimizer chỉ làm một việc: push logit $z_v$ của student về phía logit teacher với lực tỷ lệ $\pi_T(v) - \pi_S(v)$.

Target là distribution $V$ chiều thay vì 1 scalar → **density per-token = $O(V)$ thay vì $O(1)$** → thông tin dày hơn $\sim T \cdot K$ lần so với GRPO, giải thích sample efficiency 3×–6× của SDPO ([[con_credit_assignment]]).

## Implications cho thesis

- **RQ1 (template)**: $c$ trong $\pi_T(\cdot | x, c)$ = control knob. Template format thay đổi nội dung $c$ → thay đổi $\pi_T$ → thay đổi target gradient direction. Đây là formal mechanism cho tại sao template matter.
- **RQ2 (suppression)**: $\alpha$ (KL direction) modulate mode-seeking vs mode-covering. Reverse KL mode-seeking có thể là root cause của suppression — ablation $\alpha \in \{0, 0.5, 1\}$ là ablation mới.
- **RQ2**: Fixed teacher ($\eta=0$) vs EMA — đã thảo luận trong [[con_self_teacher]], formalize ở đây qua update rule.
- **RQ3 (CTC)**: Memory cost per step $= O(T \cdot K)$ với K=100 → compute trade-off quantifiable.

## Links

- [[src_hubotter2026_self_distillation]] — §4.2 formal loss
- [[src_lasgroup_sdpo_repo]] — code references (`core_algos.py:1085`, `dp_actor._update_teacher`)
- [[con_credit_assignment]] — density comparison với GRPO
- [[con_self_teacher]] — teacher regularization regimes
- [[con_reprompt_template]] — $c$ là input của $\pi_T$
- [[con_uncertainty_suppression]] — $\alpha$ modulate suppression hypothesis
