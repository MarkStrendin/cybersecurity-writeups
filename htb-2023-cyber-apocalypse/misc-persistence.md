---
layout: default
title: Persistence
---

# [Cyber Apocalypse 2023](index.md) - Misc - Persistence

> Thousands of years ago, sending a GET request to /flag would grant immense power and wisdom. Now it's broken and usually returns random data, but keep trying, and you might get lucky... Legends say it works once every 1000 tries.

So, write a script that hits the given web server 1000 times and get the flag. Seems simple enough, and is a chance to practice some more Python.

```python
import requests, time

url = "http://IP AND PORT GO HERE"

found_flag = False
count = 0
while found_flag == False:
    response = requests.get(url + "/flag")
    potential_flag = response.text.replace('\n','')
    found_flag = potential_flag.startswith("HTB{")
    count = count + 1
    print(count,": ", potential_flag)

print("FLAG FOUND")
print(potential_flag)
```
Letting this run for a while, we get the flag.

```
512 :  3,:.A_c=YV2aRns7L{TYxRv
513 :  50NbqfybXTH.|RK
514 :  q>y]r4g4hw*c!=4v~plLUK6W
515 :  4UY?19(,q1_s:=mVV[Ru>@)fVofV
516 :  :2'G~_vcOy[yVUr+){?>t6sdh~-N^
517 :  HTB{y0u_h4v3_p0w3rfuL_sCr1pt1ng_ab1lit13S!}
FLAG FOUND
HTB{y0u_h4v3_p0w3rfuL_sCr1pt1ng_ab1lit13S!}
```
I did a lot of testing, but not _that_ much, so it's not every 1000 requests, it's a 1/1000 chance - so it's a good thing I wrote the script to check for `HTB{` and not just count 1000 requests.

```
HTB{y0u_h4v3_p0w3rfuL_sCr1pt1ng_ab1lit13S!}
```