# AI / Deep Learning — Log

Chronological record of ingests, lint passes, and major edits. Append-only.

Tip: `grep "^## \[" log.md | tail -5` shows the five most recent entries.

---

## [2026-04-22] bootstrap | wiki scaffolding created

- Created: `CLAUDE.md`, `index.md`, `log.md`, `raw/`, `raw/assets/`
- Cataloged 58 existing concept notes into 14 topic clusters in `index.md`.
- Lint snapshot captured in `CLAUDE.md` and `index.md`:
  - 1 empty note: `transformer.md`
  - 3 stubs: `regularization.md`, `Decision Tree.md`, `Contrastive Learning Loss Functions.md`
  - 5 probable duplicate groups (Logistic Regression ×3, Linear Regression ×2, Word embedding ×3, Neural Network ×2, CNN ×2)
- No existing notes modified. Legacy format preserved.
- Key takeaway: wiki layer is now discoverable. Next priorities per user: fill `transformer` stub, resolve duplicates, start ingesting sources into `raw/`.

## [2026-06-14] create | quantization, LoRA, QLoRA concept note

- Created: [[quantization_lora_qlora]] (new YAML format, VN body + EN terminology).
- Covers: byte/params memory math (inference vs training), precision (FP32/FP16/BF16), quantization (PTQ/QAT, LLM.int8/GPTQ/AWQ/NF4/GGUF), LoRA (low-rank ΔW=BA), QLoRA (NF4 + double quant + paged optimizers), decision tree.
- New index cluster #15 "LLM Efficiency & Fine-tuning". note_count 58 → 59.
- Cross-linked to [[Adamw and Adam (optimizer)]], [[Backpropagation]], [[Vanishing and Exploding Gradient]], [[transformer]], [[regularization]].
- Sources cited (not yet ingested to raw/): LoRA (Hu 2021), QLoRA (Dettmers 2023), LLM.int8 (Dettmers 2022), GPTQ (Frantar 2022), AWQ (Lin 2023).
