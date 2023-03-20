---
layout: default
title: She Shells C Shells
---

# [Cyber Apocalypse 2023](index.md) - Reversing - She Shells C Shells

> You've arrived in the Galactic Archive, sure that a critical clue is hidden here. You wait anxiously for a terminal to boot up, hiding in the shadows from the guards hunting for you. Unfortunately, it looks like you'll need a password to get what you need without setting off the alarms...

When doing reversing challenges, I like to run `strings` against the binary to see if the flag happens to be visible there. If it is, it can save me a ton of time trying to reverse engineer code.

```
$ strings shell | grep HTB

```
Nothing.

Running the binary (which is _probably_ a bad idea in most cases) shows us that this is actually a little command shell.

```
$ ./shell
ctfsh-$ help
ls: ls [directory] - lists files in a directory
whoami: whoami - prints the current user's name
cat: cat [files...] - prints out a sequence of files
getflag: admin only
ctfsh-$
```
There's a `getflag` function that asks for a password, so that where we should focus our attention.

```
ctfsh-$ getflag
Password:
```
