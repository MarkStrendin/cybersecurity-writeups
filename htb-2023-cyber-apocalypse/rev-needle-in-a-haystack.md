---
layout: default
title: Needle in a Haystack
---

# [Cyber Apocalypse 2023](index.md) - Reversing - Needle in a Haystack

> You've obtained an ancient alien Datasphere, containing categorized and sorted recordings of every word in the forgotten intergalactic common language. Hidden within it is the password to a tomb, but the sphere has been worn with age and the search function no longer works, only playing random recordings. You don't have time to search through every recording - can you crack it open and extract the answer?

Like other reversing challenges, we're given a binary and that's it.

When doing reversing challenges, I like to run `strings` against the binary to see if the flag happens to be visible there. If it is, it can save me a ton of time trying to reverse engineer code.

```
$ strings haystack
/lib64/ld-linux-x86-64.so.2
srand
time
... lots of strings snipped out for brevity ...
ozglonori
chleatf
kroucalo?
HTB{d1v1ng_1nt0_th3_d4tab4nk5}
huarg
voremtc
glyubyuur
klesalo
.. lots of strings snipped out for brevity ...
.dynamic
.got.plt
.data
.bss
.comment
```

And we can see the flag is just in the list here.

```
HTB{d1v1ng_1nt0_th3_d4tab4nk5}
```

A potentially time-saving addition to running strings in a CTF where you know the format of the flags would be:

```sh
$ strings haystack | grep HTB
HTB{d1v1ng_1nt0_th3_d4tab4nk5}
```
This way a person doesn't need to actually _look_ through the list, saving valuable seconds.
