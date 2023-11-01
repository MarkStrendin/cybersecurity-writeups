---
layout: default
title: Candy Bowl
---

# [Hack The Boo 2023 - Practice](index.md) - Reversing - Candy Bowl

> Dip your hand in my candy bowl and see if you can pull out a flag!

We are provided a binary named `candybowl`.

This is a "very easy" puzzle in a practice CTF, so we should start with the basics and run `strings` against the binary to see what comes up.

```
...
Sugar Daddy
Brain Licker
Sour Patch Kids
Sour Punch
Toxic Waste
Warheads
HTB{4lw4y5_ch3ck_ur_k1d5_c4ndy}
Reaching into the candy bowl...
Your candy is... '%s'. Enjoy!
;*3$"
GCC: (Debian 10.2.1-6) 10.2.1 20210110
crtstuff.c
deregister_tm_clones
__do_global_dtors_aux
completed.0
...
```

And it looks like we've already found the flag.

```
HTB{4lw4y5_ch3ck_ur_k1d5_c4ndy}
```