---
layout: default
title: Wide
---

# [Cyber Apocalypse](index.md) - Reversing - Wide

This challenge is a small binary that reads a database file of different dimension names and descriptions. 
A menu appears listing the dimensions, and you are prompted to choose one to examine.

```
[*] Welcome user: kr4eq4L2$12xb, to the Widely Inflated Dimension Editor [*]
[*]    Serving your pocket dimension storage needs since 14,012.5 B      [*]
[*]                       Displaying Dimensions....                      [*]
[*]       Name       |              Code                |   Encrypted    [*]
[X] Primus           | people breathe variety practice  |                [*]
[X] Cheagaz          | scene control river importance   |                [*]
[X] Byenoovia        | fighting cast it parallel        |                [*]
[X] Cloteprea        | facing motor unusual heavy       |                [*]
[X] Maraqa           | stomach motion sale valuable     |                [*]
[X] Aidor            | feathers stream sides gate       |                [*]
[X] Flaggle Alpha    | admin secret power hidden        |       *        [*]
Which dimension would you like to examine?
```
Records are selected by entering their numbers. Entering number 6 indicates that the item is encrypted, and requests a key.

```
Which dimension would you like to examine? 6
[X] That entry is encrypted - please enter your WIDE decryption key:
```

Running `strings` with no parameters on the binary didn't reveal a key (or a flag).

Using `Ghidra` to decompile and explore the source code, we find a `menu` function with the following code in it:

```c++
iVar1 = wcscmp(local_1c8,L"sup3rs3cr3tw1d3");
if (iVar1 == 0) {
    for (local_1d4 = 0;
        (local_1d4 < 0x80 && (*(char *)((long)&local_98 + (long)(int)local_1d4) != '\0'));
        local_1d4 = local_1d4 + 1) {
    *(byte *)((long)&local_98 + (long)(int)local_1d4) =
            *(byte *)((long)&local_98 + (long)(int)local_1d4) ^
            (char)(local_1d4 * 0x1b) + (char)((int)(local_1d4 * 0x1b) / 0xff);
    }
    puts((char *)&local_98);
}
else {
    puts("[X]                          Key was incorrect                           [X]");
}
```
Which appears to be the decryption key and the algorithm used to encrypt.

Running the program again, selecting `6`, and giving it the key `sup3rs3cr3tw1d3` reveals the flag.

```
HTB{str1ngs_4r3nt_4lw4ys_4sc11}
```

The flag seemed to be a clue on a different way to solve this challenge - if `strings` didn't find it, but I can see it in the source code, it sounds like I could have coaxed `strings` into finding it if I didn't just use the default options.

`strings` supports different string encodings using the `-e` option:
```
-e encoding
--encoding=encoding
Select the character encoding of the strings that are to be found.  Possible values for encoding are: s = single-7-bit-byte characters (ASCII, ISO 8859, etc., default), S = single-8-bit-byte characters, b = 16-bit bigendian, l = 16-bit littleendian, B = 32-bit bigendian, L = 32-bit littleendian.  Useful for finding wide character strings. (l and b apply to, for example, Unicode UTF-16/UCS-2 encodings).
```
Trying each of these, eventually `-L` works to reveal the key from the binary.

```
# strings -e L wide
 sup3rs3cr3tw1d3
```
This makes sense because the upper-case `L` in the source code likely indicates the same string encoding.

```c++
iVar1 = wcscmp(local_1c8,L"sup3rs3cr3tw1d3");
```

In future endeavors I will make a script for `strings` to run through each encoding, just in case.