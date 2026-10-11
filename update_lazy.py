import os
import re

entity_dir = 'src/main/java/vn/bookstore/the4bookstore/entity'

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Replace @ManyToOne with no arguments
    content = re.sub(r'@ManyToOne\s*\n', r'@ManyToOne(fetch = FetchType.LAZY)\n', content)
    content = re.sub(r'@ManyToOne\s*\r?\n', r'@ManyToOne(fetch = FetchType.LAZY)\n', content)
    # Also for cases where it might just be @ManyToOne without newline (rare, but just in case)
    # Actually, a better regex: @ManyToOne without following parenthesis
    content = re.sub(r'@ManyToOne(?!\s*\()', r'@ManyToOne(fetch = FetchType.LAZY)', content)
    
    # Same for @OneToOne
    content = re.sub(r'@OneToOne(?!\s*\()', r'@OneToOne(fetch = FetchType.LAZY)', content)

    # For @ManyToOne(...) or @OneToOne(...)
    def modify_annotation(match):
        anno = match.group(1)
        args = match.group(2)
        if 'fetch' in args:
            args = re.sub(r'fetch\s*=\s*FetchType\.[A-Z]+', 'fetch = FetchType.LAZY', args)
        else:
            args += ', fetch = FetchType.LAZY'
        return f"@{anno}({args})"

    content = re.sub(r'@(ManyToOne|OneToOne)\s*\((.*?)\)', modify_annotation, content)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {filepath}")

for root, _, files in os.walk(entity_dir):
    for f in files:
        if f.endswith('.java'):
            process_file(os.path.join(root, f))
