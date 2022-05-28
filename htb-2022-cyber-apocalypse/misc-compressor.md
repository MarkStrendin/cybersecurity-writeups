---
layout: default
title: Compressor
---

# [Cyber Apocalypse](index.md) - Misc - Compressor

> Ramona's obsession with modifications and the addition of artifacts to her body has slowed her down and made her fail and almost get killed in many missions. For this reason, she decided to hack a tiny robot under Golden Fang's ownership called "Compressor", which can reduce and increase the volume of any object to minimize/maximize it according to the needs of the mission. With this item, she will be able to carry any spare part she needs without adding extra weight to her back, making her fast. Can you help her take it and hack it?

This challenge was a remote server that you connect to with a terminal (like telnet).

The menu you were presented with gave you options for different robot body parts, and allowed you to run specific commands that created files, `cat`'ed files, `zip`'ed files, and `rm`'ed files.

Some of the commands - notably `cat` and `zip` prompted for optional paramenters.

I spent too much time trying to exploit `zip`, and was successful in getting it to compress files outside of it's directory (possibly including the flag), but with no way to access or extract the zip file, this was not very successful.

Then I noticed that the option to `cat` a file asks for a filename, and doesn't sanitize it's input. I was able to tell it `cat file.txt ; pwd` and `cat file.txt ; ls` to explore the server's file structure. I found the flag in `/home/ctf/flag.txt`, and was able to use the command `cat file.txt ; cat /home/ctf/flag.txt` to retrieve it.

## Alternate way to solve this

You can also exploit the `zip` command to give yourself a shell.
Connect using `nc` rather than `telnet`.

1. Create an artifact
2. Choose "Compress artifact" from the menu
3. Enter any name
4. Enter the name of the file you made in step 1
5. For options, type in, type `-T --unzip-command 'sh -c /bin/sh`
6. It will add the file, and then dump you to a shell. Use `pwd`, `ls`, and `cd ..` to explore the file system.
7. 2 directories up from where you started, in `/home/ctf`, you'll find `flag.txt`. Issuing the command `cat /home/ctf/flag.txt`