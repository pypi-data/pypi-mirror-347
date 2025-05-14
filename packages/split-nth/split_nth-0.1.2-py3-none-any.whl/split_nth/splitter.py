import re
def split_on_word(s, word, occ=1):
    matches = list(re.finditer(rf'\s+{re.escape(word)}\s+', s, flags=re.IGNORECASE))
    if occ < 1 or len(matches) < occ:
        return [s]
    start, end = matches[occ - 1].span()
    return [s[:start].strip(), s[end:].strip()]