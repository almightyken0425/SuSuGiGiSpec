import sys
import re

def lint_file(filepath):
    print(f"Linting {filepath}...")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error opening file: {e}")
        sys.exit(1)

    errors = []
    in_code_block = False

    for i, line in enumerate(lines):
        line_num = i + 1
        stripped = line.strip()

        # Toggle code block
        if stripped.startswith('```'):
            in_code_block = not in_code_block
            continue

        if in_code_block:
            continue

        # 1. Parentheses (exclude links)
        # Simple heuristic: if we see '(', check if it's preceded by ']' (markdown link).
        # Also check for function calls in inline code `func()` which might be allowed if backticked.
        # The rule says: "嚴禁使用任何括號...例如 () []"
        # We will flag any '(' that is not inside backticks and not part of a markdown link pattern.
        
        # Remove components that are within backticks for checking
        line_no_code = re.sub(r'`[^`]*`', '', line)
        
        if '(' in line_no_code or ')' in line_no_code or '（' in line_no_code or '）' in line_no_code:
            # Check for link pattern ](
            if '](' not in line_no_code:
                 # Check if it's strictly just text
                 errors.append(f"Line {line_num}: Found parentheses: {line.strip()}")

        if '[' in line_no_code or ']' in line_no_code:
            # Check for link pattern [text](url) -> we removed parens check above but brackets remain
            # or checkbox - [ ]
            if not re.search(r'\[.*\]\(', line) and not re.search(r'-\s*\[[ x]\]', line):
                 errors.append(f"Line {line_num}: Found brackets: {line.strip()}")
                 
        # Full-width prohibited characters
        if re.search(r'[「」『』【】]', line_no_code):
             errors.append(f"Line {line_num}: Found prohibited quotes/brackets: {line.strip()}")

        # 2. Asterisk Lists
        if stripped.startswith('* ') and not stripped.startswith('**'):
            errors.append(f"Line {line_num}: Found asterisk list: {line.strip()}")

        # 3. Numbered Lists or Headers with numbers
        if re.match(r'^\s*\d+\.', line):
            errors.append(f"Line {line_num}: Found numbered list: {line.strip()}")
        
        # Header numbering check
        if line.startswith('#'):
            # Match patterns like "# 1. ", "## 2. ", "### 1. "
            if re.search(r'^#+\s*\d+[\.\s]', line):
                errors.append(f"Line {line_num}: Found numbered header: {line.strip()}")

        # 4. **備註:**
        if '**備註:**' in line:
            errors.append(f"Line {line_num}: Found prohibited key '**備註:**': {line.strip()}")

        # 5. Position words
        if re.search(r'(左:|右:|頂部:|底部:)', line):
            errors.append(f"Line {line_num}: Found position description: {line.strip()}")
            
    if errors:
        print("FAILED")
        for e in errors:
            print(e)
        sys.exit(1)
    else:
        print("PASSED")

import os

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: lint_spec.py <file_or_directory>")
        sys.exit(1)
    
    target = sys.argv[1]
    
    if os.path.isdir(target):
        print(f"Scanning directory: {target}")
        has_error = False
        for root, dirs, files in os.walk(target):
            # Skip hidden folders
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            for file in files:
                if file.endswith(".md"):
                    full_path = os.path.join(root, file)
                    print(f"\nChecking: {file}")
                    try:
                        lint_file(full_path)
                    except SystemExit as e:
                        if e.code != 0:
                            has_error = True
        
        if has_error:
            print("\nResult: Some files FAILED.")
            sys.exit(1)
        else:
            print("\nResult: All files PASSED.")
            sys.exit(0)

    else:
        lint_file(target)
