---
layout: default
title: Remote Computation
---

# [Cyber Apocalypse 2023](index.md) - Misc - Remote Computation

> The alien species use remote machines for all their computation needs. Pandora managed to hack into one, but broke its functionality in the process. Incoming computation requests need to be calculated and answered rapidly, in order to not alarm the aliens and ultimately pivot to other parts of their network. Not all requests are valid though, and appropriate error messages need to be sent depending on the type of error. Can you buy us some time by correctly responding to the next 500 requests?

We're given a docker container that we can spawn and connect to.

Connecting to it we get a menu:

```
$ nc 64.227.41.83 30836
[-MENU-]
[1] Start
[2] Help
[3] Exit
>
```

`1` starts the math problems coming. We're expected to solve 500 of these.
`2` shows some help, and shows us the curve-balls they'll be sending us:

```
Results
---
All results are rounded
to 2 digits after the point.
ex. 9.5752 -> 9.58

Error Codes
---
* Divide by 0:
This may be alien technology,
but dividing by zero is still an error!
Expected response: DIV0_ERR

* Syntax Error
Invalid expressions due syntax errors.
ex. 3 +* 4 = ?
Expected response: SYNTAX_ERR

* Memory Error
The remote machine is blazingly fast,
but its architecture cannot represent any result
outside the range -1337.00 <= RESULT <= 1337.00
Expected response: MEM_ERR
```

 * Some equations it sends will have invalid syntax that we'll have to account for - specifically two operators next to each-other (ie: `23 +* 5`)
 * Some equations will cause division-by-zero errors, and we're expected to send back a specific error code when this happens
 * Answers must be between `-1337.00` and `1337.00`, and if they are not, we're expected to send a specific error code back
 * Answers must be given to two decimal places

Now that we know the rules, time to write some Python. I don't know Python especially well, so this was a good opportunity to learn more about how it works. The code below took me several hours of tinkering to write.

```py
import telnetlib, re

def strip_bad_characters(instr):
    return re.sub("[^0-9\-\+\/\* \(\)]", "", instr)

def calculate_response(equation):
    safe_equation = strip_bad_characters(equation)
    try:
        answer = round(eval(safe_equation), 2)
    except ZeroDivisionError:
        return "DIV0_ERR"
    except SyntaxError:
        return "SYNTAX_ERR"

    if answer > 1337.00:
        return "MEM_ERR"
    if answer < -1337.00:
        return "MEM_ERR"

    return str(answer)

def parse_response(response):
    re_groups = re.search(b"[.|\n]*\[(\d+)\]\: (.*) =.*", response)
    question_number = int(re_groups.group(1))
    equation = str(re_groups.group(2).decode("ascii"))
    response = calculate_response(equation)
    return (question_number, response, equation)

telnet = telnetlib.Telnet("64.227.41.83","30836")

telnet.read_until(b">")
telnet.write(b'1\n')

# Get into the loop
question_number = 0
while question_number < 500:
    # Read question
    response = telnet.read_until(b">")
    question_number, answer, equation = parse_response(response)
    print("%03d" % question_number,": ", equation, " = ", answer)

    # Send response
    telnet.write(answer.encode("ascii"))
    telnet.write(b"\n")

# Read everything that it gives us after
print(str(telnet.read_until(b">").decode("ascii")))

telnet.close
```

I added in code to check to make sure that only numbers and equation-related characters would show up - since I was using `eval()` to calculate the equations, I was expecting to see an equation show up that ran some naughty code. No such code seemed to come in, but... now I don't have to worry about it.

When it finishes, we get the flag.

```
496 :  22 * 9 * 2 + 16 * 20 / 15  =  417.33
497 :  9 + 22 * 18 * 25 - 12 - 17 - 27 * 14 * 16 + 26 + 3 / 26 * 6 / 19  =  MEM_ERR
498 :  13 / 9 / 23 - 19 - 3 / 4 * 24 - 6 - 8 + 13 / 10 + 19  =  -30.64
499 :  10 / 9 - 16 + 17 * 16 / 13 - 13 / 2 + 23 - 14 - 19 * 7 * 9 / 27 + 29  =  -6.8
500 :  19 * 7 - 20 + 6 + 26 / 6 / 12 - 26 + 14  =  107.36
 [*] Good job! HTB{d1v1d3_bY_Z3r0_3rr0r}
```