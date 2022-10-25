---
layout: default
title: Entity
---

# [Hack The Boo](index.md) - Pwn - Entity
**Difficulty:** Easy


> This Spooky Time of the year, what's better than watching a scary film on the TV? Well, a lot of things, like playing CTFs but you know what's definitely not better? Something coming out of your TV!

We are provided with some C code, and the compiled version of this code (presumably).

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static union {
    unsigned long long integer;
    char string[8];
} DataStore;

typedef enum {
    STORE_GET,
    STORE_SET,
    FLAG
} action_t;

typedef enum {
    INTEGER,
    STRING
} field_t;

typedef struct {
    action_t act;
    field_t field;
} menu_t;

menu_t menu() {
    menu_t res = { 0 };
    char buf[32] = { 0 };
    printf("\n(T)ry to turn it off\n(R)un\n(C)ry\n\n>> ");
    fgets(buf, sizeof(buf), stdin);
    buf[strcspn(buf, "\n")] = 0;
    switch (buf[0]) {
    case 'T':
        res.act = STORE_SET;
        break;
    case 'R':
        res.act = STORE_GET;
        break;
    case 'C':
        res.act = FLAG;
        return res;
    default:
        puts("\nWhat's this nonsense?!");
        exit(-1);
    }

    printf("\nThis does not seem to work.. (L)ie down or (S)cream\n\n>> ");
    fgets(buf, sizeof(buf), stdin);
    buf[strcspn(buf, "\n")] = 0;
    switch (buf[0]) {
    case 'L':
        res.field = INTEGER;
        break;
    case 'S':
        res.field = STRING;
        break;
    default:
        printf("\nYou are doomed!\n");
        exit(-1);
    }
    return res;
}

void set_field(field_t f) {
    char buf[32] = {0};
    printf("\nMaybe try a ritual?\n\n>> ");
    fgets(buf, sizeof(buf), stdin);
    switch (f) {
    case INTEGER:
        sscanf(buf, "%llu", &DataStore.integer);
        if (DataStore.integer == 13371337) {
            puts("\nWhat's this nonsense?!");
            exit(-1);
        }
        break;
    case STRING:
        memcpy(DataStore.string, buf, sizeof(DataStore.string));
        break;
    }

}

void get_field(field_t f) {
    printf("\nAnything else to try?\n\n>> ");
    switch (f) {
    case INTEGER:
        printf("%llu\n", DataStore.integer);
        break;
    case STRING:
        printf("%.8s\n", DataStore.string);
        break;
    }
}

void get_flag() {
    if (DataStore.integer == 13371337) {
        system("cat flag.txt");
        exit(0);
    } else {
        puts("\nSorry, this will not work!");
    }
}

int main() {
    setvbuf(stdout, NULL, _IONBF, 0);
    bzero(&DataStore, sizeof(DataStore));
    printf("\nSomething strange is coming out of the TV..\n");
    while (1) {
        menu_t result = menu();
        switch (result.act) {
        case STORE_SET:
            set_field(result.field);
            break;
        case STORE_GET:
            get_field(result.field);
            break;
        case FLAG:
            get_flag();
            break;
        }
    }

}
```

If we ignore what the text is saying, this program is all about reading and writing to `DataStore` - a `union` that contains a string (character array) and an integer value. The way that unions work in C++ is that variables inside of it share the same memory space, and so you can't use both the string and integer values at the same time.

Setting a string value of `a` will result in a numeric value of `2657`.

It looks like what you need to do is find a string value that you can set the DataStore.string to that will set DataStore.integer to `13371337`, then trigger the `get_flag()` function to retrieve the flag.

I created the following map to navigate the program more easily. The "main menu" is when it says "(T)ry to turn it off (R)un (C)ry". If you ignore the text and just push the listed characters, you can more easily interact with the DataStore. Entering any other character will stop the program.

Set string value
- T
- S
- Enter a string value and press enter

Set integer value
- T
- L
- Enter an integer value and press enter

Show string value
- R
- S

Show integer value
- R
- L

Attempt to retrieve flag
- C

Simply entering an integer value of `13371337` will cause the program to exit, but there are no checks when we enter a string.

I wrote the following C++ program to help find characters that would be close to the equivalent of 13371337, but did not have success finding them.

```c
#include <iostream>
#include <cstring>
#include <string>

static union {
    unsigned long long integer;
    char string[8];
} DataStore;

int main()
{
    char buf[32] = {0};

    while(1)
    {
        printf("\nMaybe try a ritual?\n\n>> ");
        fgets(buf, sizeof(buf), stdin);
        memcpy(DataStore.string, buf, sizeof(DataStore.string));
        std::cout << "\"" << DataStore.integer << "\"\n";
    }
}
```
When I wrote code to simply convert `13371337` into characters, I got unprintable characters, which I could not easily copy and paste back into the terminal.

I stopped working on this challenge at this point, so that I could attempt other challenges.
