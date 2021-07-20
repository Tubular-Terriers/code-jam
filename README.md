# Poing, the obvious remix

Most people, when thinking of revolutionary game ideas, try to make their game nothing like the games before. We took a "Think Inside The Box" approach.

# The box

The first game ever developed was `Pong` in `Nov 29, 1972`. The game was nothing in terms of graphics, controls and even user interface. Fast forward to `2021` we now have all the technology to make this old fashioned game one of the leading multiplayer one

# The plan

`pymunk`
> An actual physics engine that can handle better edge cases than traditional ones. It also allows customization of collisions which allows us to create conditional physics. Compared to the silly 1 dimensional space in `Pong`, this new engine will allow a new experience to a low resolution physics sim

`pygame`
> An excellent framework to allow debugging of the physics engine, and a surprisingly? great tool for creating the sound engine.

`curses`
> The core and backbone of our application. Every module in our project is written with the final implementation to a core curses library in mind. This flexible and low level api allowed us to create our own update schemes

`keyboard`
> `curses` was extremely limited in terms of keyboard, and of course, we couldn't allow such compromises. A `pyinput.keyboard` module would perfectly suit our needs of checking if a key is up or down. To integrate this with our new `curses` UI framework, we developed a cascading event passing structure

`event handlers`
> Even if `pynput.keyboard` works nice on its own, its hard to manage which button is actually listening to an event. So, we changed the structure to a recursive stacking call structure (imagine a waterfall) to allow easier debugging and structural organization.

`websockets`
> What is a fighting game without multiplayer support? NOTHING! `websockets` allows the communication between players to virtually interact with each other.

`server verification`
> But how can we ensure that only verified people can join the game? Well, by introducing server verfication of course. By passing a token on connecting to the server, we can identify the person who logged in. This way, banning that player would be an easy trick as well.

`django`
> The best way to verify people in a code jam from a discord server is, without a doubt, a discord oauth application. The django website is actually a bridge between our oauth application. Once someone is verified, the website shows a button so you can copy your token

`pygame.mixer`
> The pong game had a reminiscent `ping, pong` sound. We wanted to deliver this sensation to our players. Introducing `pygame.mixer`, a module that can support the playback of multiple sounds, perfect for multi-event concurring online play

`json`
> `json` based messaging system provided us with an easy way to debug our code. Using postman to script and send verification code and game packet code allowed easier testing than using small python scripts. It was also easy to read, as `print(payload)` would just print the dictionary to the console. Double win for us. We might have used python's `pickle`, but we found out that using `json` was better for short term development

`application state manager`
> Our ui system is actuallly multiple screens attached. Each ui handles its own inputs and events. So what is a good way to check if these ui states work correctly? An application state manager. By structuring our `app` to have a `while True` loop with multiple ui's being awaited to return a new app state, developing a ui has never been more easier

`ui pipeline`
> The ui system is layered like an onion. A single keypress to change the ui screen goes through `Keyboard -> App -> UI -> Widget` just to be processed. This organization structure might be daunting to visualize. This is why we developed a ui pipeline that shows all of this

`data pipelines`
> The game data can go in all places. It is important to know whether a module is above or below another. Sometimes, two modules have to coexist. This is why a nice data pipeline diagram can help our developers make modules.

# Developers

> [nopeless](https://github.com/nopeless) - Team leader  
> [Nickhil](https://github.com/Nickhil1737) - Team member  
> [MePhew](https://github.com/Me-Phew) - Team member  
> [Karthik_Mv](https://github.com/karthikmurakonda) - Team member  
> [nobalpha](https://github.com/nobalpha) - Team member  
> [madara uchiha](https://github.com/pritansh-sahsani) - Team member
