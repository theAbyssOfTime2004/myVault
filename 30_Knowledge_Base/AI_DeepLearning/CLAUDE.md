# AI / Deep Learning — Wiki Schema

Context for Claude Code when working in `30_Knowledge_Base/AI_DeepLearning/`.

## Purpose

Personal knowledge base for AI / ML / DL concepts. Accumulates learning material from courses, papers, blogs, videos. Used as study reference, thesis background, and long-term second brain.

## Structure

```
AI_DeepLearning/
├── CLAUDE.md          # this file
├── index.md           # catalog of all notes, grouped by cluster
├── log.md             # chronological record
├── raw/               # NEW: source documents (papers, web clips)
│   └── assets/        # images (Ctrl+Shift+D)
└── <concept notes>.md # existing 58 flat notes (legacy format)
```

No subdirectories for concept notes yet — keep flat structure to preserve existing `[[wikilinks]]`. Add subdirectories only if the folder grows past ~150 notes.

## Two formats coexist

**Legacy format** (existing 58 notes, preserve as-is):
- Title Case file name: `Attention Mechanism.md`
- First line: `YYYY-MM-DD HH:MM`
- Second line: `Tags: [[tag1]], [[tag2]]`
- Body: free markdown with embedded `![[images]]` and `[[wikilinks]]`

**New format** (use for all new notes and full rewrites):
```yaml
---
type: concept | source | synthesis
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [nlp, attention]
sources: [src_vaswani2017_attention]   # if derived from ingested sources
aliases: [attention, self-attention]
---
```
Then body. Snake_case file name for new notes: `self_attention.md`.

**Do not force-migrate** legacy notes. Only touch format when the user asks or when doing a major rewrite.

## Workflows

### Ingest (new source added to `raw/`)

1. Read the source fully.
2. Discuss key takeaways with the user.
3. Create `raw/<source_file>.md` if not already there, or keep the clipped name.
4. Decide: which existing concept notes are affected? Which new ones are needed?
5. For each affected note:
   - Legacy note → add a new section at the bottom citing the source
   - New note → create in new YAML format with `sources: [...]` linking back
6. Cross-link with `[[WikiLinks]]` to related notes.
7. Update `index.md` — add new notes, update counts.
8. Append to `log.md`:
   ```
   ## [YYYY-MM-DD] ingest | <source short title>
   - Source: raw/<file>.md
   - Updated: [[Note A]], [[Note B]]
   - Created: [[New Note]]
   ```

### Query

1. Read `index.md` to locate the relevant cluster.
2. Read notes in that cluster + their linked notes.
3. Answer with citations as `[[Note Name]]` and, where applicable, `[[src_*]]`.
4. If the answer synthesizes multiple notes into a new insight, ask the user whether to file it as a new concept note.

### Lint

- **Stubs**: notes < 500 bytes — candidates for filling or merging
- **Empty**: notes at 0 bytes (e.g. `transformer.md`) — create full page
- **Duplicates**: multiple notes on the same topic (e.g. three Logistic Regression notes) — recommend merging
- **Orphans**: notes with no inbound `[[links]]` from other notes
- **Missing cross-refs**: note mentions a concept that has its own page but doesn't link to it
- **Language inconsistency**: same concept split across VN and EN notes

Output a report. Do not edit during lint.

## Rules

- **Never modify `raw/`.**
- Preserve legacy note format unless user approves rewrite.
- Every ingest: update `index.md` AND append `log.md`.
- Every new note: use YAML frontmatter + snake_case file name.
- Cross-link liberally — this vault's value is in the graph.

## Language convention

- **Note mới: body tiếng Việt**, code-switch sang English cho terminology (attention, backprop, gradient descent, embedding...), tên model, tên paper.
- **Note cũ**: giữ nguyên ngôn ngữ (đừng auto-translate). Chỉ Việt hóa khi user yêu cầu rewrite.
- **Metadata (YAML, log entries, file names): English** cho ổn định tooling.
- Không cứng nhắc — natural flow quan trọng hơn tỷ lệ VN/EN.

## Known issues (lint snapshot 2026-04-22)

**Empty / stubs to fill:**
- `transformer.md` (0 B) — critical gap, high priority
- `regularization.md` (129 B)
- `Decision Tree.md` (150 B)
- `Contrastive Learning Loss Functions.md` (185 B)

**Probable duplicates to review:**
- `Logistic Regression.md` + `Logistic Regression review 1.md` + `Logistic Regression review 2.md`
- `Linear Regression.md` + `Linear Regression for more complex models.md`
- `Word embedding and Word Representation.md` + `Word embedding and Word2Vec.md` + `SkipGram and CBOW.md`
- `Neural Network.md` + `Neural Networks Foundation.md`
- `CNN review.md` + `Convolutional Neural Networks.md`
