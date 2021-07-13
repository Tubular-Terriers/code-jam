# handles with the websocket connection
# imports translation from the game engine
import asyncio

import websockets


async def main():
    url = "wss://echo.websocket.org/"

    async with websockets.connect(url) as ws:
        print("connected")


asyncio.get_event_loop().run_until_complete(main())
