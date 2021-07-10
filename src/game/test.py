import asyncio
import time

import engine

game = engine.Game()
# game.start()


i = 0
while True:
    i += 1
    game.render.update()
    time.sleep(0.1)

# async def main():
#     while True:
#         game.render.update()
#         print("print")


# asyncio.run(main())
