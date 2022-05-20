---
layout: default
title: OmegaOne
---

# [Cyber Apocalypse](index.md) - Reversing - OmegaOne

> You've been sent to the library planet Omega-One. Here, records from all over the galaxy are collected, sorted and archived with perfect efficiency. You need to retrieve records about Draeger's childhood, but the interface is impossibly large. Can you unravel the storage system?

In this challenge, we are given a binary and a text file (`outut.txt`)containing 32 names.

Running the binary doesn't appear to do produce any output or syntax help.

The `output.txt` file looks like this:

```
Crerceon
Ezains
Ummuh
Zonnu
Vinzo
Cuzads
Emoi
Ohols
Groz'ens
Ukox
Ehnu
Pheilons
Cuzads
Khehlan
Ohols
Ehnu
Munis
Inphas
Pheilons
Ehnu
Dut
Ukox
Ohols
Pheilons
Pheilons
Zimil
Ehnu
Honzor
Vinzo
Ukteils
Falnain
Dhohmu
Baadix
```

Decompiling the binary with ghidra we see a fairly sparse program that doesn't appear to do much.

There doesn't appear to be a `main` function, so if we look at the `entry` function we see that it initializes some things
```c++
  __libc_start_main(FUN_00100b4c,in_stack_00000000,&stack0x00000008,FUN_001020a0,FUN_00102110,
                    param_3,auStack8);
```

Following the first function name (`FUN_00100b4c` in my case) we find some kind of dictionary get initialized

```c++
  FUN_00101870(DAT_00303018,"k","Lendrens");
  FUN_00101870(DAT_00303018,"d","Thauv\'i");
  FUN_00101870(DAT_00303018,"P","Throrqiek");
  FUN_00101870(DAT_00303018,"e","Inqods");
  FUN_00101870(DAT_00303018,"6","Tarquts");
  FUN_00101870(DAT_00303018,"p","Dut");
  FUN_00101870(DAT_00303018,"A","Krolkel");
  FUN_00101870(DAT_00303018,"n","Emoi");
  FUN_00101870(DAT_00303018,"|","Dakroith");
  FUN_00101870(DAT_00303018,"*","Creiqex");
  FUN_00101870(DAT_00303018,"Y","Thomois");
  FUN_00101870(DAT_00303018,"4","Groz\'ens");
  FUN_00101870(DAT_00303018,"D","Urqek");
  FUN_00101870(DAT_00303018,"v","Nid");
  FUN_00101870(DAT_00303018,"H","Crerceon");
  FUN_00101870(DAT_00303018,"#","Yonphie");
  FUN_00101870(DAT_00303018,"S","Xits");
  FUN_00101870(DAT_00303018,"I","Thohul");
  FUN_00101870(DAT_00303018,"W","Zahrull");
  FUN_00101870(DAT_00303018,"i","Om\'ons");
  FUN_00101870(DAT_00303018,"F","Kradraks");
  FUN_00101870(DAT_00303018,"+","Ielkul");
  FUN_00101870(DAT_00303018,"q","Vranix");
  FUN_00101870(DAT_00303018,"M","Trun");
  FUN_00101870(DAT_00303018,"h","Craz\'ails");
  FUN_00101870(DAT_00303018,".","Xoq\'an");
  FUN_00101870(DAT_00303018,"r","Ukox");
  FUN_00101870(DAT_00303018,"N","Evods");
  FUN_00101870(DAT_00303018,";","Taxan");
  FUN_00101870(DAT_00303018,"b","Munis");
  FUN_00101870(DAT_00303018,"g","Trurkror");
  FUN_00101870(DAT_00303018,"?","Tulphaer");
  FUN_00101870(DAT_00303018,"_","Ehnu");
  FUN_00101870(DAT_00303018,"$","Krets");
  FUN_00101870(DAT_00303018,",","Grons");
  FUN_00101870(DAT_00303018,")","Ingell");
  FUN_00101870(DAT_00303018,"(","Ecruns");
  FUN_00101870(DAT_00303018,"m","Khehlan");
  FUN_00101870(DAT_00303018,"R","Velzaeth");
  FUN_00101870(DAT_00303018,"Q","Cuhix");
  FUN_00101870(DAT_00303018,"l","Vinzo");
  FUN_00101870(DAT_00303018,"E","Istrur");
  FUN_00101870(DAT_00303018,">","Zuvas");
  FUN_00101870(DAT_00303018,"s","Honzor");
  FUN_00101870(DAT_00303018,"0","Ukteils");
  FUN_00101870(DAT_00303018,"}","Baadix");
  FUN_00101870(DAT_00303018,"{","Zonnu");
  FUN_00101870(DAT_00303018,"\\","Aarcets");
  FUN_00101870(DAT_00303018,"[","Nevell");
  FUN_00101870(DAT_00303018,"!","Dhohmu");
  FUN_00101870(DAT_00303018,"X","Xan");
  FUN_00101870(DAT_00303018,"O","Zissat");
  FUN_00101870(DAT_00303018,"x","Iscax");
  FUN_00101870(DAT_00303018,"t","Pheilons");
  FUN_00101870(DAT_00303018,"`","Ghiso");
  FUN_00101870(DAT_00303018,"-","Scrigvil");
  FUN_00101870(DAT_00303018,"B","Ummuh");
  FUN_00101870(DAT_00303018,"u","Inphas");
  FUN_00101870(DAT_00303018,"/","Vurqails");
  FUN_00101870(DAT_00303018,"a","Vruziels");
  FUN_00101870(DAT_00303018,":","Ghut\'ox");
  FUN_00101870(DAT_00303018,"^","Aahroill");
  FUN_00101870(DAT_00303018,"L","Gairqeik");
  FUN_00101870(DAT_00303018,"U","Qeks");
  FUN_00101870(DAT_00303018,"\'","Scuvvils");
  FUN_00101870(DAT_00303018,"3","Ohols");
  FUN_00101870(DAT_00303018,"5","Som\'ir");
  FUN_00101870(DAT_00303018,"C","Onzear");
  FUN_00101870(DAT_00303018,"2","Dhaesux");
  FUN_00101870(DAT_00303018,"w","Falnain");
  FUN_00101870(DAT_00303018," ","Draalpho");
  FUN_00101870(DAT_00303018,"G","Yemor");
  FUN_00101870(DAT_00303018,"c","Thraurgok");
  FUN_00101870(DAT_00303018,"\"","Vogeath");
  FUN_00101870(DAT_00303018,"1","Cuzads");
  FUN_00101870(DAT_00303018,"Z","Gagro");
  FUN_00101870(DAT_00303018,"=","Zad");
  FUN_00101870(DAT_00303018,"f","Dhieqe");
  FUN_00101870(DAT_00303018,"&","Xustrek");
  FUN_00101870(DAT_00303018,"o","Harned");
  FUN_00101870(DAT_00303018,"V","Dhulgea");
  FUN_00101870(DAT_00303018,"y","Zimil");
  FUN_00101870(DAT_00303018,"z","Thretex");
  FUN_00101870(DAT_00303018,"8","Bravon");
  FUN_00101870(DAT_00303018,"%","Krugreall");
  FUN_00101870(DAT_00303018,"J","Vaendred");
  FUN_00101870(DAT_00303018,"@","Osux");
  FUN_00101870(DAT_00303018,"T","Ezains");
  FUN_00101870(DAT_00303018,"K","Mik\'ed");
  FUN_00101870(DAT_00303018,"<","Cruz\'oll");
  FUN_00101870(DAT_00303018,"]","Dhognot");
  FUN_00101870(DAT_00303018,"7","Drids");
  FUN_00101870(DAT_00303018,"9","Drercieks");
  FUN_00101870(DAT_00303018,"j","Statars");
```
I notice that:
 - Each name corresponds to a single letter
 - Some names from this list are in the `output.txt` file
 - `H`, `T`, `B`, `{`, and `}` are present in this list
 - `output.txt` starts with `Crerceon` which corresponds to `H`, and ends with `Baadix` which corresponds to `}`

It seems like I should just be able to look up each name in this dictionary and assemble the flag.

I *could* do this manually, but I'm a professional C# programmer, so its easier for me to write a quick script using [.Net Fiddle](https://dotnetfiddle.net/) to assemble the flag for me. I was able to quickly turn the above C++ code into the correct formatting for a C# dictionary using VSCode and it's multi-cursor capabilities (Sublime Text would also have worked).

```cs
using System;
using System.Text;
using System.Collections;
using System.Collections.Generic;
					
public class Program
{
	public static void Main()
	{
		Dictionary<string,string> _dict = new Dictionary<string,string>() {
			{ "Lendrens","k" },{ "Thauv\'i","d" },{ "Throrqiek","P" },{ "Inqods","e" },{ "Tarquts","6" },{ "Dut","p" },{ "Krolkel","A" },{ "Emoi","n" },{ "Dakroith","|" },{ "Creiqex","*" },{ "Thomois","Y" },{ "Groz\'ens","4" },{ "Urqek","D" },{ "Nid","v" },{ "Crerceon","H" },{ "Yonphie","#" },{ "Xits","S" },{ "Thohul","I" },{ "Zahrull","W" },{ "Om\'ons","i" },{ "Kradraks","F" },{ "Ielkul","+" },{ "Vranix","q" },{ "Trun","M" },{ "Craz'ails","h" },{ "Xoq\'an","." },{ "Ukox","r" },{ "Evods","N" },{ "Taxan",";" },{ "Munis","b" },{ "Trurkror","g" },{ "Tulphaer","?" },{ "Ehnu","_" },{ "Krets","$" },{ "Grons","" },{ "Ingell",")" },{ "Ecruns","(" },{ "Khehlan","m" },{ "Velzaeth","R" },{ "Cuhix","Q" },{ "Vinzo","l" },{ "Istrur","E" },{ "Zuvas",">" },{ "Honzor","s" },{ "Ukteils","0" },{ "Baadix","}" },{ "Zonnu","{" },{ "Aarcets","\\" },{ "Nevell","[" },{ "Dhohmu","!" },{ "Xan","X" },{ "Zissat","O" },{ "Iscax","x" },{ "Pheilons","t" },{ "Ghiso","`" },{ "Scrigvil","-" },{ "Ummuh","B" },{ "Inphas","u" },{ "Vurqails","/" },{ "Vruziels","a" },{ "Ghut\'ox",":" },{ "Aahroill","^" },{ "Gairqeik","L" },{ "Qeks","U" },{ "Scuvvils","\'" },{ "Ohols","3" },{ "Som\'ir","5" },{ "Onzear","C" },{ "Dhaesux","2" },{ "Falnain","w" },{ "Draalpho"," " },{ "Yemor","G" },{ "Thraurgok","c" },{ "Vogeath","\"" },{ "Cuzads","1" },{ "Gagro","Z" },{ "Zad","=" },{ "Dhieqe","f" },{ "Xustrek","&" },{ "Harned","o" },{ "Dhulgea","V" },{ "Zimil","y" },{ "Thretex","z" },{ "Bravon","8" },{ "Krugreall","%" },{ "Vaendred","J" },{ "Osux","@" },{ "Ezains","T" },{ "Mik\'ed","K" },{ "Cruz\'oll","<" },{ "Dhognot","]" },{ "Drids","7" },{ "Drercieks","9" },{ "Statars","j" }
		};
		
		List<string> input = new List<string>() {
			"Crerceon","Ezains","Ummuh","Zonnu","Vinzo","Cuzads","Emoi","Ohols","Groz'ens","Ukox","Ehnu","Pheilons","Cuzads","Khehlan","Ohols","Ehnu","Munis","Inphas","Pheilons","Ehnu","Dut","Ukox","Ohols","Pheilons","Pheilons","Zimil","Ehnu","Honzor","Vinzo","Ukteils","Falnain","Dhohmu","Baadix"
		};
		
		StringBuilder flag = new StringBuilder();
		
		foreach(string inp in input) 
		{
			if (_dict.ContainsKey(inp)) {
				flag.Append(_dict[inp]);
			} else {
                // I expect each name to exist in the dictionary, but just in case
				Console.WriteLine("Key not found: " + inp);
			}
		}
		
		Console.WriteLine("Flag: " + flag.ToString());
		
	}
}
```

And this reveals the flag.
```
Flag: HTB{l1n34r_t1m3_but_pr3tty_sl0w!}
```