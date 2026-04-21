# Thesis SDPO — Wiki Schema

Context for Claude Code when working in `10_Projects/14_Thesis_SDPO/`.

## Purpose

Research wiki for the thesis: *Behavioral differences in reasoning — test-time SDPO reprompt template formulation on code*. Every paper, model, benchmark, or concept related to the thesis is captured and interlinked here so knowledge compounds as the project progresses.

## Three layers

1. **`raw/`** — immutable source documents (papers, web clips, datasheets). Claude reads but **never modifies** anything in `raw/`.
   - `raw/assets/` — images downloaded via Obsidian hotkey (Ctrl+Shift+D)
2. **`wiki/`** — Claude-owned markdown. Summaries, entity pages, concept pages, comparisons. Claude creates, updates, cross-references.
3. **`experiments/`** — experiment logs and code pointers. Owned by the user. Claude reads but does not modify.

## Wiki layout

```
wiki/
├── index.md          # catalog, read first on every query
├── log.md            # chronological record
├── sources/          # one page per ingested paper/article
├── entities/         # models, benchmarks, datasets
├── concepts/         # methods, phenomena, metrics
└── synthesis/        # comparisons, overviews, thesis proposal
```

## Naming conventions

- Snake_case file names (no spaces)
- Sources: `src_<firstauthor><year>_<shorttitle>.md` — e.g. `src_hubotter2025_self_distillation.md`
- Entities: `ent_<name>.md` — e.g. `ent_sdpo.md`, `ent_qwen3_8b.md`
- Concepts: `con_<name>.md` — e.g. `con_epistemic_verbalization.md`
- Synthesis: `syn_<name>.md` — e.g. `syn_template_taxonomy.md`

## YAML frontmatter (required on all wiki pages)

```yaml
---
type: source | entity | concept | synthesis
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [tag1, tag2]
sources: [src_foo2025, src_bar2026]   # pages this content derives from
---
```

## Workflows

### Ingest (new source added to `raw/`)

1. Read the source fully.
2. Discuss key takeaways with the user before writing.
3. Create `wiki/sources/src_<name>.md` with: one-paragraph abstract, key contributions, methods, results, my own notes/questions.
4. Identify entities and concepts mentioned. For each: create a new page if missing, or update the existing one (add a new section citing this source).
5. Cross-reference: every entity/concept page must link back to its sources via `[[src_*]]`. Source pages link forward to relevant entities/concepts.
6. Update `wiki/index.md`.
7. Append a log entry:

   ```
   ## [YYYY-MM-DD] ingest | <paper short title>
   - Created: src_..., con_...
   - Updated: ent_..., index.md
   - Key takeaway: <one sentence>
   ```

### Query

1. Read `wiki/index.md` first.
2. Drill into the named pages and their `[[links]]`.
3. Answer with citations pointing to `[[src_*]]` pages.
4. If the answer is reusable (comparison table, analysis, cross-cutting insight), propose filing it as `wiki/synthesis/syn_*.md`. Do not file without user approval.
5. Log query only if it produced a new page.

### Lint

Run periodically or when asked. Report:
- Contradictions between pages
- Claims that newer sources supersede
- Orphan pages (no inbound links)
- Concepts mentioned in body text but lacking their own page
- Missing cross-references
- Gaps where a web search would help fill a hole

Do not edit during lint — output a report, let the user decide.

## Rules

- **Never modify `raw/` or `experiments/`.**
- Use `[[wikilinks]]` (exact file name without extension) for every cross-reference inside `wiki/`.
- Every non-trivial claim in `synthesis/` must cite at least one `[[src_*]]`.
- When in doubt about page type or naming, ask the user.
- Update `index.md` on every wiki change. Append `log.md` on every ingest.

## Language convention

- **Body: tiếng Việt** — giải thích, transition, narrative, open questions.
- **Code-switch tự nhiên sang English** cho:
  - Terminology & methods: *SDPO, RLVR, credit assignment, self-teacher, epistemic verbalization, reprompt template*
  - Tên model / benchmark / tác giả / paper title
  - Technical ngắn gọn không có từ Việt tương đương hoặc dịch ra thì kỳ
- **Metadata (YAML frontmatter, log entries, file names): English** — giữ ổn định cho tooling.
- Không cần cứng nhắc — đọc thấy tự nhiên là được. Tránh dịch tên riêng hoặc dịch ép technical term.
