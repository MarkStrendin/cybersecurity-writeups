---
layout: default
title: Pumpkin Stand
---

# [Hack The Boo](index.md) - Pwn - Pumpkin Stand
**Difficulty:** Easy

> This time of the year, we host our big festival and the one who craves the pumpkin faster and make it as scary as possible, gets an amazing prize! Be fast and try to crave this hard pumpkin!

We are provided a binary.

Decompiling the binary with Ghidra, we see that the application sticks us in 4 `while` loops, each with it's own `if` statement that will break out of the loop if certain criteria are met.

```c
  while( true ) {
    while( true ) {
      while( true ) {
        while( true ) {
          menu();
          __isoc99_scanf(&DAT_0010132b,&menu_item_selection);
          printf("\nHow many do you want?\n\n>> ");
          __isoc99_scanf(&DAT_0010132b,&quantity_selection);
          if (0 < quantity_selection) break;
          printf("%s\n[-] You cannot buy less than 1!\n",&DAT_0010134a);
        }
        pumpcoins = pumpcoins -
                    quantity_selection *
                    (short)*(undefined4 *)((long)&values + (long)(int)menu_item_selection * 4);
        if (-1 < pumpcoins) break;
        printf("\nCurrent pumpcoins: [%s%d%s]\n\n",&DAT_00100e80,(ulong)(uint)(int)pumpcoins);
        printf("%s\n[-] Not enough pumpcoins for this!\n\n%s",&DAT_0010134a,&DAT_00100e78);
      }
      if (menu_item_selection != 1) break;
      printf("\nCurrent pumpcoins: [%s%d%s]\n\n",&DAT_00100e80,(ulong)(uint)(int)pumpcoins);
      puts("\nGood luck crafting this huge pumpkin with a shovel!\n");
    }
    if (0x270e < pumpcoins) break;
    printf("%s\n[-] Not enough pumpcoins for this!\n\n%s",&DAT_0010134a,&DAT_00100e78);
  }
  local_48 = 0;
  local_40 = 0;
  local_38 = 0;
  local_30 = 0;
  local_28 = 0;
  local_20 = 0;
  flag_file_contents = fopen("./flag.txt","rb");
  if (flag_file_contents != (FILE *)0x0) {
    fgets((char *)&local_48,0x30,flag_file_contents);
    printf("%s\nCongratulations, here is the code to get your laser:\n\n%s\n\n",&DAT_00100ee3,
           &local_48);
    exit(0x16);
  }
```

If we break out of all of the loops, it will show us the flag.

From inner-most to outer-most, the criteria that we need to meet to break out of the loops are:
- The menu item we select must be greater than `0`
- We must have more than `-1` coins
- The menu item we select must not equal `1`
- Our coins must be greater than `9998` (`0x270e` in hex = `9998` in decimal)

We can see that the math used to calculate "pumpcoins" each loop iteration is as follows:
```c
pumpcoins = pumpcoins - quantity_selection * (short)*(undefined4 *)((long)&values + (long)(int)menu_item_selection * 4);
```

This looks a bit.. wonky... but this looks like it'll be what we need to abuse to break out of the loops.

The new coin value is calculated regardless of if we have enough coins or not, so if we continue to buy shovels, we quickly go into the negative.
The coin value is a signed small integer, meaning it can store values between `–32,767` and `32,767`. If we get this value over `32767` or under `-32767`, it will wrap around - `32767 + 1` will get us `-32767`, and vice-versa.

```
Current pumpcoins: [1337]

Items:

1. Shovel  (1337 p.c.)
2. Laser   (9999 p.c.)

>> 1

How many do you want?

>> 2

Current pumpcoins: [-1337]


[-] Not enough pumpcoins for this!


Current pumpcoins: [-1337]

Items:

1. Shovel  (1337 p.c.)
2. Laser   (9999 p.c.)

>>
```

No matter what quantity we select, if we choose option 2 - the laser - our coins get reset to zero.

We can easily get our coin count above 9998 by buying enough shovels to cost more than 32767 coins. 26 shovels is just enough for this, giving us 32111 coins.

```
Current pumpcoins: [1337]

Items:

1. Shovel  (1337 p.c.)
2. Laser   (9999 p.c.)

>> 1

How many do you want?

>> 26

Current pumpcoins: [32111]


Good luck crafting this huge pumpkin with a shovel!


Current pumpcoins: [32111]

Items:

1. Shovel  (1337 p.c.)
2. Laser   (9999 p.c.)

>>
```

We can see the string `Good luck crafting this huge pumpkin with a shovel!`, so we know we're in the second-last loop - only one more to break out of and we'll get the flag.

Selecting option 1 will only keep us in the loop - we could potentially stay here forever wrapping the coin amount from negative to positive... that is, if the program didn't automatically kick us out after about 2 minutes.
Selecting option 2 will reset our coins to zero.
Selecting any other small integer will exit the last loop, keeping our coin values the same so that we're still breaking out of the other inner loops. Selecting menu option 3, quantity 1, from the menu will get us the flag.

```

                                          ##&
                                        (#&&
                                       ##&&
                                 ,*.  #%%&  .*,
                      .&@@@@#@@@&@@@@@@@@@@@@&@@&@#@@@@@@(
                    /@@@@&@&@@@@@@@@@&&&&&&&@@@@@@@@@@@&@@@@,
                   @@@@@@@@@@@@@&@&&&&&&&&&&&&&@&@@@@@@&@@@@@@
                 #&@@@@@@@@@@@@@@&&&&&&&&&&&&&&&#@@@@@@@@@@@@@@,
                .@@@@@#@@@@@@@@#&&&&&&&&&&&&&&&&&#@@@@@@@@@@@@@&
                &@@@@@@@@@@@@@@&&&&&&&&&&&&&&&&&&&@@@@@@@@@@@@@@@
                @@@@@@@@@@@@@@&&&&&&&&&&&&&&&&&&&&@@@@@@@@@&@@@@@
                @@@@@@@@@@@@@@@&&&&&&&&&&&&&&&&&&&@@@@@@@@@@@@@@@
                @@@@@@@@@@@@@@@&&&&&&&&&&&&&&&&&&&@@@@@@@@@@@@@@@
                .@@@@@@@@@@@@@@&&&&&&&&&&&&&&&&&&&@@@@@@@@@@@@@@
                 (@@@@@@@@@@@@@@&&&&&&&&&&&&&&&&&@@@@@@@@@@@@@@.
                   @@@@@@@@@@@@@@&&&&&&&&&&&&&&&@@@@@@@@@@@@@@
                    ,@@@@@@@@@@@@@&&&&&&&&&&&&&@@@@@@@@@@@@@
                       @@@@@@@@@@@@@&&&&&&&&&@@@@@@@@@@@@/

Current pumpcoins: [1337]

Items:

1. Shovel  (1337 p.c.)
2. Laser   (9999 p.c.)

>> 1

How many do you want?

>> 26

Current pumpcoins: [32111]


Good luck crafting this huge pumpkin with a shovel!


Current pumpcoins: [32111]

Items:

1. Shovel  (1337 p.c.)
2. Laser   (9999 p.c.)

>> 3

How many do you want?

>> 1

Congratulations, here is the code to get your laser:

HTB{1nt3g3R_0v3rfl0w_101_0r_0v3R_9000!}


Connection closed by foreign host.
```

# Takeaways
- When writing a program that handles money, ensure that the math in your program makes logical sense based on your scenario.
