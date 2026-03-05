import re

with open('books/genesis.draft.md', 'r') as f:
    content = f.read()

# 1. Restore external links that were 403/429
content = content.replace('Ancient Near Eastern Context - BioLogos', '[Ancient Near Eastern Context](https://biologos.org/common-questions/is-genesis-real-history) - BioLogos')
content = content.replace('The Historical and Cultural Context of Genesis - Medium', '[The Historical and Cultural Context of Genesis](https://medium.com/@aaronrschuck/the-historical-and-cultural-context-of-genesis-10e7ed903e51) - Medium')
content = content.replace('Genesis. The Seedbed of All Christian Doctrine - Creation.com', '[Genesis—The Seedbed of All Christian Doctrine](https://creation.com/genesis-the-seedbed-of-all-christian-doctrine) - Creation.com')
content = content.replace('The Use of Genesis in the New Testament - Creation.com', '[The Use of Genesis in the New Testament](https://creation.com/genesis-new-testament) - Creation.com')
content = content.replace('Biblical Canon - Britannica', '[Biblical Canon](https://www.britannica.com/topic/biblical-canon) - Britannica')

# 2. Fix definitions that were blockquotes
content = content.replace('\n\n> Genesis — meaning "origins" or "beginnings"\n\n', ' Genesis (meaning "origins" or "beginnings") ')
content = content.replace('\n\n> The Five Books — in Greek *Pentateuch*, meaning "five scrolls"\n\n', ' The Five Books (in Greek *Pentateuch*, meaning "five scrolls") ')

# 3. Fix Bible citation formatting and parentheses
books = ['Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy', 'Joshua', 'Judges', 'Ruth', '1 Samuel', '2 Samuel', '1 Kings', '2 Kings', '1 Chronicles', '2 Chronicles', 'Ezra', 'Nehemiah', 'Esther', 'Job', 'Psalms', 'Proverbs', 'Ecclesiastes', 'Song of Solomon', 'Isaiah', 'Jeremiah', 'Lamentations', 'Ezekiel', 'Daniel', 'Hosea', 'Joel', 'Amos', 'Obadiah', 'Jonah', 'Micah', 'Nahum', 'Habakkuk', 'Zephaniah', 'Haggai', 'Zechariah', 'Malachi', 'Matthew', 'Mark', 'Luke', 'John', 'Acts', 'Romans', '1 Corinthians', '2 Corinthians', 'Galatians', 'Ephesians', 'Philippians', 'Colossians', '1 Thessalonians', '2 Thessalonians', '1 Timothy', '2 Timothy', 'Titus', 'Philemon', 'Hebrews', 'James', '1 Peter', '2 Peter', '1 John', '2 John', '3 John', 'Jude', 'Revelation']
book_regex = '|'.join([re.escape(b) for b in books])

def normalize_citation(match):
    # This matches anything inside parentheses that looks like a Bible citation
    inner = match.group(1)

    # Remove all existing (ESV) to re-add it at the end
    inner_clean = inner.replace(' (ESV)', '').replace('(ESV)', '')

    # Split by semicolon (different books)
    parts = re.split(r';\s*', inner_clean)
    new_parts = []
    for p in parts:
        # Check if p starts with a book name
        book_match = re.match(rf'^({book_regex})\s+(.*)', p)
        if book_match:
            bname = book_match.group(1)
            refs = book_match.group(2)
            # Fix chapter/verse separators in refs
            # Chapters: comma and space
            # Verses: comma only

            # This is hard to do perfectly with regex, so we'll do common patterns
            # 1:1, 2:1 -> 1:1, 2:1 (OK)
            # 1:1-3,5-7 -> 1:1-3,5-7 (OK)
            # 1:1,3 -> 1:1,3 (OK)
            # Fix if someone used semicolon for same book chapters
            refs = re.sub(r'(\d+:\d+(?:-\d+)?);\s*(\d+)', r'\1, \2', refs)
            new_parts.append(f"{bname} {refs}")
        else:
            # Same book as previous part
            new_parts.append(p)

    # Re-join with semicolons if they are different books, but my logic above is a bit simplified
    # Let's just join with semicolon and then fix semicolons within same book
    final_inner = '; '.join(new_parts)

    return f"({final_inner} (ESV))"

# Applying it selectively to avoid destroying other parens
content = re.sub(rf'\((({book_regex})\s+[^)]+)\)', normalize_citation, content)

# 4. Correct ESV wording (A second pass to be sure)
content = content.replace('Let us make man in our image, after our likeness', 'Let us make man in our image, after our likeness') # Matches ESV
content = content.replace('Genesis 1:26 (ESV) ("male and female he created them")', 'Genesis 1:27 (ESV) ("male and female he created them")')

# 5. Fix Conclusion links
# Use exact slugs from the file
content = content.replace('(#2-the-image-of-god-imago-dei)', '(#2-the-image-of-god-imago-dei)')
content = content.replace('(#3-the-fall-and-original-sin)', '(#3-the-fall-and-original-sin)')
content = content.replace('(#4-the-proto-evangelium-first-gospel-promise)', '(#4-the-proto-evangelium-first-gospel-promise)')
content = content.replace('(#national-identity-and-covenant-formation)', '(#national-identity-and-covenant-formation)')
content = content.replace('(#practical-and-pastoral-purposes)', '(#practical-and-pastoral-purposes)')

# 6. Final Polish
content = content.replace(' (ESV))', ' (ESV))') # Ensure single closing
content = content.replace(' (ESV)))', ' (ESV))')
content = content.replace(' (ESV)) )', ' (ESV))')
content = content.replace('..', '.')
content = content.replace('. .', '.')
content = content.replace(' (ESV)).', ' (ESV)).')

with open('books/genesis.draft.md', 'w') as f:
    f.write(content)
