"""
codex.py - Data encoding utilities.
Handles the conversion of string payloads into different numerical bases,
simulating encoding transformations as a packet moves between nodes with
different 'codex' levels.
"""

def ascii_to_base(ascii_val, base):
    if ascii_val == 0:
        return "0"
    digits = []
    chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    while ascii_val > 0:
        digits.append(chars[ascii_val % base])
        ascii_val //= base
    return "".join(reversed(digits))

def encode_payload(text, base):
    return [ascii_to_base(ord(c), base) for c in text]
