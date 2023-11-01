---
layout: default
title: Wide
---

# [Hack The Boo 2023 - Practice](index.md) - Crypto - Hexoding

> In order to be a successful ghost in the modern society, a ghost must fear nothing. Caspersky always loved scaring people, but he could not reach his maximum potential because he was fearful of cryptography. This is why he wants to join the Applied Cryptography Academy of Ghosts. To gain admission, the professors give you a challenge that you need to solve. They try to spook you with weird functions, but don't be scared; the challenge can be solved even without the source code. Can you help Caspersky pass the entrance exams?
Submit flag & press enter

We're provided two files:

`output.txt`
```
4854427b6b6e3077316e675f6830775f74305f3164336e743166795f336e633064316e675f736368336d33735f31735f6372756331346c5f6630725f615f
Y3J5cHQwZ3I0cGgzcl9fXzRsczBfZDBfbjB0X2MwbmZ1czNfZW5jMGQxbmdfdzF0aF9lbmNyeXA1MTBuIX0=
```

`source.py`
```python
from secret import FLAG

HEX_CHARS = '0123456789abcdef'
B64_CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'


def to_hex(data):
    data = int.from_bytes(data, 'big')
    encoded = ''
    while data:
        i = data % 16
        encoded = HEX_CHARS[i] + encoded
        data >>= 4
    return '0' * (len(encoded) % 2) + encoded


def to_base64(data):
    padding_length = 0

    if len(data) % 3 != 0:
        padding_length = (len(data) + 3 - len(data) % 3) - len(data)

    data += b'\x00' * padding_length
    bits = ''.join([bin(c)[2:].zfill(8) for c in data])
    blocks = [bits[i:i+6] for i in range(0, len(bits), 6)]

    encoded = ''
    for block in blocks:
        encoded += B64_CHARS[int(block, 2)]

    return encoded[:-padding_length] + '=' * padding_length


def main():
    first_half = FLAG[:len(FLAG)//2]
    second_half = FLAG[len(FLAG)//2:]

    hex_encoded = to_hex(first_half)
    base64_encoded = to_base64(second_half)

    with open('output.txt', 'w') as f:
        f.write(f'{hex_encoded}\n{base64_encoded}')

main()
```

The first thing I did was put the entire output into Cyberchef and try to base64 decode it, which does get us the second half of the flag, but the first half is all garbled.

```
..._crypt0gr4ph3r___4ls0_d0_n0t_c0nfus3_enc0d1ng_w1th_encryp510n!}
```

So taking a quick look a the code, we can see that it does in fact split the flag into two halfs:

```python
first_half = FLAG[:len(FLAG)//2]
second_half = FLAG[len(FLAG)//2:]
```

And it puts each half on it's own line, which I didn't notice at first:
```python
f.write(f'{hex_encoded}\n{base64_encoded}')
```

and its clear by the names of these variables that the first half is "hex encoded" and the second half is "base64 encoded". This seems obvious now - the first line only uses hex characters (0-9a-f), where the second line includes characters that don't make sense for hex (and is padded with an equals sign at the end).

So going back to CyberChef, we can hex decode the first half:

```
4854427b6b6e3077316e675f6830775f74305f3164336e743166795f336e633064316e675f736368336d33735f31735f6372756331346c5f6630725f615f
```
becomes
```
HTB{kn0w1ng_h0w_t0_1d3nt1fy_3nc0d1ng_sch3m3s_1s_cruc14l_f0r_a_
```

and the second half
```
Y3J5cHQwZ3I0cGgzcl9fXzRsczBfZDBfbjB0X2MwbmZ1czNfZW5jMGQxbmdfdzF0aF9lbmNyeXA1MTBuIX0=
```

becomes:
```
crypt0gr4ph3r___4ls0_d0_n0t_c0nfus3_enc0d1ng_w1th_encryp510n!}
```

And we now have the complete (very long) flag:
```
HTB{kn0w1ng_h0w_t0_1d3nt1fy_3nc0d1ng_sch3m3s_1s_cruc14l_f0r_a_crypt0gr4ph3r___4ls0_d0_n0t_c0nfus3_enc0d1ng_w1th_encryp510n!}
```

And the lesson here, as the flag tells us, is that encoding can be reversed without any sort of key or password, so we shouldn't rely on it to keep our secrets.