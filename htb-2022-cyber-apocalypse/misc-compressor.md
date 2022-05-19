---
layout: default
title: Compressor
---

# [Cyber Apocalypse](index.md) - Misc - Compressor

This challenge was a remote server that you connect to with a terminal (like telnet).

The menu you were presented with gave you options for different robot body parts, and allowed you to run specific commands that created files, `cat`'ed files, `zip`'ed files, and `rm`'ed files.

Some of the commands - notably `cat` and `zip` prompted for optional paramenters.

I spent too much time trying to exploit `zip`, and was successful in getting it to compress files outside of it's directory (possibly including the flag), but with no way to access or extract the zip file, this was not very successful.

Then I noticed that the option to `cat` a file asks for a filename, and doesn't sanitize it's input. I was able to tell it `cat file.txt ; pwd` and `cat file.txt ; ls` to explore the server's file structure. I found the flag in `/home/ctf/flag.txt`, and was able to use the command `cat file.txt ; cat /home/ctf/flag.txt` to retrieve it.
