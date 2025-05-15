# InAFish encoding.
# >[_] not good encoding
# very small output, but very slow output
import random
import string

"""
Encodes a string into an encoded string.

Arguments:
string search: The string to search for in the encoded string.
list get: The string to use for encoding. Default is string.printable. Not recomended to change.
Returns:
string: The encoded string.

"""
def encode(search="hi", get=string.printable):
    random.seed(0)
    out = ""
    while True:
        out += random.choice(get)
        if search in out:
            return f"{out.index(search)}-{len(search)}"

"""
Decodes an encoded string into a normal string.

Arguments:
string search: The string to search decode.
list get: The string to use for decoding. Default is string.printable. Not recomended to change. Must be the same as the one used in encode.
Returns:
string: The decoded string.
"""

def decode(search="4718-2", get=string.printable):
    start, length = map(int, search.split("-"))
    random.seed(0)
    out = ""
    for _ in range(start):
        out += random.choice(get)
    out1 = ""
    for _ in range(length):
        out1 += random.choice(get)
    return out1

