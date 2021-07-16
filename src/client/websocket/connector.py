# handles with the websocket connection
# imports translation from the game engine
import asyncio
import json
import traceback

import websockets

import packet


class GameEventEmitter:
    def __init__(self, TOKEN):
        if TOKEN is None:
            raise Exception("TOKEN cannot be None")
        self.TOKEN = TOKEN
        self.ws_callback = lambda _: 0
        self.websocket = None
        self.verification = None
        self.initialized = False
        self.verified = False

    async def initialize_server_connection(self, url):
        self.initialized = True
        self.websocket = await websockets.connect(url)

        # Register process hook
        async def hook():
            while True:
                try:
                    data = await self.websocket.recv()
                    self.on_recv(data)
                except Exception as e:
                    if not self.websocket.open:
                        break

        asyncio.get_event_loop().create_task(hook())
        return True

    def on_recv(self, data):
        try:
            data = json.loads(data)
        except json.decoder.JSONDecodeError:
            """Error while loading dumps"""
            print(f"Recieved {data}. Not a valid json")
            return
        print(data)
        action_type = data["action"]
        pl = data["payload"]
        if action_type == packet.VerifyResponse.ACTION:
            print("verification packet recieved")
            p = packet.VerifyResponse.load(pl)
            print(p)
            if p.is_verified():
                self.verified = True
                print("is verified")
            else:
                self.verified = False
                print("verified fail")
            self.verification.cancel()

    def assert_init(self):
        if not self.initialized:
            raise Exception("server was not initialized")

    def assert_verficiation(self):
        if not self.verified:
            raise Exception("client was not verified")

    async def verify(self):
        self.assert_init()
        try:
            vp = packet.Verify(self.TOKEN)
            asyncio.create_task(self.websocket.send(vp.send()))
            await asyncio.sleep(10)
        except asyncio.CancelledError:
            return self.verified
        return False

    def set_hook():
        """Sets the callback (only 1 callback allowed)"""


# async def main():
#     url = "wss://echo.websocket.org/"

#     async with websockets.connect(url) as ws:
#         print("connected")


# asyncio.get_event_loop().run_until_complete(main())
