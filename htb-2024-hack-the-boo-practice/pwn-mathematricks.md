---
layout: default
title: Mathematricks
---

# [Hack The Boo 2024 - Practice](index.md) - Pwn - Mathematricks

> How about a magic trick? Or a math trick? Beat me and I will give you an amazing reward!

We are given a zip file containing the binary, a python script for interacting with the binary programatically, and a docker container that we can start that runs the binary on the CTF servers. Presumably the binary we download will contain a fake flag, and the "live" one running on the CTF servers will give us the real flag.

The included Python script is designed to interact with the binary running on the CTF systems, and we can modify it to give different answers. I didn't end up using this, and I can't imagine that it would be more efficient than doing this challenge by hand, but its useful to see an example script that can interact with a CTF challenge - this may come in handy for later challenges.

Starting the challenge in a Docker container and using `nc` to connect to it, we can see that it asks us some math problems.

```

        🎉 ~~ w3lC0m3 2 tH3 M4th3M4tR1kCs c0nt35t ~~ 🎉

                        ■ ■ ■ ■ ■ ■ ■
                        ■           ■
                        ■ 1. Play   ■
                        ■ 2. Rules  ■
                        ■           ■
                        ■ ■ ■ ■ ■ ■ ■

                        🥸 1

                🎉 ~~ Let the game begin! ~~ 🎉

                Q1: 1 + 1 = ?

                > 2

                [+] THAT WAS AMAZING!

                Q2: 2 - 1 = ?

                > 1

                [+] WE HAVE A MATHEMATICIAN AMONG US!

                Q3: 1337 - 1337 = ?

                > 0
```

Extremely simple so far, then the final question...

```
                [+] GOD OF MATHS JUST ENTERED THE CHAT..

                Q4: Enter 2 numbers n1, n2 where n1 > 0 and n2 > 0 and n1 + n2 < 0

```

So we need two numbers that are both positive, but when added together result in a negative number.
I don't believe this is possible in normal mathematics, but inside a computer, we have variables that can be overflowed. If the number variable is an (signed) INT, and we give it the maximum number an INT can hold as one number, and then any positive number for the second, it will overflow and we'll get a negative number. 

Quickly looking up the maximum number for a signed integer we find that it's 2,147,483,647. So if we can give it two numbers that when added together, would result in a number larger than 2147483647, it should overflow to a negative, and it should solve the challenge.

```
                Q4: Enter 2 numbers n1, n2 where n1 > 0 and n2 > 0 and n1 + n2 < 0

                n1: 2000000000

                n2: 2000000000
HTB{m4th3m4tINT_5tuff_6bc8ef60927c884a2c366791ca63efa0}
```

And we are given the flag.

```
HTB{m4th3m4tINT_5tuff_6bc8ef60927c884a2c366791ca63efa0}
```