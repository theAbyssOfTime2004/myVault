---
created: 2026-04-26
tags: [system, design, infrastructure]
---

# Vault Redesign · 2026-04-26

> Ghi lại toàn bộ thay đổi: theme Obsidian + pipeline đẩy graph lên portfolio.

---

## // mục_tiêu

Đồng bộ aesthetic của Obsidian vault với portfolio cá nhân (`theabyssoftime2004.github.io`), đồng thời phát hành graph view ra public web với cập nhật gần real-time.

---

## // phần_1_theme_obsidian

### Đã làm

- Trích xuất design tokens từ `style.css` của portfolio (color palette, font, spacing)
- Tạo CSS snippet `abyss-theme.css` override toàn bộ Obsidian dark theme
- Bỏ ASCII art của portfolio vào đầu `Home.md` làm splash banner
- Custom graph view: color groups theo folder, line size, text fade

### Color palette (muted variant của portfolio)

| Token            | Value     | Dùng cho               |
| ---------------- | --------- | ---------------------- |
| `bg`             | `#1c1528` | Background chính       |
| `bg-secondary`   | `#251c33` | Sidebar, code block    |
| `border`         | `#3d3050` | Divider, viền          |
| `text`           | `#c8c6c0` | Body text (warm gray)  |
| `text-muted`     | `#a8a6a0` | Secondary text         |
| `accent`         | `#a8ad7a` | Link, button, H1       |
| `accent-purple`  | `#a698bf` | H2, tag node           |
| `accent-green`   | `#8aa66e` | H3, periodic note      |
| `accent-orange`  | `#bfa078` | H4, attachment         |

### Files

- ▹ [[../.obsidian/snippets/abyss-theme.css]] — full theme override
- ▹ [[../.obsidian/appearance.json]] — accent color + enable snippet
- ▹ [[../.obsidian/graph.json]] — color groups + force settings

---

## // phần_2_graph_lên_web

### Kiến trúc

```
┌─────────────────┐    edit       ┌──────────────────┐
│  Obsidian (PC)  │ ────────────► │  myVault repo    │
└─────────────────┘  obsidian-git └────────┬─────────┘
                                           │ push
                                           ▼
                                  ┌──────────────────┐
                                  │ GitHub Action    │
                                  │ build_graph.py   │
                                  └────────┬─────────┘
                                           │ commit graph.json
                                           ▼
                          raw.githubusercontent.com/.../graph.json
                                           │ fetch
                                           ▼
                                  ┌──────────────────┐
                                  │  Portfolio site  │
                                  │  D3 graph viewer │
                                  └──────────────────┘
```

Tổng độ trễ end-to-end: **~1–2 phút** từ khi save note đến khi web update.

### Các thành phần

**Vault repo (`myVault`):**

| File                                | Vai trò                                                             |
| ----------------------------------- | ------------------------------------------------------------------- |
| `scripts/build_graph.py`            | Walk vault → parse `[[wikilink]]` → output `graph.json` (nodes/links) |
| `.github/workflows/build-graph.yml` | Trigger trên push file `.md`, chạy parser, commit graph.json        |
| `graph.json`                        | Output: structure-only (title + folder + edges), không có content    |

**Portfolio repo (`theAbyssOfTime2004.github.io`):**

| File                  | Vai trò                                                            |
| --------------------- | ------------------------------------------------------------------ |
| `js/graph-viewer.js`  | D3 force-directed graph; fetch graph.json; hover/drag/zoom         |
| `css/style.css`       | Style container, legend, stats — match Abyss palette               |
| `about.html`          | Section `VAULT GRAPH :` + load D3 CDN + viewer script              |

### Cách parser hoạt động

1. `rglob("*.md")` toàn vault, skip folder ẩn (`.obsidian`, `.git`, `99_System`, …)
2. Mỗi note → node: `{ id, title, group (theo top-level folder), degree }`
3. Regex `\[\[([^\]\|#]+)...\]\]` để bóc target từ wikilink (có alias, có heading)
4. Dùng title-index để resolve link → ID (handle case-insensitive + basename)
5. Tính degree để node nhiều liên kết hiển thị to hơn
6. Output JSON: `{ nodes: [...], links: [...], stats: {...} }`

### Cách viewer hiển thị

- `d3.forceSimulation` với 4 force: `link`, `charge` (đẩy), `center`, `collide`
- Color theo group key (Projects → accent vàng, Knowledge → tím, v.v.)
- Hover node: build adjacency map → fade non-neighbors xuống opacity 0.15
- Drag = `d3.drag` với `fx/fy` lock vị trí
- Zoom = `d3.zoom` scale 0.2–4×

---

## // bảo_trì

### Khi thêm/đổi màu folder

1. Sửa `FOLDER_GROUP` trong [[../scripts/build_graph.py]]
2. Sửa `PALETTE.groups` trong `js/graph-viewer.js` của portfolio
3. Push cả 2 repo

### Khi muốn ẩn folder khỏi graph public

Thêm tên folder vào `EXCLUDE_DIRS` trong `build_graph.py`. Hiện tại đang ẩn:
`.obsidian`, `.git`, `.github`, `scripts`, `99_System`, `copilot`.

### Khi parser fail

Vào tab Actions của `myVault` repo trên GitHub → xem log workflow `build-graph` → fix script local rồi push lại.

### Khi muốn test parser local

Cần Python 3.11+. Hiện máy chưa cài Python trong PATH — chỉ chạy được trên CI. Nếu cần test local: cài Python hoặc dùng `py -3.11 scripts/build_graph.py`.

---

## // điểm_cần_lưu_ý

- Vault repo phải **public** vì portfolio fetch trực tiếp qua `raw.githubusercontent.com`. Nếu chuyển private, phải đổi sang flow push-graph-to-portfolio (cần GitHub PAT)
- `graph.json` chỉ chứa **title** và **folder name** — không leak content note. Nhưng filename vẫn lộ, nên đặt tên file đừng nhạy cảm
- ASCII splash trong [[../00_Dashboard/Home]] chỉ render đẹp ở **Reading mode**, không phải Edit/Live preview
- Workflow chỉ trigger khi có thay đổi `.md` (config trong `paths:` của workflow)
