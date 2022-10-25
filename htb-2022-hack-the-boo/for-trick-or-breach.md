---
layout: default
title: Trick Or Breach
---

# [Hack The Boo](index.md) - Forensics - Trick Or Breach
**Difficulty:** Easy

> Our company has been working on a secret project for almost a year. None knows about the subject, although rumor is that it is about an old Halloween legend where an old witch in the woods invented a potion to bring pumpkins to life, but in a more up-to-date approach. Unfortunately, we learned that malicious actors accessed our network in a massive cyber attack. Our security team found that the hack had occurred when a group of children came into the office's security external room for trick or treat. One of the children was found to be a paid actor and managed to insert a USB into one of the security personnel's computers, which allowed the hackers to gain access to the company's systems. We only have a network capture during the time of the incident. Can you find out if they stole the secret project?

We are provided with a pcap file containing of *only* DNS queries.

```
1	0.000000	192.168.1.10	147.182.172.189	DNS	126	Standard query 0xa49f A 504b0304140008080800a52c47550000000000000000000000.pumpkincorp.com
```

It's obvious that the DNS queries are being used to transmit encoded data - but the method is not immediately obvious.
The values appear to be hex, padded out to 50 characters (before the `.pumpkincorp.com`) by zeros.

I left this challenge here to pursue other challenges, and think about how this data might be decoded.