# July 9th

Created various GitHub and Discord automation

Tidied up our repository so every member can easily use it

We decided to not install pre-commit on every member's computer.
We went for a faster development speed instead

# July 10th

Almost every member did their first commit by adding their name on the readme

Lint action was acting up, but we found out that the error was rather a non-issue

We drafted our ideas on a shared drawing board

Our idea revolves around the game `pong` the first game ever created

![image](https://cdn.discordapp.com/attachments/799265265820237834/863442251634966559/unknown.png)

We decided to make a battle royale style pong game

Created the project structure with game, client, and server

![image](https://cdn.discordapp.com/attachments/862242420863139855/863488446328733736/unknown.png)

![image](https://cdn.discordapp.com/attachments/862242420863139853/863511003668676608/Untitled_Diagram_1.png)

# July 11th

Refined the pipeline structure of data and communications

![image](https://cdn.discordapp.com/attachments/862242420863139853/863805255904919552/unknown.png)

Since `curses window.getch` will be blocking or cost a lot of cpu, we have to use a non-blocking, event-based, asyncio compatible key reading library. Maybe we need a custom one

Our team split roles

curses team:
 * front end menu:
    * karthik
    * madara uchiha
 * front end game render:
    * mephew

backend-web team:
 * nope
 * nick

backend-engine team:
 * nope
 * joshuqa

We have new concept art as well

![image](https://media.discordapp.net/attachments/862242420863139855/863666768080928778/unknown.png)

The players are inside the box in this version

# July 12th

Finished the UI and Widget framework

Unlike curses, this framework is entirely asynchronous and callback based

This allows lively menus like this

![image](https://cdn.discordapp.com/attachments/862242420863139855/864174792713043988/widgetdemo.gif)

All thanks to the contribution of the members, we were able to create a new world above curses

Added a flowchart for the UI and Widget framework

![image](https://cdn.discordapp.com/attachments/862242420863139855/864218016437501982/rendering_framework.png)

Edited the pipeline framework so that the server structure is more explicit

![image](https://cdn.discordapp.com/attachments/862242420863139855/864217895622017064/pipeline_1.png)

Created fancy progress bar

![image](https://cdn.discordapp.com/attachments/776517583359967232/864227818266558494/progress_bar.gif)

Our backend team created a mapping diagram so entities can be loaded/unloaded

```json
[
  {
    "0": {
      "d3e76c82-dcd6-4a1e-a762-760a6948ec60": {
        "name": "obstacle",
        "type": "o",
        "x": 0,
        "y": 0,
        "w": 2
      },
      "02e4c3c1-b1fc-4336-af03-ab221983d5a6": {
        "name": "obstacle",
        "type": "o",
        "x": 3,
        "y": 0,
        "w": 3
      },
      "449298f6-1def-4103-a4b6-46e0c4be2fe0": {
        "name": "obstacle",
        "type": "o",
        "x": 3,
        "y": 1,
        "w": 1
      },
      "6fd438d2-c910-44ff-b283-808812d88fbc": {
        "name": "player",
        "type": "p",
        "x": 0,
        "y": 1,
        "w": 2
      },
      "dc7c8a0d-7e9f-4ac3-aab0-eaf62f8b9650": {
        "name": "player",
        "type": "p",
        "x": 5,
        "y": 1,
        "w": 2
      }
    }
  },
  {
    "1": {
      "5e617d97-10ed-495c-9544-40bb6901022f": {
        "name": "obstacle",
        "type": "o",
        "x": 0,
        "y": 0,
        "w": 2
      },
      "3f884497-0526-46cd-90a8-28d4af19399a": {
        "name": "obstacle",
        "type": "o",
        "x": 3,
        "y": 0,
        "w": 3
      },
      "945e91c1-7b68-4692-91ce-442466b095f2": {
        "name": "obstacle",
        "type": "o",
        "x": 3,
        "y": 1,
        "w": 1
      },
      "23c4174c-e7e3-4648-bde1-d644f5d11343": {
        "name": "player",
        "type": "p",
        "x": 0,
        "y": 1,
        "w": 2
      },
      "fb9aa93e-cc34-4a72-910e-4e31f7242a93": {
        "name": "player",
        "type": "p",
        "x": 5,
        "y": 1,
        "w": 2
      }
    }
  }
]
```

They also added a better testing ground

![image](https://cdn.discordapp.com/attachments/862242420863139855/864386058040508416/unknown.png)

# July 13th

Made an application state diagram

![image](https://media.discordapp.net/attachments/862242420863139855/864418416089366528/unknown.png)

Finally, created a custom keytext input handler and a textbox widget

When typing text, other keys do not affect the widget

![image](https://cdn.discordapp.com/attachments/862242420863139855/864527737195724800/textbox.gif)


Refined the textbox widget, so it includes other accessible api as well

Now keys like `ctrl+c` and `ctrl+backspace` does not appear on the screen and get ignored

It also has `is_pressed(key)` support

![image](https://cdn.discordapp.com/attachments/862242420863139855/864589327517220914/texboxdemo.gif)

![image](https://cdn.discordapp.com/attachments/862242420863139855/864590228190003200/is_pressed_demo.gif)

> The best part of this is that everything is non-blocking, and keyboard events are open, so it also supports instantaneous text rendering

Implemented support for Discord rich presence system

![image](https://cdn.discordapp.com/attachments/776517583359967232/864639192528846848/unknown.png)

Added files for background music and worked on creating engines for music and sound effects playback  
> Menu screen has its own non-copyrighted version of original tetris soundtrack  
> Loading screen has a few songs from which the music engine randomly selects one to play during each loading  
> Music in the core gameplay is being randomly shuffled throughout the play from a variety of non-copyrighted retro songs

# July 14th

Implemented sound system with separate engines for background music and sfx playback

Implemented new game engine with event hooks

The new game works good

We managed to extend `pymunk`'s native rigid body classes to `Entities`, making it easier for the `curses` rendering widget to process the game and show it on a text pad

This is the debug screen provided by `pygame`

![image](https://cdn.discordapp.com/attachments/862242420863139855/864963358146166815/PylwRFlBGr.gif)

Although this is nowhere near to end product, it has all the necessary components to be

Added basic user settings structure, providing additional abstraction layer for easy management of user config

# July 15th

Created diagram for advanced hitbox filtering for pymunk

![image](https://cdn.discordapp.com/attachments/862242420863139855/865167559099023360/unknown.png)

Based on the original pong game, the dimensions for the player has been mathematically calculated (our game is merely a 2 dimensional extension from the 1 dimensional pong game)

In an arena 600x600 with a virtual screen of 300x200, the player should be around 50 in length, and the collision box should be 5 in length

![image](https://cdn.discordapp.com/attachments/864018053640486932/865175800609505280/unknown.png)

Greatly improved user settings system

Created a dump and load method for entities

Now arbitrary physical data can be stored in `dict` form and loaded by the game engine

![image](https://cdn.discordapp.com/attachments/862242420863139855/865255252890746890/xxGX4nDDoR.gif)

Automatically attempt to reinitialize the curses window

![image](https://cdn.discordapp.com/attachments/862242420863139855/865265533237461022/0xMzpMQc66.gif)
