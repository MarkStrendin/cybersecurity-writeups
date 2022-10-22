---
layout: default
title: Cult Meeting
---

# [Hack The Boo](index.md) - Reversing - Cult Meeting

**Difficulty:** Easy
> After months of research, you're ready to attempt to infiltrate the meeting of a shadowy cult. Unfortunately, it looks like they've changed their password!

We are provided a binary, and can launch a Docker container that is running this binary.

Connecting to the Docker container, we see that it asks for a password.

```sh
$ telnet 167.71.137.174 30425
Trying 167.71.137.174...
Connected to 167.71.137.174.
Escape character is '^]'.
You knock on the door and a panel slides back
|/👁️ 👁️ \|   A hooded figure looks out at you
"What is the password for this week's meeting?" sdfsf
sdfsf

   \/
|/👁️ 👁️ \| "That's not our password - call the guards!"
Connection closed by foreign host.
```

Opening the provided binary in Ghidra, and finding the `main` class, we can see that it's fairly simple.

```c
undefined8 main(void)

{
  int iVar1;
  char *pcVar2;
  char local_48 [64];

  setvbuf(stdout,(char *)0x0,2,0);
  puts("\x1b[3mYou knock on the door and a panel slides back\x1b[0m");
  puts(&DAT_00102040);
  fwrite("\"What is the password for this week\'s meeting?\" ",1,0x30,stdout);
  fgets(local_48,0x40,stdin);
  pcVar2 = strchr(local_48,10);
  *pcVar2 = '\0';
  iVar1 = strcmp(local_48,"sup3r_s3cr3t_p455w0rd_f0r_u!");
  if (iVar1 == 0) {
    puts("\x1b[3mThe panel slides closed and the lock clicks\x1b[0m");
    puts("|      | \"Welcome inside...\" ");
    system("/bin/sh");
  }
  else {
    puts("   \\/");
    puts(&DAT_00102130);
  }
  return 0;
}

```
It looks like this program asks the user for a password...

```c
fwrite("\"What is the password for this week\'s meeting?\" ",1,0x30,stdout);
fgets(local_48,0x40,stdin);
```

And the compares it to see if it's the expected password.

```c
iVar1 = strcmp(local_48,"sup3r_s3cr3t_p455w0rd_f0r_u!");
```

and if we know the password, it gives us a shell:
```c
puts("|      | \"Welcome inside...\" ");
system("/bin/sh");
```

Lets try to telnet to the live version of this challenge and see if this password works.

```sh
$ telnet 167.71.137.174 30425
Trying 167.71.137.174...
Connected to 167.71.137.174.
Escape character is '^]'.
You knock on the door and a panel slides back
|/👁️ 👁️ \|   A hooded figure looks out at you
"What is the password for this week's meeting?" sup3r_s3cr3t_p455w0rd_f0r_u!
sup3r_s3cr3t_p455w0rd_f0r_u!

The panel slides closed and the lock clicks
|      | "Welcome inside..."
/bin/sh: 0: can't access tty; job control turned off
$ $
```
Looks like it worked, and we get a shell.

```bash
$ $ ls
ls

flag.txt  meeting
$ $ cat flag.txt
cat flag.txt

HTB{1nf1ltr4t1ng_4_cul7_0f_str1ng5}
```
and we find our flag: `HTB{1nf1ltr4t1ng_4_cul7_0f_str1ng5}`

# A simpler method
Using Ghidra was a bit overkill for this challenge - we could have just used `strings`.

```sh
$ strings meeting
/lib64/ld-linux-x86-64.so.2
mgUa
puts
stdin
fgets
stdout
system
fwrite
strchr
__cxa_finalize
setvbuf
strcmp
__libc_start_main
libc.so.6
GLIBC_2.2.5
_ITM_deregisterTMCloneTable
__gmon_start__
_ITM_registerTMCloneTable
u/UH
[]A\A]A^A_
[3mYou knock on the door and a panel slides back
[3m A hooded figure looks out at you
"What is the password for this week's meeting?"
sup3r_s3cr3t_p455w0rd_f0r_u!
[3mThe panel slides closed and the lock clicks
|      | "Welcome inside..."
/bin/sh
   \/
 \| "That's not our password - call the guards!"
;*3$"
GCC: (Debian 10.2.1-6) 10.2.1 20210110
crtstuff.c
deregister_tm_clones
__do_global_dtors_aux
completed.0
...
```
The password stands out in this list because of the characters it uses, and because it even includes the word "password".

If this were not an "Easy" CTF challenge, the password may not have been so obvious, and this method may not have worked.

# Takeaways
- Don't store passwords in your code in plaintext
- Don't store passwords in your code at all, ideally