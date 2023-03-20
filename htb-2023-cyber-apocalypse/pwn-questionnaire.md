---
layout: default
title: Questionnaire
---

# [Cyber Apocalypse 2023](index.md) - Pwn - Questionnaire

> It's time to learn some things about binaries and basic c. Connect to a remote server and answer some questions to get the flag.

We're given a zip file with some source code and a compiled binary, and a spawnable docker container.

This challenge is really just some reading about how compiling and buffer overflows work, and it gives you the answers, either in the accompanying zip file or in the preamble before each question.

```
This is a simple questionnaire to get started with the basics.

◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉
◉                                                                                                       ◉
◉  When compiling C/C++ source code in Linux, an ELF (Executable and Linkable Format) file is created.  ◉
◉  The flags added when compiling can affect the binary in various ways, like the protections.          ◉
◉  Another thing affected can be the architecture and the way it's linked.                              ◉
◉                                                                                                       ◉
◉  If the system in which the challenge is compiled is x86_64 and no flag is specified,                 ◉
◉  the ELF would be x86-64 / 64-bit. If it's compiled with a flag to indicate the system,               ◉
◉  it can be x86 / 32-bit binary.                                                                       ◉
◉                                                                                                       ◉
◉  To reduce its size and make debugging more difficult, the binary can be stripped or not stripped.    ◉
◉                                                                                                       ◉
◉  Dynamic linking:                                                                                     ◉
◉                                                                                                       ◉
◉  A pointer to the linked file is included in the executable, and the file contents are not included   ◉
◉  at link time. These files are used when the program is run.                                          ◉
◉                                                                                                       ◉
◉  Static linking:                                                                                      ◉
◉                                                                                                       ◉
◉  The code for all the routines called by your program becomes part of the executable file.            ◉
◉                                                                                                       ◉
◉  Stripped:                                                                                            ◉
◉                                                                                                       ◉
◉  The binary does not contain debugging information.                                                   ◉
◉                                                                                                       ◉
◉  Not Stripped:                                                                                        ◉
◉                                                                                                       ◉
◉  The binary contains debugging information.                                                           ◉
◉                                                                                                       ◉
◉  The most common protections in a binary are:                                                         ◉
◉                                                                                                       ◉
◉  Canary: A random value that is generated, put on the stack, and checked before that function is      ◉
◉  left again. If the canary value is not correct-has been changed or overwritten, the application will ◉
◉  immediately stop.                                                                                    ◉
◉                                                                                                       ◉
◉  NX: Stands for non-executable segments, meaning we cannot write and execute code on the stack.       ◉
◉                                                                                                       ◉
◉  PIE: Stands for Position Independent Executable, which randomizes the base address of the binary     ◉
◉  as it tells the loader which virtual address it should use.                                          ◉
◉                                                                                                       ◉
◉  RelRO: Stands for Relocation Read-Only. The headers of the binary are marked as read-only.           ◉
◉                                                                                                       ◉
◉  Run the 'file' command in the terminal and 'checksec' inside the debugger.                           ◉
◉                                                                                                       ◉
◉  The output of 'file' command:                                                                        ◉
◉                                                                                                       ◉
◉  ✗ file test                                                                                          ◉
◉  test: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked,                       ◉
◉  interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=5a83587fbda6ad7b1aeee2d59f027a882bf2a429,     ◉
◉  for GNU/Linux 3.2.0, not stripped.                                                                   ◉
◉                                                                                                       ◉
◉  The output of 'checksec' command:                                                                    ◉
◉                                                                                                       ◉
◉  gef➤  checksec                                                                                       ◉
◉  Canary                        : ✘                                                                    ◉
◉  NX                            : ✓                                                                    ◉
◉  PIE                           : ✘                                                                    ◉
◉  Fortify                       : ✘                                                                    ◉
◉  RelRO                         : Partial                                                              ◉
◉                                                                                                       ◉
◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉

[*] Question number 0x1:

Is this a '32-bit' or '64-bit' ELF? (e.g. 1337-bit)

>>
```
Running the `file` command on the provided binary provides us with most of the answers in this section.

```
test: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=5a83587fbda6ad7b1aeee2d59f027a882bf2a429, for GNU/Linux 3.2.0, not stripped
```
So the answer to the first question is `64-bit`

```
>> 64-bit

♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠
♠                   ♠
♠      Correct      ♠
♠                   ♠
♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠

[*] Question number 0x2:

What's the linking of the binary? (e.g. static, dynamic)

```

The output of the `file` command says "dynamically linked", so the answer here is "dynamic"

```
>> dynamic

♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠
♠                   ♠
♠      Correct      ♠
♠                   ♠
♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠

[*] Question number 0x3:

Is the binary 'stripped' or 'not stripped'?

```
`file` says our file is "not stripped".

```
>> not stripped

♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠
♠                   ♠
♠      Correct      ♠
♠                   ♠
♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠

[*] Question number 0x4:

Which protections are enabled (Canary, NX, PIE, Fortify)?
```
The text at the start of this section gives us this answer (NX), but if we wanted to find this for ourselves, we'll need `gdb` and the `gef` extension for it.

`gdb` is the GBU Debugger, and on most debian-based systems it can be installed with `apt install gbd`.

`gef` can be found at https://github.com/hugsy/gef, and has an "instant setup" script in the readme.

With both installed, we can run the following to load the `test` binary into the debugger:
```
gdb test
```
Remembering that `test` is the name of the binary, not a parameter of `gdb`.

We can now simply type `checksec` and get the answer:

```
Reading symbols from test...
(No debugging symbols found in test)
gef➤  checksec
[+] checksec for '/home/security/htb/test'
[*] .gef-2b72f5d0d9f0f218a91cd1ca5148e45923b950d5.py:L8764 'checksec' is deprecated and will be removed in a feature release. Use Elf(fname).checksec()
Canary                        : ✘
NX                            : ✓
PIE                           : ✘
Fortify                       : ✘
RelRO                         : Partial
gef➤
```
"NX" is checked, and that's the answer.

```
>> NX

♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠
♠                   ♠
♠      Correct      ♠
♠                   ♠
♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠
◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉
◉                                                                                                       ◉
◉  Great job so far! Now it's time to see some C code and a binary file.                                ◉
◉                                                                                                       ◉
◉  In the pwn_questionnaire.zip there are two files:                                                    ◉
◉                                                                                                       ◉
◉  1. test.c                                                                                            ◉
◉  2. test                                                                                              ◉
◉                                                                                                       ◉
◉  The 'test.c' is the source code and 'test' is the output binary.                                     ◉
◉                                                                                                       ◉
◉  Let's start by analyzing the code.                                                                   ◉
◉  First of all, let's focus on the '#include <stdio.h>' line.                                          ◉
◉  It includes the 'stdio.h' header file to use some of the standard functions like 'printf()'.         ◉
◉  The same principle applies for the '#include <stdlib.h>' line, for other functions like 'system()'.  ◉
◉                                                                                                       ◉
◉  Now, let's take a closer look at:                                                                    ◉
◉                                                                                                       ◉
◉  void main(){                                                                                         ◉
◉      vuln();                                                                                          ◉
◉  }                                                                                                    ◉
◉                                                                                                       ◉
◉  By default, a binary file starts executing from the 'main()' function.                               ◉
◉                                                                                                       ◉
◉  In this case, 'main()' only calls another function, 'vuln()'.                                        ◉
◉  The function 'vuln()' has 3 lines.                                                                   ◉
◉                                                                                                       ◉
◉  void vuln(){                                                                                         ◉
◉      char buffer[0x20] = {0};                                                                         ◉
◉      fprintf(stdout, "\nEnter payload here: ");                                                       ◉
◉      fgets(buffer, 0x100, stdin);                                                                     ◉
◉  }                                                                                                    ◉
◉                                                                                                       ◉
◉  The first line declares a 0x20-byte buffer of characters and fills it with zeros.                    ◉
◉  The second line calls 'fprintf()' to print a message to stdout.                                      ◉
◉  Finally, the third line calls 'fgets()' to read 0x100 bytes from stdin and store them to the         ◉
◉  aformentioned buffer.                                                                                ◉
◉                                                                                                       ◉
◉  Then, there is a custom 'gg()' function which calls the standard 'system()' function to print the    ◉
◉  flag. This function is never called by default.                                                      ◉
◉                                                                                                       ◉
◉  void gg(){                                                                                           ◉
◉      system("cat flag.txt");                                                                          ◉
◉  }                                                                                                    ◉
◉                                                                                                       ◉
◉  Run the 'man <function_name>' command to see the manual page of a standard function (e.g. man fgets).◉
◉                                                                                                       ◉
◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉

[*] Question number 0x5:

What is the name of the custom function that gets called inside `main()`? (e.g. vulnerable_function())

>>
```

Now we need to look at the provided source code.

```c
#include <stdio.h>
#include <stdlib.h>

/*
This is not the challenge, just a template to answer the questions.
To get the flag, answer the questions.
There is no bug in the questionnaire.
*/

void gg(){
	system("cat flag.txt");
}

void vuln(){
	char buffer[0x20] = {0};
	fprintf(stdout, "\nEnter payload here: ");
	fgets(buffer, 0x100, stdin);
}

void main(){
	vuln();
}
```

The only thing that `main()` does is run `vuln()`, so that's the answer we're looking for here. It's a function, so it needs `()` at the end of it to signify this.

```
>> vuln()

♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠
♠                   ♠
♠      Correct      ♠
♠                   ♠
♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠

[*] Question number 0x6:

What is the size of the 'buffer' (in hex or decimal)?

>>
```
The buffer refers to the variable named `buffer`:

```
char buffer[0x20] = {0};
```
The value in the square brackets determines it's size. It starts with `0x`, which means that this is a hexadecimal number. The challenge will accept `0x20`, or it's converted decimal value, `32`.

```
>> 0x20

♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠
♠                   ♠
♠      Correct      ♠
♠                   ♠
♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠

[*] Question number 0x7:

Which custom function is never called? (e.g. vuln())

>>
```
We've seen `main()` and `vuln()` get called, but `gg()` has not - this is the answer they're looking for. It's a function, so it needs `()` at the end of it to signify this.

```
>> gg()

♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠
♠                   ♠
♠      Correct      ♠
♠                   ♠
♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠
◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉
◉                                                                                                       ◉
◉  Excellent! Now it's time to talk about Buffer Overflows.                                             ◉
◉                                                                                                       ◉
◉  Buffer Overflow means there is a buffer of characters, integers or any other type of variables,      ◉
◉  and someone inserts into this buffer more bytes than it can store.                                   ◉
◉                                                                                                       ◉
◉  If the user inserts more bytes than the buffer's size, they will be stored somewhere in the memory   ◉
◉  after the address of the buffer, overwriting important addresses for the flow of the program.        ◉
◉  This, in most cases, will make the program crash.                                                    ◉
◉                                                                                                       ◉
◉  When a function is called, the program knows where to return because of the 'return address'. If the ◉
◉  player overwrites this address, they can redirect the flow of the program wherever they want.        ◉
◉  To print a function's address, run 'p <function_name>' inside 'gdb'. (e.g. p main)                   ◉
◉                                                                                                       ◉
◉  gef➤  p gg                                                                                           ◉
◉  $1 = {<text variable, no debug info>} 0x401176 <gg>                                                  ◉
◉                                                                                                       ◉
◉  To perform a Buffer Overflow in the simplest way, we take these things into consideration.           ◉
◉                                                                                                       ◉
◉  1. Canary is disabled so it won't quit after the canary address is overwritten.                      ◉
◉  2. PIE is disabled so the addresses of the binary functions are not randomized and the user knows    ◉
◉     where to return after overwritting the return address.                                            ◉
◉  3. There is a buffer with N size.                                                                    ◉
◉  4. There is a function that reads to this buffer more than N bytes.                                  ◉
◉                                                                                                       ◉
◉  Run printf 'A%.0s' {1..30} | ./test to enter 30*"A" into the program.                                ◉
◉                                                                                                       ◉
◉  Run the program manually with "./test" and insert 30*A, then 39, then 40 and see what happens.       ◉
◉                                                                                                       ◉
◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉

[*] Question number 0x8:

What is the name of the standard function that could trigger a Buffer Overflow? (e.g. fprintf())

>>
```
This question is worded a bit confusing if you don't immediately understand what it's asking.
In the code, we can see the `vuln()` function only really has 3 lines of code, and it calls two functions - `fprintf()` and `fgets()`. The answer it's looking for is `fgets()`. It's a function, so it needs `()` at the end of it to signify this.

```
>> fgets()

♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠
♠                   ♠
♠      Correct      ♠
♠                   ♠
♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠

[*] Question number 0x9:

Insert 30, then 39, then 40 'A's in the program and see the output.

After how many bytes a Segmentation Fault occurs (in hex or decimal)?

>>
```

The text for this section explains _how_ we can find out, but for me, actually doing this took a few extra steps. I happened to be using a Debian based Linux system that had not yet updated it's packages to include the required version of libc:

```
> ./test
./test: /lib/x86_64-linux-gnu/libc.so.6: version `GLIBC_2.34' not found (required by ./test)
```
Apparently this issue should be fixed in the next major release of Debian... so I switched to a system running Kali linux instead, and it was able to run the binary just fine.

It wants us to run `printf 'A%.0s' {1..30} | ./test` with varying levels of characters to see which one crashes the program.

```
$ printf 'A%.0s' {1..39} | ./test

Enter payload here:
```
When we use `39`, it still appears to function normally, same as if we typed something in ourselves.

```
$ printf 'A%.0s' {1..40} | ./test

Enter payload here:
Enter payload here:
```
At `40`, it shows us the prompt twice for some reason.

```
$ printf 'A%.0s' {1..41} | ./test

Segmentation fault
```
At `41`, we get a segmentation fault. The question says __after__ how many bytes a segmentation fault occurs - `41` is where it started, which is after `40`, so `40` is the answer (and thankfully there is no penalty for putting in the wrong answer if you put `41`.)

```
>> 41

♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠
♠                 ♠
♠      Wrong      ♠
♠                 ♠
♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠

[*] Question number 0x9:

Insert 30, then 39, then 40 'A's in the program and see the output.

After how many bytes a Segmentation Fault occurs (in hex or decimal)?

>> 40

♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠
♠                   ♠
♠      Correct      ♠
♠                   ♠
♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠

[*] Question number 0xa:

What is the address of 'gg()' in hex? (e.g. 0x401337)

>>
```
The text at the start of this section explains how to find this with `gdb`, and even just gives us the answer.

If we want to get the answer ourselves, we can load up the binary in `gdb`.

```
gdb test
```
and then use the `p` command in `gdb`, with the name of the function we want to check, which is `gg` in this case.

```
Reading symbols from test...
(No debugging symbols found in test)
gef➤  p gg
$1 = {<text variable, no debug info>} 0x401176 <gg>
gef➤
```
Memory addresses are in hex - the answer here is `0x401176`.

```
>> 0x401176

♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠
♠                   ♠
♠      Correct      ♠
♠                   ♠
♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠ ♠

Great job! It's high time you solved your first challenge! Here is the flag!

HTB{th30ry_bef0r3_4cti0n}
```

And we're done. No challenge, exactly, just a quick tutorial on some things you might look for in a "pwn" challenge.