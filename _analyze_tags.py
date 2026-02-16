import os
import re
from collections import defaultdict

ROOT = '/Users/maid12/Documents/projects/myVault'

tag_pattern = re.compile(r'(?<!\!)\[\[(.*?)\]\]')
code_block_pattern = re.compile(r'```.*?```', re.DOTALL)
inline_code_pattern = re.compile(r'`[^`\n]+`')

# tag -> list of (file, line_number, context)
tag_usage = defaultdict(list)
# tag -> set of files where it appears in a "Tags:" line
tag_as_category = defaultdict(set)
# tag -> set of files where it appears NOT in a "Tags:" line
tag_as_link = defaultdict(set)

md_files = []
for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if not d.startswith('.')]
    for f in filenames:
        if f.endswith('.md'):
            md_files.append(os.path.join(dirpath, f))

for filepath in md_files:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        clean = code_block_pattern.sub('', content)
        clean = inline_code_pattern.sub('', clean)
        
        for i, line in enumerate(clean.split('\n'), 1):
            matches = tag_pattern.findall(line)
            is_tag_line = line.strip().startswith('Tags:') or line.strip().startswith('tags:')
            
            for m in matches:
                raw = m.split('|')[0].strip()
                if raw.startswith('"') and raw.endswith('"'): continue
                if raw.startswith("'") and raw.endswith("'"): continue
                if not raw: continue
                
                rel = os.path.relpath(filepath, ROOT)
                tag_usage[raw].append((rel, i, line.strip()[:80]))
                
                if is_tag_line:
                    tag_as_category[raw].add(rel)
                else:
                    tag_as_link[raw].add(rel)
    except: pass

print("=" * 80)
print("1. CASE-INSENSITIVE DUPLICATES")
print("=" * 80)
lower_map = defaultdict(list)
for tag in tag_usage:
    lower_map[tag.lower()].append(tag)

for key, variants in sorted(lower_map.items()):
    if len(variants) > 1:
        print(f"  Duplicate group: {variants}")
        for v in variants:
            print(f"    '{v}' used {len(tag_usage[v])} times")

print("\n" + "=" * 80)
print("2. NAMING INCONSISTENCIES")
print("=" * 80)
camel_case = []
lower_case = []
title_case = []
mixed = []
for tag in sorted(tag_usage.keys()):
    if ' ' not in tag and tag[0].isupper() and any(c.isupper() for c in tag[1:]):
        camel_case.append(tag)
    elif tag == tag.lower():
        lower_case.append(tag)
    elif tag == tag.title() or (tag[0].isupper() and ' ' in tag):
        title_case.append(tag)
    else:
        mixed.append(tag)

print(f"  CamelCase (no spaces): {camel_case}")
print(f"  lowercase: {lower_case}")
print(f"  Title Case: {title_case[:20]}...")
print(f"  Mixed/Other: {mixed[:20]}")

print("\n" + "=" * 80)
print("3. TAGS USED ONLY AS CATEGORY (in Tags: lines)")
print("=" * 80)
only_category = set(tag_as_category.keys()) - set(tag_as_link.keys())
for t in sorted(only_category):
    print(f"  '{t}' -> used in {len(tag_as_category[t])} files as category tag")

print("\n" + "=" * 80)
print("4. TAGS USED ONLY AS INLINE LINKS (never in Tags: lines)")
print("=" * 80)
only_link = set(tag_as_link.keys()) - set(tag_as_category.keys())
for t in sorted(only_link):
    print(f"  '{t}' -> linked from {len(tag_as_link[t])} files")

print("\n" + "=" * 80)
print("5. TAGS USED BOTH WAYS")
print("=" * 80)
both = set(tag_as_category.keys()) & set(tag_as_link.keys())
for t in sorted(both):
    print(f"  '{t}' -> category in {len(tag_as_category[t])} files, linked in {len(tag_as_link[t])} files")

print("\n" + "=" * 80)
print("6. VERY LONG TAG NAMES (possibly note titles used as tags)")
print("=" * 80)
for tag in sorted(tag_usage.keys(), key=len, reverse=True):
    if len(tag) > 30:
        print(f"  [{len(tag)} chars] '{tag}' -> {len(tag_usage[tag])} uses")

print("\n" + "=" * 80)
print("7. TAG FILES IN '3 - Tags/' FOLDER")
print("=" * 80)
tags_folder = os.path.join(ROOT, '3 - Tags')
tag_files = set()
if os.path.exists(tags_folder):
    for f in os.listdir(tags_folder):
        if f.endswith('.md'):
            name = f[:-3]
            tag_files.add(name)
            if name not in tag_usage:
                print(f"  TAG FILE EXISTS but tag never used: '{name}'")
                
for tag in sorted(tag_usage.keys()):
    if tag in tag_files:
        pass  # has matching file
    else:
        # Check case-insensitive
        found = False
        for tf in tag_files:
            if tf.lower() == tag.lower():
                found = True
                print(f"  CASE MISMATCH: tag '{tag}' <-> file '{tf}.md'")
                break
        # Not reporting tags without files since many are note links

print("\n" + "=" * 80)
print("8. SUMMARY")
print("=" * 80)
print(f"  Total unique tags: {len(tag_usage)}")
print(f"  Tags used as category: {len(tag_as_category)}")
print(f"  Tags used as link: {len(tag_as_link)}")
print(f"  Tag files in 3-Tags folder: {len(tag_files)}")
print(f"  Case-insensitive duplicates: {sum(1 for v in lower_map.values() if len(v) > 1)}")
