#!/usr/bin/env python3
"""Walk the vault, extract wikilinks, emit graph.json for the portfolio viewer."""

import json
import re
from pathlib import Path

VAULT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT = VAULT_ROOT / "graph.json"

EXCLUDE_DIRS = {".obsidian", ".git", ".github", "scripts", "99_System", "copilot"}

# Top-level folder → color group (must mirror Abyss palette in viewer)
FOLDER_GROUP = {
    "10_Projects":       "projects",
    "20_Areas":          "areas",
    "30_Knowledge_Base": "knowledge",
    "40_Archives":       "archive",
    "50_Weekly_Notes":   "periodic",
    "60_Monthly_Notes":  "periodic",
    "70_Daily_Notes":    "periodic",
    "00_Dashboard":      "dashboard",
}

WIKILINK_RE = re.compile(r"\[\[([^\]\|#]+)(?:#[^\]\|]+)?(?:\|[^\]]+)?\]\]")


def collect_notes() -> dict[str, dict]:
    """Return {note_id: {title, group, path}} for every .md in vault."""
    notes = {}
    for md in VAULT_ROOT.rglob("*.md"):
        rel = md.relative_to(VAULT_ROOT)
        if any(part in EXCLUDE_DIRS for part in rel.parts):
            continue

        top = rel.parts[0] if len(rel.parts) > 1 else "root"
        group = FOLDER_GROUP.get(top, "other")
        title = md.stem
        note_id = str(rel.with_suffix("")).replace("\\", "/")

        notes[note_id] = {
            "id": note_id,
            "title": title,
            "group": group,
        }
    return notes


def build_title_index(notes: dict[str, dict]) -> dict[str, str]:
    """Map title (and basename) → note_id for resolving wikilinks."""
    index = {}
    for nid, n in notes.items():
        index.setdefault(n["title"].lower(), nid)
        index.setdefault(nid.lower(), nid)
    return index


def extract_links(notes: dict[str, dict], index: dict[str, str]) -> list[dict]:
    """Parse [[wikilinks]] from each note and resolve to known note ids."""
    links = []
    for nid in notes:
        path = VAULT_ROOT / f"{nid}.md"
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue

        seen = set()
        for match in WIKILINK_RE.finditer(text):
            target_raw = match.group(1).strip()
            target_key = target_raw.lower()
            target_id = index.get(target_key) or index.get(target_key.split("/")[-1])
            if target_id and target_id != nid and (nid, target_id) not in seen:
                seen.add((nid, target_id))
                links.append({"source": nid, "target": target_id})
    return links


def main() -> None:
    notes = collect_notes()
    index = build_title_index(notes)
    links = extract_links(notes, index)

    # Compute degree to size nodes in viewer
    degree: dict[str, int] = {nid: 0 for nid in notes}
    for l in links:
        degree[l["source"]] = degree.get(l["source"], 0) + 1
        degree[l["target"]] = degree.get(l["target"], 0) + 1
    for nid, n in notes.items():
        n["degree"] = degree.get(nid, 0)

    payload = {
        "nodes": list(notes.values()),
        "links": links,
        "stats": {
            "node_count": len(notes),
            "link_count": len(links),
        },
    }

    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(VAULT_ROOT)}: "
          f"{len(notes)} nodes, {len(links)} links")


if __name__ == "__main__":
    main()
