---
layout: default
title: Space Pirate: Entrypoint
---

# Space Pirate: Entrypoint

This challenge is done via a remote connection to a server over telnet (or Netcat probably would have worked as well).
We were provided the binary for this challenge, which could be decompiled using a program like Ghidra.

Before I did that, I connected to the challenge server to see what the program was *supposed* to do. It asks for a password, and basically anything you type in that *isn't* the password will give you the flag right away. 

I was unsure if this was how it was supposed to work, but decided to take the win and move on. I did not bother to decompile it.

So I guess this isn't much of a write-up - either it was an extremely easy challenge designed to trap people who would overthink it, or it was broken.