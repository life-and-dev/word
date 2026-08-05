import re

with open('books/jubilees.draft.md', 'r') as f:
    content = f.read()

# 1. Fix H1 spacing (remove extra newlines)
content = re.sub(r'# Book of Jubilees\n+', '# Book of Jubilees\n', content)

# 2. Fix (ESV) mess
# Remove (ESV) from Jubilees citations
content = re.sub(r'Jubilees\s+([\d:;,\- ]+)\s*\(ESV\)', r'Jubilees \1', content)

# Ensure space after (ESV) if followed by alphanumeric char
content = re.sub(r'\(ESV\)([A-Za-z0-9])', r'(ESV) \1', content)

# Remove double (ESV) if any left
content = content.replace('(ESV) (ESV)', '(ESV)')

# 3. Rewrite Conclusion to properly summarize and link
conclusion_intro = """
## Conclusion

The Book of Jubilees serves as a critical bridge for understanding the evolution of Jewish thought during the Second Temple period. By retelling the narratives of Genesis and Exodus through a sectarian lens, it emphasizes the eternal nature of the Law and the necessity of Jewish distinctiveness.

"""

summaries = [
    ("- Scholarly consensus identifies the author as a Jewish priest from the second century BCE who used the authority of Moses to promote specific legal and calendrical interpretations. (See [Authorship](#authorship))"),
    ("- The article highlights how the text emerged from the cultural tensions of the Maccabean period, reflecting a deep dissatisfaction with the Jerusalem Temple establishment. (See [History](#history))"),
    ("- A primary purpose of the work was to enforce strict boundaries between Jews and Gentiles, particularly through the prohibition of intermarriage and the promotion of a unique 364-day solar calendar. (See [Purpose](#purpose))"),
    ("- Although not canonical in most Western traditions, Jubilees influenced several New Testament writers and was widely cited by early Church Fathers before its eventual suppression. (See [References](#references))"),
    ("- The Ethiopian Orthodox Tewahedo Church remains the only major tradition to accept Jubilees as fully canonical Scripture, preserving the complete text in Ge'ez. (See [Canon](#canon))"),
    ("- Unique teachings such as a developed hierarchy of angels, the role of demonic agency under Mastema, and the doctrine of heavenly tablets distinguish Jubilees from other contemporary literature. (See [Teachings](#teachings))"),
    ("- Comparison with the Dead Sea Scrolls has vindicated the accuracy of the Ethiopic translation while also identifying minor errors that accumulated over centuries of transmission. (See [Variants](#variants))"),
    ("- Textual inconsistencies and radical departures from the canonical Genesis narrative suggest that the book underwent significant editorial expansion and reflects specific sectarian interests. (See [Errors](#errors))"),
    ("- Direct contradictions with other biblical books regarding the fate of Lot's descendants and the origin of major festivals highlight the divergent theological traditions present in Second Temple Judaism. (See [Conflicts](#conflicts))")
]

new_conclusion = conclusion_intro + "\n".join(summaries) + "\n"

# Replace existing Conclusion section
content = re.sub(r'## Conclusion.*', new_conclusion, content, flags=re.DOTALL)

with open('books/jubilees.draft.md', 'w') as f:
    f.write(content)
