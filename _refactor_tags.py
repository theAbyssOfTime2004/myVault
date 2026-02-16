#!/usr/bin/env python3
"""
Obsidian Vault Tag Refactoring Script
- Phase 1: Merge case-insensitive duplicates
- Phase 2: Standardize naming conventions (CamelCase, underscores, etc.)
- Phase 3: Rename corresponding files in '3 - Tags/' folder
"""
import os
import re
import shutil
from collections import defaultdict

ROOT = '/Users/maid12/Documents/projects/myVault'
TAGS_FOLDER = os.path.join(ROOT, '3 - Tags')
DRY_RUN = False  # Set True to preview changes without applying

# ============================================================
# RENAME MAP: old_tag -> new_tag
# ============================================================
RENAME_MAP = {
    # Phase 1: Merge duplicates
    'machine learning': 'Machine Learning',
    'neural networks': 'Neural Networks',
    
    # Phase 2: Fix CamelCase / underscores / inconsistent casing
    'DeepLearning': 'Deep Learning',
    'high_performance_python': 'High Performance Python',
    'dsa': 'DSA',
    'fsds': 'FSDS',
    'Data_Mining_Lab3_Report': 'Data Mining Lab3 Report',
    
    # Phase 2b: Normalize similar naming styles
    'AI engineer': 'AI Engineering',  # merge with existing "AI Engineering"
}

# ============================================================

code_block_re = re.compile(r'```.*?```', re.DOTALL)

def find_md_files(root):
    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not d.startswith('.')]
        for f in filenames:
            if f.endswith('.md'):
                files.append(os.path.join(dirpath, f))
    return files

def replace_tag_in_content(content, old_tag, new_tag):
    """Replace [[old_tag]] with [[new_tag]], but NOT ![[old_tag]] (image embeds).
    Also handles [[old_tag|display]] -> [[new_tag|display]].
    Skips replacements inside code blocks."""
    
    # Split content by code blocks to preserve them
    parts = code_block_re.split(content)
    code_blocks = code_block_re.findall(content)
    
    new_parts = []
    for part in parts:
        # Replace [[old_tag]] but not ![[old_tag]]
        # Use negative lookbehind for !
        escaped_old = re.escape(old_tag)
        # Match [[old_tag]] or [[old_tag|...]]
        pattern = r'(?<!\!)\[\[' + escaped_old + r'(\|[^\]]*)?\]\]'
        
        def replacer(m):
            pipe_part = m.group(1) if m.group(1) else ''
            return f'[[{new_tag}{pipe_part}]]'
        
        part = re.sub(pattern, replacer, part)
        new_parts.append(part)
    
    # Reassemble with code blocks
    result = ''
    for i, part in enumerate(new_parts):
        result += part
        if i < len(code_blocks):
            result += code_blocks[i]
    
    return result

def main():
    print("=" * 70)
    print("OBSIDIAN VAULT TAG REFACTORING")
    print(f"Mode: {'DRY RUN (preview only)' if DRY_RUN else 'LIVE (applying changes)'}")
    print("=" * 70)
    
    md_files = find_md_files(ROOT)
    print(f"Found {len(md_files)} markdown files.\n")
    
    total_file_edits = 0
    total_tag_replacements = 0
    files_renamed = 0
    
    for old_tag, new_tag in RENAME_MAP.items():
        print(f"\n{'─' * 50}")
        print(f"Renaming: '{old_tag}' -> '{new_tag}'")
        print(f"{'─' * 50}")
        
        files_changed = 0
        
        for filepath in md_files:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                new_content = replace_tag_in_content(content, old_tag, new_tag)
                
                if new_content != content:
                    rel = os.path.relpath(filepath, ROOT)
                    # Count replacements
                    count = content.count(f'[[{old_tag}]]') + content.count(f'[[{old_tag}|')
                    print(f"  ✏️  {rel} ({count} replacement(s))")
                    
                    if not DRY_RUN:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                    
                    files_changed += 1
                    total_tag_replacements += count
                    
            except Exception as e:
                print(f"  ❌ Error processing {filepath}: {e}")
        
        if files_changed > 0:
            total_file_edits += files_changed
            print(f"  → {files_changed} file(s) updated")
        else:
            print(f"  → No occurrences found")
        
        # Rename tag file in 3-Tags if it exists
        old_file = os.path.join(TAGS_FOLDER, f'{old_tag}.md')
        new_file = os.path.join(TAGS_FOLDER, f'{new_tag}.md')
        
        if os.path.exists(old_file):
            # On macOS (case-insensitive FS), check if old and new are the same file
            same_file = False
            if os.path.exists(new_file):
                try:
                    same_file = os.path.samefile(old_file, new_file)
                except OSError:
                    same_file = False
            
            if same_file:
                # Case-only rename: use two-step rename via temp file
                print(f"  📁 Case-rename tag file: '{old_tag}.md' -> '{new_tag}.md'")
                if not DRY_RUN:
                    # Update content inside the file first
                    with open(old_file, 'r', encoding='utf-8') as f:
                        file_content = f.read()
                    file_content = replace_tag_in_content(file_content, old_tag, new_tag)
                    with open(old_file, 'w', encoding='utf-8') as f:
                        f.write(file_content)
                    # Two-step rename for case-insensitive FS
                    temp_file = old_file + '.tmp_rename'
                    os.rename(old_file, temp_file)
                    os.rename(temp_file, new_file)
                files_renamed += 1
            elif os.path.exists(new_file):
                # Target exists (truly different file), merge content
                print(f"  📁 Merging tag file: '{old_tag}.md' INTO '{new_tag}.md'")
                if not DRY_RUN:
                    with open(old_file, 'r', encoding='utf-8') as f:
                        old_content = f.read()
                    with open(new_file, 'r', encoding='utf-8') as f:
                        new_content_f = f.read()
                    
                    old_links = set(re.findall(r'\[\[(.*?)\]\]', old_content))
                    new_links = set(re.findall(r'\[\[(.*?)\]\]', new_content_f))
                    missing = old_links - new_links
                    
                    if missing:
                        merged = new_content_f.rstrip() + '\n'
                        for link in sorted(missing):
                            merged += f'[[{link}]]\n'
                        with open(new_file, 'w', encoding='utf-8') as f:
                            f.write(merged)
                        print(f"    Added {len(missing)} link(s) from old file")
                    
                    os.remove(old_file)
                    print(f"    Deleted old file: '{old_tag}.md'")
                files_renamed += 1
            else:
                # Simply rename
                print(f"  📁 Renaming tag file: '{old_tag}.md' -> '{new_tag}.md'")
                if not DRY_RUN:
                    # Also update content inside the file
                    with open(old_file, 'r', encoding='utf-8') as f:
                        file_content = f.read()
                    file_content = replace_tag_in_content(file_content, old_tag, new_tag)
                    with open(old_file, 'w', encoding='utf-8') as f:
                        f.write(file_content)
                    os.rename(old_file, new_file)
                files_renamed += 1
    
    print(f"\n{'=' * 70}")
    print("SUMMARY")
    print(f"{'=' * 70}")
    print(f"  Tags renamed:           {len(RENAME_MAP)}")
    print(f"  Files edited:           {total_file_edits}")
    print(f"  Tag replacements:       {total_tag_replacements}")
    print(f"  Tag files renamed/merged: {files_renamed}")
    
    if DRY_RUN:
        print("\n  ⚠️  DRY RUN - No changes were applied. Set DRY_RUN=False to apply.")

if __name__ == '__main__':
    main()
