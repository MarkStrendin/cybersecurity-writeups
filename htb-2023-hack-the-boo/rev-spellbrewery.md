---
layout: default
title: Wide
---

# [Hack The Boo 2023](index.md) - Reversing - SpellBrewery

> I've been hard at work in my spell brewery for days, but I can't crack the secret of the potion of eternal life. Can you uncover the recipe?

We're provided a zip file containing a binary, a couple json files, and a dll.

Running a `file` against the binary gets us:
```
SpellBrewery: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 2.6.32, BuildID[sha1]=8b106946c31c6346abd618ab5d2232845492e2d9, not stripped
```

And running `file` against the dll gets us:
```
SpellBrewery.dll: PE32 executable (console) Intel 80386 Mono/.Net assembly, for MS Windows
```

So, it looks like we're dealing with a .Net application.
I used [Jetbrains dotPeek](https://www.jetbrains.com/decompiler/) to disassemble both files into C# code. 
The binary itself was not interesting, it just runs the code from the DLL, so we can focus our attention on the DLL for now.

In the DLL file, we find all the logic for this program - it wants us to add ingredients, and if we've chosen the correct ones, in the correct order, it will reveal the flag to us.

```cs
namespace SpellBrewery
{
  internal class Brewery
  {
    private static readonly string[] IngredientNames = new string[106]
    {
      "Witch's Eye",
      "Bat Wing",
      "Ghostly Essence",
      "Toadstool Extract",
      "Vampire Blood",
      "Mandrake Root",
      "Zombie Brain",
      "Ghoul's Breath",
      "Spider Venom",
      "Black Cat's Whisker",
      "Werewolf Fur",
      "Banshee's Wail",
      "Spectral Ash",
      "Pumpkin Spice",
      "Goblin's Earwax",
      "Haunted Mist",
      "Wraith's Tear",
      "Serpent Scale",
      "Moonlit Fern",
      "Cursed Skull",
      "Raven Feather",
      "Wolfsbane",
      "Frankenstein's Bolt",
      "Wicked Ivy",
      "Screaming Banshee Berry",
      "Mummy's Wrappings",
      "Dragon's Breath",
      "Bubbling Cauldron Brew",
      "Gorehound's Howl",
      "Wraithroot",
      "Haunted Grave Moss",
      "Ectoplasmic Slime",
      "Voodoo Doll's Stitch",
      "Bramble Thorn",
      "Hocus Pocus Powder",
      "Cursed Clove",
      "Wicked Witch's Hair",
      "Halloween Moon Dust",
      "Bog Goblin Slime",
      "Ghost Pepper",
      "Phantom Firefly Wing",
      "Gargoyle Stone",
      "Zombie Toenail",
      "Poltergeist Polyp",
      "Spectral Goo",
      "Salamander Scale",
      "Cursed Candelabra Wax",
      "Witch Hazel",
      "Banshee's Bane",
      "Grim Reaper's Scythe",
      "Black Widow Venom",
      "Moonlit Nightshade",
      "Ghastly Gourd",
      "Siren's Song Seashell",
      "Goblin Gold Dust",
      "Spider Web Silk",
      "Haunted Spirit Vine",
      "Frog's Tongue",
      "Mystic Mandrake",
      "Widow's Peak Essence",
      "Wicked Warlock's Beard",
      "Crypt Keeper's Cryptonite",
      "Bewitched Broomstick Bristle",
      "Dragon's Scale Shimmer",
      "Vampire Bat Blood",
      "Graveyard Grass",
      "Halloween Harvest Pumpkin",
      "Cursed Cobweb Cotton",
      "Phantom Howler Fur",
      "Wraithbone",
      "Goblin's Green Slime",
      "Witch's Brew Brew",
      "Voodoo Doll Pin",
      "Bramble Berry",
      "Spooky Spellbook Page",
      "Halloween Cauldron Steam",
      "Spectral Spectacles",
      "Salamander's Tail",
      "Cursed Crypt Key",
      "Pumpkin Patch Spice",
      "Haunted Hay Bale",
      "Banshee's Bellflower",
      "Ghoulish Goblet",
      "Frankenstein's Lab Liquid",
      "Zombie Zest Zest",
      "Werewolf Whisker",
      "Gargoyle Gaze",
      "Black Cat's Meow",
      "Wolfsbane Extract",
      "Goblin's Gold",
      "Phantom Firefly Fizz",
      "Spider Sling Silk",
      "Widow's Weave",
      "Wraith Whisper",
      "Siren's Serenade",
      "Moonlit Mirage",
      "Spectral Spark",
      "Dragon's Roar",
      "Banshee's Banshee",
      "Witch's Whisper",
      "Ghoul's Groan",
      "Toadstool Tango",
      "Vampire's Kiss",
      "Bubbling Broth",
      "Mystic Elixir",
      "Cursed Charm"
    };
    private static readonly string[] correct = new string[36]
    {
      "Phantom Firefly Wing",
      "Ghastly Gourd",
      "Hocus Pocus Powder",
      "Spider Sling Silk",
      "Goblin's Gold",
      "Wraith's Tear",
      "Werewolf Whisker",
      "Ghoulish Goblet",
      "Cursed Skull",
      "Dragon's Scale Shimmer",
      "Raven Feather",
      "Dragon's Scale Shimmer",
      "Zombie Zest Zest",
      "Ghoulish Goblet",
      "Werewolf Whisker",
      "Cursed Skull",
      "Dragon's Scale Shimmer",
      "Haunted Hay Bale",
      "Wraith's Tear",
      "Zombie Zest Zest",
      "Serpent Scale",
      "Wraith's Tear",
      "Cursed Crypt Key",
      "Dragon's Scale Shimmer",
      "Salamander's Tail",
      "Raven Feather",
      "Wolfsbane",
      "Frankenstein's Lab Liquid",
      "Zombie Zest Zest",
      "Cursed Skull",
      "Ghoulish Goblet",
      "Dragon's Scale Shimmer",
      "Cursed Crypt Key",
      "Wraith's Tear",
      "Black Cat's Meow",
      "Wraith Whisper"
    };
    private static readonly List<Ingredient> recipe = new List<Ingredient>();

    private static void Main()
    {
      while (true)
      {
        switch (Menu.RunMenu())
        {
          case Menu.Choice.ListIngredients:
            Brewery.ListIngredients();
            break;
          case Menu.Choice.DisplayRecipe:
            Brewery.DisplayRecipe();
            break;
          case Menu.Choice.AddIngredient:
            Brewery.AddIngredient();
            break;
          case Menu.Choice.BrewSpell:
            Brewery.BrewSpell();
            break;
          case Menu.Choice.ClearRecipe:
            Brewery.ClearRecipe();
            break;
        }
      }
    }

    private static void ListIngredients()
    {
      for (int index = 0; index < Brewery.IngredientNames.Length; ++index)
      {
        Console.Write(Brewery.IngredientNames[index] ?? "");
        if (index + 1 < Brewery.IngredientNames.Length)
          Console.Write(", ");
        if (index % 6 == 5)
          Console.Write("\n");
      }
      Console.Write("\n");
    }

    private static void DisplayRecipe()
    {
      if (Brewery.recipe.Count == 0)
        Console.WriteLine("There are no current ingredients");
      else
        Console.WriteLine(string.Join<Ingredient>(", ", (IEnumerable<Ingredient>) Brewery.recipe));
    }

    private static void AddIngredient()
    {
      Console.Write("What ingredient would you like to add? ");
      string name;
      while (true)
      {
        name = Console.ReadLine();
        if (!((IEnumerable<string>) Brewery.IngredientNames).Contains<string>(name))
          Console.WriteLine("Invalid ingredient name");
        else
          break;
      }
      Brewery.recipe.Add(new Ingredient(name));
      string str = "aeiou".Contains(char.ToLower(name[0])) ? "an" : "a";
      DefaultInterpolatedStringHandler interpolatedStringHandler = new DefaultInterpolatedStringHandler(41, 2);
      interpolatedStringHandler.AppendLiteral("The cauldron fizzes as you toss in ");
      interpolatedStringHandler.AppendFormatted(str);
      interpolatedStringHandler.AppendLiteral(" '");
      interpolatedStringHandler.AppendFormatted(name);
      interpolatedStringHandler.AppendLiteral("'...");
      Console.WriteLine(interpolatedStringHandler.ToStringAndClear());
    }

    private static void BrewSpell()
    {
      if (Brewery.recipe.Count < 1)
      {
        Console.WriteLine("You can't brew with an empty cauldron");
      }
      else
      {
        byte[] array = Brewery.recipe.Select<Ingredient, byte>((Func<Ingredient, byte>) (ing => (byte) (Array.IndexOf<string>(Brewery.IngredientNames, ing.ToString()) + 32))).ToArray<byte>();
        if (Brewery.recipe.SequenceEqual<Ingredient>(((IEnumerable<string>) Brewery.correct).Select<string, Ingredient>((Func<string, Ingredient>) (name => new Ingredient(name)))))
        {
          Console.WriteLine("The spell is complete - your flag is: " + Encoding.ASCII.GetString(array));
          Environment.Exit(0);
        }
        else
          Console.WriteLine("The cauldron bubbles as your ingredients melt away. Try another recipe.");
      }
    }

    private static void ClearRecipe()
    {
      Brewery.recipe.Clear();
      Console.WriteLine("You pour the cauldron down the drain. A fizzing noise and foul smell rises from it...");
    }
  }
}
```

We can see in the following section that it checks our input against a list called `Brewery.correct`, which appears to be the correct order of ingredients that it expects us to add.

```cs
if (Brewery.recipe.SequenceEqual<Ingredient>(((IEnumerable<string>) Brewery.correct).Select<string, Ingredient>((Func<string, Ingredient>) (name => new Ingredient(name)))))
{
    Console.WriteLine("The spell is complete - your flag is: " + Encoding.ASCII.GetString(array));
    Environment.Exit(0);
}
else
    Console.WriteLine("The cauldron bubbles as your ingredients melt away. Try another recipe.");
}
```

And we can see this list defined earlier in the code:

```cs
private static readonly string[] correct = new string[36]
    {
      "Phantom Firefly Wing",
      "Ghastly Gourd",
      "Hocus Pocus Powder",
      "Spider Sling Silk",
      "Goblin's Gold",
      "Wraith's Tear",
      "Werewolf Whisker",
      "Ghoulish Goblet",
      "Cursed Skull",
      "Dragon's Scale Shimmer",
      "Raven Feather",
      "Dragon's Scale Shimmer",
      "Zombie Zest Zest",
      "Ghoulish Goblet",
      "Werewolf Whisker",
      "Cursed Skull",
      "Dragon's Scale Shimmer",
      "Haunted Hay Bale",
      "Wraith's Tear",
      "Zombie Zest Zest",
      "Serpent Scale",
      "Wraith's Tear",
      "Cursed Crypt Key",
      "Dragon's Scale Shimmer",
      "Salamander's Tail",
      "Raven Feather",
      "Wolfsbane",
      "Frankenstein's Lab Liquid",
      "Zombie Zest Zest",
      "Cursed Skull",
      "Ghoulish Goblet",
      "Dragon's Scale Shimmer",
      "Cursed Crypt Key",
      "Wraith's Tear",
      "Black Cat's Meow",
      "Wraith Whisper"
    };
```

If we get the order correct, there is some code to reveal the flag to us:

```cs
byte[] array = Brewery.recipe.Select<Ingredient, byte>((Func<Ingredient, byte>) (ing => (byte) (Array.IndexOf<string>(Brewery.IngredientNames, ing.ToString()) + 32))).ToArray<byte>();
```
```cs
Console.WriteLine("The spell is complete - your flag is: " + Encoding.ASCII.GetString(array));
```

So, we _could_ reverse engineer this block of code to just retrieve the flag from the code, but properly reversing this code will take time, and I decided that while that would be fun, it would probably be faster to just manually copy and paste the correct answers into the program and have it give us the flag "legitimately". I would come back later after the competition is over and do a "proper" reverse engineer of the code to figure out how it works (which you can find below).

We can run the program manually by using the command `dotnet SpellBrewery.dll` (provided we have dotnet installed). It should run on both Windows or Linux, I used Windows because I already had a Windows box handy that had dotnet installed on it.

```
1. List Ingredients
2. Display Current Recipe
3. Add Ingredient
4. Brew Spell
5. Clear Recipe
6. Quit
>
```

So, I just manually added the correct ingredients from the list, and then selected option `4` for "Brew Spell", and got the flag.

```
The cauldron fizzes as you toss in a 'Wraith Whisper'...
1. List Ingredients
2. Display Current Recipe
3. Add Ingredient
4. Brew Spell
5. Clear Recipe
6. Quit
> 4
The spell is complete - your flag is: HTB{y0ur3_4_tru3_p0t10n_m45st3r_n0w}
```

# Solving it with code instead of manual labour
By taking bits of the decompiled code, we can make a script that just tells us the flag:
```cs
using System;
using System.Linq;
using System.Collections.Generic;
using System.Text;

#nullable enable
namespace SpellBrewery 
{
	class Ingredient
	{
		private readonly string name;
		public Ingredient(string name) => this.name = name;
		public override string ToString() => this.name;
	}

	class Brewery
	{
		private static readonly string[] IngredientNames = new string[106]
		{
		  "Witch's Eye",
		  "Bat Wing",
		  "Ghostly Essence",
		  "Toadstool Extract",
		  "Vampire Blood",
		  "Mandrake Root",
		  "Zombie Brain",
		  "Ghoul's Breath",
		  "Spider Venom",
		  "Black Cat's Whisker",
		  "Werewolf Fur",
		  "Banshee's Wail",
		  "Spectral Ash",
		  "Pumpkin Spice",
		  "Goblin's Earwax",
		  "Haunted Mist",
		  "Wraith's Tear",
		  "Serpent Scale",
		  "Moonlit Fern",
		  "Cursed Skull",
		  "Raven Feather",
		  "Wolfsbane",
		  "Frankenstein's Bolt",
		  "Wicked Ivy",
		  "Screaming Banshee Berry",
		  "Mummy's Wrappings",
		  "Dragon's Breath",
		  "Bubbling Cauldron Brew",
		  "Gorehound's Howl",
		  "Wraithroot",
		  "Haunted Grave Moss",
		  "Ectoplasmic Slime",
		  "Voodoo Doll's Stitch",
		  "Bramble Thorn",
		  "Hocus Pocus Powder",
		  "Cursed Clove",
		  "Wicked Witch's Hair",
		  "Halloween Moon Dust",
		  "Bog Goblin Slime",
		  "Ghost Pepper",
		  "Phantom Firefly Wing",
		  "Gargoyle Stone",
		  "Zombie Toenail",
		  "Poltergeist Polyp",
		  "Spectral Goo",
		  "Salamander Scale",
		  "Cursed Candelabra Wax",
		  "Witch Hazel",
		  "Banshee's Bane",
		  "Grim Reaper's Scythe",
		  "Black Widow Venom",
		  "Moonlit Nightshade",
		  "Ghastly Gourd",
		  "Siren's Song Seashell",
		  "Goblin Gold Dust",
		  "Spider Web Silk",
		  "Haunted Spirit Vine",
		  "Frog's Tongue",
		  "Mystic Mandrake",
		  "Widow's Peak Essence",
		  "Wicked Warlock's Beard",
		  "Crypt Keeper's Cryptonite",
		  "Bewitched Broomstick Bristle",
		  "Dragon's Scale Shimmer",
		  "Vampire Bat Blood",
		  "Graveyard Grass",
		  "Halloween Harvest Pumpkin",
		  "Cursed Cobweb Cotton",
		  "Phantom Howler Fur",
		  "Wraithbone",
		  "Goblin's Green Slime",
		  "Witch's Brew Brew",
		  "Voodoo Doll Pin",
		  "Bramble Berry",
		  "Spooky Spellbook Page",
		  "Halloween Cauldron Steam",
		  "Spectral Spectacles",
		  "Salamander's Tail",
		  "Cursed Crypt Key",
		  "Pumpkin Patch Spice",
		  "Haunted Hay Bale",
		  "Banshee's Bellflower",
		  "Ghoulish Goblet",
		  "Frankenstein's Lab Liquid",
		  "Zombie Zest Zest",
		  "Werewolf Whisker",
		  "Gargoyle Gaze",
		  "Black Cat's Meow",
		  "Wolfsbane Extract",
		  "Goblin's Gold",
		  "Phantom Firefly Fizz",
		  "Spider Sling Silk",
		  "Widow's Weave",
		  "Wraith Whisper",
		  "Siren's Serenade",
		  "Moonlit Mirage",
		  "Spectral Spark",
		  "Dragon's Roar",
		  "Banshee's Banshee",
		  "Witch's Whisper",
		  "Ghoul's Groan",
		  "Toadstool Tango",
		  "Vampire's Kiss",
		  "Bubbling Broth",
		  "Mystic Elixir",
		  "Cursed Charm"
		};
		
        private static readonly List<Ingredient> recipe = new List<Ingredient>() {
            new Ingredient("Phantom Firefly Wing"),
            new Ingredient("Ghastly Gourd"),
            new Ingredient("Hocus Pocus Powder"),
            new Ingredient("Spider Sling Silk"),
            new Ingredient("Goblin's Gold"),
            new Ingredient("Wraith's Tear"),
            new Ingredient("Werewolf Whisker"),
            new Ingredient("Ghoulish Goblet"),
            new Ingredient("Cursed Skull"),
            new Ingredient("Dragon's Scale Shimmer"),
            new Ingredient("Raven Feather"),
            new Ingredient("Dragon's Scale Shimmer"),
            new Ingredient("Zombie Zest Zest"),
            new Ingredient("Ghoulish Goblet"),
            new Ingredient("Werewolf Whisker"),
            new Ingredient("Cursed Skull"),
            new Ingredient("Dragon's Scale Shimmer"),
            new Ingredient("Haunted Hay Bale"),
            new Ingredient("Wraith's Tear"),
            new Ingredient("Zombie Zest Zest"),
            new Ingredient("Serpent Scale"),
            new Ingredient("Wraith's Tear"),
            new Ingredient("Cursed Crypt Key"),
            new Ingredient("Dragon's Scale Shimmer"),
            new Ingredient("Salamander's Tail"),
            new Ingredient("Raven Feather"),
            new Ingredient("Wolfsbane"),
            new Ingredient("Frankenstein's Lab Liquid"),
            new Ingredient("Zombie Zest Zest"),
            new Ingredient("Cursed Skull"),
            new Ingredient("Ghoulish Goblet"),
            new Ingredient("Dragon's Scale Shimmer"),
            new Ingredient("Cursed Crypt Key"),
            new Ingredient("Wraith's Tear"),
            new Ingredient("Black Cat's Meow"),
            new Ingredient("Wraith Whisper")
        };

		public static void Main() {
            Console.WriteLine("The spell is complete - your flag is: " + decodeFlag());
		}

        private static string decodeFlag() {
            
            List<byte> byteList = new List<byte>();

            // Loop through all ingredients in the inputted recipe
            foreach (Ingredient ing in Brewery.recipe)
            {
                // Find the array index of the ingredient in the main ingredient list
                int index = Array.IndexOf(Brewery.IngredientNames, ing.ToString());

                Console.Write(ing + ": " + index);

                // Add 32 to the value
                index += 32;

                Console.WriteLine(" + 32 = " + index + ", In ASCII is:  " + Encoding.ASCII.GetString(new byte[] { (byte)index } ));

                // Add the new value to the byte list
                byteList.Add((byte)(index));
            }

            // Assemble all the bytes in an array
            byte[] array = byteList.ToArray();

            // Encode the byte array as ASCII text and return
            return Encoding.ASCII.GetString(array);
        }
	}
}
```

In the original code, the flag is decoded using the following:
```cs
byte[] array = Brewery.recipe.Select<Ingredient, byte>((Func<Ingredient, byte>) (ing => (byte) (Array.IndexOf<string>(Brewery.IngredientNames, ing.ToString()) + 32))).ToArray<byte>();
```
This is a "lambda expression", which are a c# feature to allow a developer to do more with fewer lines of code. In this case, it's a bit hard to get my head around what exactly it's doing, so I re-wrote it as a standalone function that does the same thing, and commented what each line does so that I understand it. I included some `Console.Write` debugging to better understand what each step of the code was doing as it runs.

```cs
private static string decodeFlag() {            
    List<byte> byteList = new List<byte>();

    // Loop through all ingredients in the inputted recipe
    foreach (Ingredient ing in Brewery.recipe)
    {
        // Find the array index of the ingredient in the main ingredient list
        int index = Array.IndexOf(Brewery.IngredientNames, ing.ToString());

        Console.Write(ing + ": " + index);

        // Add 32 to the value
        index += 32;

        Console.WriteLine(" + 32 = " + index + ", In ASCII is:  " + Encoding.ASCII.GetString(new byte[] { (byte)index } ));

        // Add the new value to the byte list
        byteList.Add((byte)(index));
    }

    // Assemble all the bytes in an array
    byte[] array = byteList.ToArray();

    // Encode the byte array as ASCII text and return
    return Encoding.ASCII.GetString(array);
}
```

For each inputted ingredient, it finds it's position in the master `IngredientNames` list, adds 32 to it, and stores these values in a byte array. It then converts the byte array to an ASCII string.

So for example, the first ingredient is `Phantom Firefly Wing`, which is in index number `40` in the master ingredient list (array indexes in C# start at 0, so it's the 41st ingredient, but gets the number 40). 40 + 32 = 72. 72 [in ASCII](https://www.asciitable.com/) is `H`.

So, basically, each ingredient from the main list corresponds to an ACII character, and the recipe is just a way to encode the characters of the flag in a complicated way.

```
Phantom Firefly Wing: 40 + 32 = 72, In ASCII is:  H
Ghastly Gourd: 52 + 32 = 84, In ASCII is:  T
Hocus Pocus Powder: 34 + 32 = 66, In ASCII is:  B
Spider Sling Silk: 91 + 32 = 123, In ASCII is:  {
Goblin's Gold: 89 + 32 = 121, In ASCII is:  y
Wraith's Tear: 16 + 32 = 48, In ASCII is:  0
Werewolf Whisker: 85 + 32 = 117, In ASCII is:  u
Ghoulish Goblet: 82 + 32 = 114, In ASCII is:  r
Cursed Skull: 19 + 32 = 51, In ASCII is:  3
Dragon's Scale Shimmer: 63 + 32 = 95, In ASCII is:  _
Raven Feather: 20 + 32 = 52, In ASCII is:  4
Dragon's Scale Shimmer: 63 + 32 = 95, In ASCII is:  _
Zombie Zest Zest: 84 + 32 = 116, In ASCII is:  t
Ghoulish Goblet: 82 + 32 = 114, In ASCII is:  r
Werewolf Whisker: 85 + 32 = 117, In ASCII is:  u
Cursed Skull: 19 + 32 = 51, In ASCII is:  3
Dragon's Scale Shimmer: 63 + 32 = 95, In ASCII is:  _
Haunted Hay Bale: 80 + 32 = 112, In ASCII is:  p
Wraith's Tear: 16 + 32 = 48, In ASCII is:  0
Zombie Zest Zest: 84 + 32 = 116, In ASCII is:  t
Serpent Scale: 17 + 32 = 49, In ASCII is:  1
Wraith's Tear: 16 + 32 = 48, In ASCII is:  0
Cursed Crypt Key: 78 + 32 = 110, In ASCII is:  n
Dragon's Scale Shimmer: 63 + 32 = 95, In ASCII is:  _
Salamander's Tail: 77 + 32 = 109, In ASCII is:  m
Raven Feather: 20 + 32 = 52, In ASCII is:  4
Wolfsbane: 21 + 32 = 53, In ASCII is:  5
Frankenstein's Lab Liquid: 83 + 32 = 115, In ASCII is:  s
Zombie Zest Zest: 84 + 32 = 116, In ASCII is:  t
Cursed Skull: 19 + 32 = 51, In ASCII is:  3
Ghoulish Goblet: 82 + 32 = 114, In ASCII is:  r
Dragon's Scale Shimmer: 63 + 32 = 95, In ASCII is:  _
Cursed Crypt Key: 78 + 32 = 110, In ASCII is:  n
Wraith's Tear: 16 + 32 = 48, In ASCII is:  0
Black Cat's Meow: 87 + 32 = 119, In ASCII is:  w
Wraith Whisper: 93 + 32 = 125, In ASCII is:  }
```