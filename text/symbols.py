_pad = ''
punct = ' .,?!'
_initial_consonant = [chr(x) for x in range(0x1100, 0x1113)]
_medial_consonant = [chr(x) for x in range(0x1161, 0x1176)]
_final_consonant = [chr(x) for x in range(0x11A8, 0x11C3)]

symbols = [_pad] + list(punct) + _initial_consonant + _medial_consonant + _final_consonant

def is_symbol(ch):
    if (ch in punct) or (0xAC00 <= ord(ch) <= 0xD7A3):
        return True
    return False

