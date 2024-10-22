---
layout: default
title: Addition
---

# [Hack The Boo 2024 - Practice](index.md) - Coding - Addition

> Two ancient runes hold hidden powers. Combine them to unlock the sum and reveal their secret.

We are given a docker container, which when launched and connected to via a web browser, we get a Python programming environment where we need to take an input of two numbers, and add them together. Again, the example code is not helping us here, so we can completely disregard it.

We get two numbers, presumably separately, so we can collect those with two `input()` commands.

```python
x = int(input())
y = int(input())
```

We can then output the numbers added together

```python
print(int(x + y))
```

And this solves the challenge, and we get the flag.

```
HTB{aDd1nG_4lL_tH3_waY_b0085421e866a1de43f6d0bc141ea112}
```

The complete code I used was:
```python
x = int(input())
y = int(input())
print(int(x + y))
```