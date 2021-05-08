import re
from text.symbols import is_symbol


_whitespace_re = re.compile(r'\s+')


def dummy_cleaners(text):
    for i, ch in enumerate(text):
        if not is_symbol(ch):
            text[i] = ' '

    return re.sub(_whitespace_re, ' ', text)

