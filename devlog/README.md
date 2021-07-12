# July 9th

Created various GitHub and Discord automation

Tidied up our repository so every member can easily use it

We decided to not install pre-commit on every member's computer.
We went for a faster development speed instead

# July 10th

Almost every member did their first commit by adding their name on the readme

Lint action was acting up but nopeless found out that the error was rather a non-issue

We drafted out ideas on a shared drawing board

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
