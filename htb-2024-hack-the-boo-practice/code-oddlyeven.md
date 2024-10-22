---
layout: default
title: Oddly Even
---

# [Hack The Boo 2024 - Practice](index.md) - Coding - Oddly Even

> The ghostly clock ticks strangely. Determine whether its chimes are even or odd to calm the restless spirits.

We are given a docker container, which when launched and connected to via a web browser, we get a Python programming environment where we need to take an input of a number, and print "odd" if it's an odd number, and "even" if it's even. We only get one input at a time, via the `input()` method, and we need to `print()` out the answer.


We can use a Ternary conditional operator to do this in very few lines:
```python
x = int(input())
print("even" if x % 2 == 0 else "odd")
```

Or if we want others to be able to understand our code, we can do it the long way:

```python
x = int(input())

output = ""
if x % 2 == 0:
  output = "even"
else:
  output = "odd"

print(output)
```

By using the **modulus** operator, which in Python is `%`, we divide two numbers together but instead of their quotient we get the remainder. If the number divided by 2 has no remainder, it would be divisible evenly by 2. Since all even numbers are divisible by 2, the number must be even, and otherwise the number must be odd.

Either way, we get the flag:
```
HTB{15_iT_0dD_oR_Is_iT_n0t?_c198157c42089527b2d4edf7e703f439}
```