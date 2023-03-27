---
layout: default
title: Secret Code
---

# [Cyber Apocalypse 2023](index.md) - Hardware - Secret Code

> 


```
Channel 0       01100101011100111110111111111110111111111000101011101101101101
Channel 2       01100110111111111111111110111111111111101111101111101101101110
Channel 3       11111101001000111111111011111111111110111100101011101110101101
Channel 4       11111011111111111010111111111110111011111011111111111011010111
Channel 5       11011110111111111100011101111000001111010011111101110011111111
Channel 6       01000101010100000101100111000001110101110100000011001101101001
Channel 7       11111001010100000011100110000111110001101100000011001111000000
```

```cs
using System.Text;

const string bits_channel_0 = "01100101011100111110111111111110111111111000101011101101101101";
const string bits_channel_2 = "01100110111111111111111110111111111111101111101111101101101110";
const string bits_channel_3 = "11111101001000111111111011111111111110111100101011101110101101";
const string bits_channel_4 = "11111011111111111010111111111110111011111011111111111011010111";
const string bits_channel_5 = "11011110111111111100011101111000001111010011111101110011111111";
const string bits_channel_6 = "01000101010100000101100111000001110101110100000011001101101001";
const string bits_channel_7 = "11111001010100000011100110000111110001101100000011001111000000";

// Making these all constants means that if we're wrong about how these are "wired up" on the 
// circuit board, we can easily change which channel from the waveform capture matches up
// with which electrical channel on the board.
const int display_cell_a = 0;
const int display_cell_b = 1;
const int display_cell_c = 2;
const int display_cell_d = 3;
const int display_cell_e = 4;
const int display_cell_f = 5;
const int display_cell_g = 6;

const int channel_0_position = display_cell_d;
const int channel_2_position = display_cell_a;
const int channel_3_position = display_cell_g;
const int channel_4_position = display_cell_c;
const int channel_5_position = display_cell_b;
const int channel_6_position = display_cell_e;
const int channel_7_position = display_cell_f;

void renderDisplay(string inputBinaryString) {
    // Make sure the input is exactly 7 digits long
    if (!(inputBinaryString.Length==7)) { return; }

    const char display_character = '█';
    const char empty_character = ' ';
    const ConsoleColor color_on = ConsoleColor.Red;
    const ConsoleColor color_off = ConsoleColor.DarkGray;
    
    ConsoleColor previous_console_color = Console.ForegroundColor;

    Console.ForegroundColor = color_off;

    // Top segment - segment "a"
    if (inputBinaryString[display_cell_a] == '1') {
        Console.ForegroundColor = color_on;
    } else {
        Console.ForegroundColor = color_off;
    }
    Console.Write($"{empty_character}{display_character}{display_character}{display_character}{empty_character}\n");
    

    for(int x = 0; x<2; x++) {
        // Top left - segment "f"
        if (inputBinaryString[display_cell_f] == '1') {
            Console.ForegroundColor = color_on;
        } else {
            Console.ForegroundColor = color_off;
        }
        Console.Write($"{display_character}");
        
        // Empty space
        Console.Write($"{empty_character}{empty_character}{empty_character}");
        
        // Top right - segment "b"
        if (inputBinaryString[display_cell_b] == '1') {
            Console.ForegroundColor = color_on;
        } else {
            Console.ForegroundColor = color_off;
        }
        Console.Write($"{display_character}\n");
    }
    
    // Middle segment - segment "g"
    if (inputBinaryString[display_cell_g] == '1') {
        Console.ForegroundColor = color_on;
    } else {
        Console.ForegroundColor = color_off;
    }
    Console.Write($"{empty_character}{display_character}{display_character}{display_character}{empty_character}\n");

    for(int x = 0; x<2; x++) {
    // Bottom Left - segment "e"
        if (inputBinaryString[display_cell_e] == '1') {
            Console.ForegroundColor = color_on;
        } else {
            Console.ForegroundColor = color_off;
        }
        Console.Write($"{display_character}");
        
        // Empty space
        Console.Write($"{empty_character}{empty_character}{empty_character}");
        
    // Bottom right - segment "c" 
        if (inputBinaryString[display_cell_c] == '1') {
            Console.ForegroundColor = color_on;
        } else {
            Console.ForegroundColor = color_off;
        }
        Console.Write($"{display_character}\n");
    }

    // Bottom segment - segment "d"
    if (inputBinaryString[display_cell_d] == '1') {
        Console.ForegroundColor = color_on;
    } else {
        Console.ForegroundColor = color_off;
    }
    Console.Write($"{empty_character}{display_character}{display_character}{display_character}{empty_character}\n");

    Console.Write("\n");

    Console.ForegroundColor = previous_console_color;
}

// Take separate channels and combine them into binary words
List<string> binary_words = new List<string>();

for(int x = 0; x < bits_channel_0.Length; x++) {
    StringBuilder word = new StringBuilder("       ");
    word[channel_0_position] = (bits_channel_0[x]);
    word[channel_2_position] = (bits_channel_2[x]);
    word[channel_3_position] = (bits_channel_3[x]);
    word[channel_4_position] = (bits_channel_4[x]);
    word[channel_5_position] = (bits_channel_5[x]);
    word[channel_6_position] = (bits_channel_6[x]);
    word[channel_7_position] = (bits_channel_7[x]);
    binary_words.Add(word.ToString());
}

foreach(string word in binary_words) {
    renderDisplay(word);
}
```