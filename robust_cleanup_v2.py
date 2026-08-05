import re

with open('books/jubilees.draft.md', 'r') as f:
    content = f.read()

# 1. Normalize spaces before (ESV) to exactly one
content = re.sub(r'\s+\(ESV\)', ' (ESV)', content)

# 2. Fix the mangled New Testament double ref
# (Matthew 18:10, (ESV) Acts 12:15 (ESV)) -> (Matthew 18:10; Acts 12:15 (ESV))
content = re.sub(r'\(Matthew 18:10,\s*\(ESV\)\s*Acts 12:15\s*\(ESV\)\)', r'(Matthew 18:10; Acts 12:15 (ESV))', content)

# 3. Fix ranges like Genesis 1 (ESV) through Exodus 19 (ESV)
# Ranges should have (ESV) only at the end
content = content.replace('Genesis 1 (ESV) to Exodus 19 (ESV)', 'Genesis 1 to Exodus 19 (ESV)')
content = content.replace('Genesis 1 (ESV) through Exodus 19 (ESV)', 'Genesis 1 to Exodus 19 (ESV)')

# 4. Remove (ESV) from Jubilees citations again
content = re.sub(r'Jubilees\s+([\d:;,\- ]+)\s*\(ESV\)', r'Jubilees \1', content)

# 5. Remove trailing spaces in Jubilees citations
content = re.sub(r'Jubilees\s+([\d:;,\- ]+)\s+', r'Jubilees \1 ', content)

# 6. Fix specific mangled refs found in trace
content = content.replace('Jubilees 1:7-18 (ESV)', 'Jubilees 1:7-18')
content = content.replace('Jubilees 1:29 (ESV)', 'Jubilees 1:29')
content = content.replace('Jubilees 27:22 (ESV)', 'Jubilees 27:22')
content = content.replace('Jubilees 49:7 (ESV)', 'Jubilees 49:7')
content = content.replace('Jubilees 50:13 (ESV)', 'Jubilees 50:13')
content = content.replace('Jubilees 35:17 (ESV)', 'Jubilees 35:17')
content = content.replace('Jubilees 30:19-23 (ESV)', 'Jubilees 30:19-23')

# 7. Ensure space after (ESV) if followed by text
content = re.sub(r'\(ESV\)([A-Za-z])', r'(ESV) \1', content)

# 8. Semicolon between different books
content = content.replace('Jeremiah 48-49 (ESV); Isaiah 15-16 (ESV)', 'Jeremiah 48-49; Isaiah 15-16 (ESV)')
content = content.replace('Matthew 18:10, (ESV) Acts 12:15 (ESV)', 'Matthew 18:10; Acts 12:15 (ESV)')

# 9. Final check for "the LORD" in quotes
# Jubilees 27:22 quote
content = content.replace('"I am the Lord God of Abraham', '"I am the LORD God of Abraham')

with open('books/jubilees.draft.md', 'w') as f:
    f.write(content)
