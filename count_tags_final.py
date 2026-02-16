import os
import re

def main():
    root_dir = '/Users/maid12/Documents/projects/myVault'
    unique_tags = set()
    tag_pattern = re.compile(r'(?<!\!)\[\[(.*?)\]\]')
    code_block_pattern = re.compile(r'```.*?```', re.DOTALL)
    inline_code_pattern = re.compile(r'`[^`\n]+`')

    md_files = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if not d.startswith('.')]
        for filename in filenames:
            if filename.endswith('.md'):
               md_files.append(os.path.join(dirpath, filename))
               
    for filepath in md_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                content = code_block_pattern.sub('', content)
                content = inline_code_pattern.sub('', content)
                
                matches = tag_pattern.findall(content)
                for match in matches:
                    raw_tag = match.split('|')[0].strip()
                    if raw_tag.startswith('"') and raw_tag.endswith('"'): continue
                    if raw_tag.startswith("'") and raw_tag.endswith("'"): continue
                    if raw_tag:
                        unique_tags.add(raw_tag)
        except: pass

    print(f"Total unique tags (case-sensitive): {len(unique_tags)}")
    unique_tags_lower = set(t.lower() for t in unique_tags)
    print(f"Total unique tags (case-insensitive): {len(unique_tags_lower)}")

if __name__ == "__main__":
    main()
