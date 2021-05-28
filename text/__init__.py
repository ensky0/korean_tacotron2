import re
from text import cleaners
from text.symbols import symbols, punct


# Mappings from symbol to numeric ID and vice versa:
_symbol_to_id = {s: i for i, s in enumerate(symbols)}
_id_to_symbol = {i: s for i, s in enumerate(symbols)}


# ch should be Korean syllable.
def _split_consonant(ch):
    n =  ord(ch) - 0xAC00
    x, jong = divmod(n, 28)
    cho, joong = divmod(x, 21)

    if jong == 0:
        return (chr(cho+0x1100), chr(joong+0x1161))
    else:
        return (chr(cho+0x1100), chr(joong+0x1161), chr(jong+0x11A7))


def _join_consonant(ids):
    cho, joong = ord(_id_to_symbol(ids[0]))-0x1100, ord(_id_to_symbol(ids[1]))-0x1161
    jong = 0 if len(ids) == 2 else ord(_id_to_symbol(ids[2]))-0x11A7

    return chr(588*cho + 28*joong + jong + 0xAC00)


def text_to_sequence(text, cleaner_names):
    seqs = []
    for ch in _clean_text(text, cleaner_names):
        if ch in punct:
            seqs.append(_symbol_to_id[ch])
        else:
            for consonant in _split_consonant(ch):
                seqs.append(_symbol_to_id[consonant])

    return seqs


def sequence_to_text(seqs):
    text = []
    for i, seq in enumerate(seqs):
        if seq in _id_to_symbol:
            text.append(_id_to_symbol[seq])
        else:
            if ((i+2) < len(seq)) and (seqs[i+2] < 47):
                text.append(_join_consonant(seqs[i:i+2]))
            else:
                text.append(_join_consonant(seqs[i:i+1]))

    return ''.join(text)


def _clean_text(text, cleaner_names):
  for name in cleaner_names:
    cleaner = getattr(cleaners, name)
    if not cleaner:
      raise Exception('Unknown cleaner: %s' % name)
    text = cleaner(text)
  return text

