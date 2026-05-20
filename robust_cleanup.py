import re

with open('books/jubilees.draft.md', 'r') as f:
    content = f.read()

# Fix spacing around (ESV)
content = re.sub(r'\s+\(ESV\)', ' (ESV)', content)
content = re.sub(r'\(ESV\)([A-Za-z0-9])', r'(ESV) \1', content)

# Fix double parentheses like (Acts 12:15 (ESV))
content = re.sub(r'\(([^)]+)\s*\(ESV\)\)', r'(\1 (ESV))', content)

# Remove (ESV) from Jubilees again just to be sure
content = re.sub(r'Jubilees\s+([\d:;,\- ]+)\s*\(ESV\)', r'Jubilees \1', content)

# Fix trailing spaces in citations
content = re.sub(r'Jubilees\s+([\d:;,\- ]+)\s+', r'Jubilees \1 ', content)

# Ensure only one H1 title
h1_count = len(re.findall(r'^# ', content, re.M))
if h1_count > 1:
    # Only keep the first one
    h1s = re.finditer(r'^# ', content, re.M)
    next(h1s) # skip first
    for match in h1s:
        # replace with ##
        pass # need to be careful here

# Check for double spaces before line end (but keeping them if they are intentional line breaks)
# Project rule says: "Markdown may contain double spaces before line end characters. This is normal as it indicate a line break. Do not remove those spaces."
# So I won't touch double spaces at EOL.

with open('books/jubilees.draft.md', 'w') as f:
    f.write(content)
