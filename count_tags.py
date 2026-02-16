import os
import re

def count_tags(root_dir):
    unique_tags = set()
    tag_pattern = re.compile(r'\[\[([^\]]+)\]\]')
    
    file_count = 0
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Skip hidden directories like .git
        dirnames[:] = [d for d in dirnames if not d.startswith('.')]
        
        for filename in filenames:
            if filename.endswith('.md'):
                file_count += 1
                filepath = os.path.join(dirpath, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        matches = tag_pattern.findall(content)
                        for match in matches:
                            # Handle piped links [[Page Name|Display Text]] -> Page Name
                            tag_content = match.split('|')[0]
                            # Clean up whitespace? Usually tags are precise. 
                            # But [[ Tag ]] might be treated as " Tag ". 
                            # Usually Obsidian trims them. Let's strip.
                            tag = tag_content.strip()
                            
                            # Filter out image embeds like ![[image.png]] which is caught as image.png
                            # The regex is \[\[ ... \]\]
                            # If the original text was ![[...]], the regex matches [[...]] part?
                            # No, findall searches for pattern. 
                            # If text is ![[image.png]], findall starts at [.
                            # Wait, regex `\[\[` will match the `[[` inside `![[`.
                            # We need to distinguish `[[tag]]` from `![[image]]`.
                            # Let's adjust regex or check context.
                            pass
                            
                except Exception as e:
                    print(f"Error reading {filepath}: {e}")

    # Re-doing the loop with better regex or logic
    # We'll use a regex that looks for `![[...]` and ignores it, or just match [[...]] and check preceding char.
    pass

# Better approach script
import os
import re

def main():
    root_dir = '/Users/maid12/Documents/projects/myVault'
    unique_tags = set()
    # Matches [[...]] but we need to check it doesn't start with !
    # Using negative lookbehind is tricky if variable length, but `![` is fixed.
    # Pattern: (?<!\!)\[\[(.*?)\]\] 
    # This matches [[...]] not preceded by !
    tag_pattern = re.compile(r'(?<!\!)\[\[(.*?)\]\]')
    
    md_files = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if not d.path.startswith('.')] # .path not avail in strings
        dirnames[:] = [d for d in dirnames if not d.startswith('.')]
        for filename in filenames:
            if filename.endswith('.md'):
               md_files.append(os.path.join(dirpath, filename))
               
    print(f"Found {len(md_files)} markdown files.")
    
    for filepath in md_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                matches = tag_pattern.findall(content)
                for match in matches:
                    # match is the content inside [[...]]
                    # Handle pipe: [[Page|Display]] -> Page
                    raw_tag = match.split('|')[0].strip()
                    if raw_tag:
                        unique_tags.add(raw_tag)
        except Exception as e:
            print(f"Error reading {filepath}: {e}")

    print(f"Total unique tags found: {len(unique_tags)}")
    # Print first 20 for verification
    print("Sample tags:")
    for t in list(unique_tags)[:20]:
        print(f"- {t}")

if __name__ == "__main__":
    main()
