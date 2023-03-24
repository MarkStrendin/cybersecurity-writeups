---
layout: default
title: Shattered Tablet
---

# [Cyber Apocalypse 2023](index.md) - Reversing - Shattered Tablet

> Deep in an ancient tomb, you've discovered a stone tablet with secret information on the locations of other relics. However, while dodging a poison dart, it slipped from your hands and shattered into hundreds of pieces. Can you reassemble it and read the clues?

We're just given a zip file with a binary. Running the binary prompts us for a string, but doesn't give us much to go on.

When doing reversing challenges, I like to run `strings` against the binary to see if the flag happens to be visible there. If it is, it can save me a ton of time trying to reverse engineer code.

```sh
$ strings tablet
/lib64/ld-linux-x86-64.so.2
mgUa
puts
stdin
printf
fgets
__cxa_finalize
__libc_start_main
libc.so.6
GLIBC_2.2.5
_ITM_deregisterTMCloneTable
__gmon_start__
... lots more things that aren't the flag, removed for brevity...
```
So, since that didn't work, we'll need to look at the source code for this.

Analyzing the binary in Ghidra, we find a small program with an extremely complicated `if` statement.

```c
  local_48 = 0;
  local_40 = 0;
  local_38 = 0;
  local_30 = 0;
  local_28 = 0;
  local_20 = 0;
  local_18 = 0;
  local_10 = 0;
  printf("Hmmmm... I think the tablet says: ");
  fgets((char *)&local_48,64,stdin);
  if (((((((((local_30._7_1_ == 'p') && (local_48._1_1_ == 'T')) && (local_48._7_1_ == 'k')) &&
          ((local_28._4_1_ == 'd' && (local_40._3_1_ == '4')))) &&
         ((local_38._4_1_ == 'e' && ((local_40._2_1_ == '_' && ((char)local_48 == 'H')))))) &&
        (local_28._2_1_ == 'r')) &&
       ((((local_28._3_1_ == '3' && (local_30._1_1_ == '_')) && (local_48._2_1_ == 'B')) &&
        (((local_30._5_1_ == 'r' && (local_48._3_1_ == '{')) &&
         ((local_30._2_1_ == 'b' && ((local_48._5_1_ == 'r' && (local_40._5_1_ == '4')))))))))) &&
      (((local_30._6_1_ == '3' &&
        (((local_38._3_1_ == 'v' && (local_40._4_1_ == 'p')) && (local_28._1_1_ == '1')))) &&
       (((local_30._3_1_ == '3' && (local_38._1_1_ == 'n')) &&
        (((local_48._4_1_ == 'b' && (((char)local_28 == '4' && (local_40._1_1_ == 'n')))) &&
         ((char)local_38 == ',')))))))) &&
     ((((((((char)local_40 == '3' && (local_48._6_1_ == '0')) && (local_38._7_1_ == 't')) &&
         ((local_40._7_1_ == 't' && ((char)local_30 == '0')))) &&
        ((local_40._6_1_ == 'r' && ((local_28._5_1_ == '}' && (local_38._5_1_ == 'r')))))) &&
       (local_38._6_1_ == '_')) && ((local_38._2_1_ == '3' && (local_30._4_1_ == '_')))))) {
    puts("Yes! That\'s right!");
  }
```
I can see the characters `H`, `T`, `B`, `{`, and `}` in there, but they are out of order. I also notice that while the program is getting input into a single variable, there are multiple variables being checked here.

The operators are all `&&` (which means "AND"), so the nesting and order doesn't actually matter in the `if` statement here - so lets clean them up a bit by removing all the brackets.

```c
local_30._7_1_ == 'p'
local_48._1_1_ == 'T'
local_48._7_1_ == 'k'
local_28._4_1_ == 'd'
local_40._3_1_ == '4'
local_38._4_1_ == 'e'
local_40._2_1_ == '_'
local_48 == 'H'
local_28._2_1_ == 'r'
local_28._3_1_ == '3'
local_30._1_1_ == '_'
local_48._2_1_ == 'B'
local_30._5_1_ == 'r'
local_48._3_1_ == '{'
local_30._2_1_ == 'b'
local_48._5_1_ == 'r'
local_40._5_1_ == '4'
local_30._6_1_ == '3'
local_38._3_1_ == 'v'
local_40._4_1_ == 'p'
local_28._1_1_ == '1'
local_30._3_1_ == '3'
local_38._1_1_ == 'n'
local_48._4_1_ == 'b'
local_28 == '4'
local_40._1_1_ == 'n'
local_38 == ','
local_40 == '3'
local_48._6_1_ == '0'
local_38._7_1_ == 't'
local_40._7_1_ == 't'
local_30 == '0'
local_40._6_1_ == 'r'
local_28._5_1_ == '}'
local_38._5_1_ == 'r'
local_38._6_1_ == '_'
local_38._2_1_ == '3'
local_30._4_1_ == '_'
```
Simply sorting the lines puts them together in groups based on the variable names that Ghidra assigned. We start to see parts of words (in leetspeak) but they are still out of order.

```c
local_28 == '4'
local_28._1_1_ == '1'
local_28._2_1_ == 'r'
local_28._3_1_ == '3'
local_28._4_1_ == 'd'
local_28._5_1_ == '}'
local_30 == '0'
local_30._1_1_ == '_'
local_30._2_1_ == 'b'
local_30._3_1_ == '3'
local_30._4_1_ == '_'
local_30._5_1_ == 'r'
local_30._6_1_ == '3'
local_30._7_1_ == 'p'
local_38 == ','
local_38._1_1_ == 'n'
local_38._2_1_ == '3'
local_38._3_1_ == 'v'
local_38._4_1_ == 'e'
local_38._5_1_ == 'r'
local_38._6_1_ == '_'
local_38._7_1_ == 't'
local_40 == '3'
local_40._1_1_ == 'n'
local_40._2_1_ == '_'
local_40._3_1_ == '4'
local_40._4_1_ == 'p'
local_40._5_1_ == '4'
local_40._6_1_ == 'r'
local_40._7_1_ == 't'
local_48 == 'H'
local_48._1_1_ == 'T'
local_48._2_1_ == 'B'
local_48._3_1_ == '{'
local_48._4_1_ == 'b'
local_48._5_1_ == 'r'
local_48._6_1_ == '0'
local_48._7_1_ == 'k'
```

Re-arranging these in the order that the variables are defined in gives us the letters of the flag:

```c
local_48 == 'H'
local_48._1_1_ == 'T'
local_48._2_1_ == 'B'
local_48._3_1_ == '{'
local_48._4_1_ == 'b'
local_48._5_1_ == 'r'
local_48._6_1_ == '0'
local_48._7_1_ == 'k'
local_40 == '3'
local_40._1_1_ == 'n'
local_40._2_1_ == '_'
local_40._3_1_ == '4'
local_40._4_1_ == 'p'
local_40._5_1_ == '4'
local_40._6_1_ == 'r'
local_40._7_1_ == 't'
local_38 == ','
local_38._1_1_ == 'n'
local_38._2_1_ == '3'
local_38._3_1_ == 'v'
local_38._4_1_ == 'e'
local_38._5_1_ == 'r'
local_38._6_1_ == '_'
local_38._7_1_ == 't'
local_30 == '0'
local_30._1_1_ == '_'
local_30._2_1_ == 'b'
local_30._3_1_ == '3'
local_30._4_1_ == '_'
local_30._5_1_ == 'r'
local_30._6_1_ == '3'
local_30._7_1_ == 'p'
local_28 == '4'
local_28._1_1_ == '1'
local_28._2_1_ == 'r'
local_28._3_1_ == '3'
local_28._4_1_ == 'd'
local_28._5_1_ == '}'
```

And cleaning this up quick in a text editor gives us the flag in a single string.

```
HTB{br0k3n_4p4rt,n3ver_t0_b3_r3p41r3d}
```

Running the binary and giving it the flag as input even tells us that it's correct.

```
Hmmmm... I think the tablet says: HTB{br0k3n_4p4rt,n3ver_t0_b3_r3p41r3d}
Yes! That's right!
```