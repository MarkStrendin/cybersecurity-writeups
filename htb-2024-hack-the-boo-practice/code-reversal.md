---
layout: default
title: Reversal
---

# [Hack The Boo 2024 - Practice](index.md) - Coding - Reversal

> A dark incantation was written backward in a spellbook. Reverse the cursed words to reveal their true meaning.

We are given a docker container, which when launched and connected to via a web browser, we get a Python programming environment where we need to take an input, reverse it, and print the output. Most of the demo/placeholder code can be removed, especially where it parses the input as an `int` for some reason... that's not going to help.


We can use Python's "Slicing" abilities to very efficiently reverse the input string:
```python
n = input()
print(n[::-1])
```

But if you don't know anything about Python or slicing, then that's very confusing. 

We could do this the long way instead, ensuring that our code is readable and understandable to those who do not code in Python:

```python
n = input()

def reverse_string(input_string):
    reversed_str = ''
    for char in input_string:
        reversed_str = char + reversed_str
    return reversed_str

print(reverse_string(n))
```

In either case, we get the flag:

```
HTB{r3VerS4l?_wElL_1_n3vEr_8d6e35b9258902e2be9335a4d7726ccf}
```