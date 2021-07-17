# handles with the websocket connection
# imports translation from the game engine
import asyncio
import json
import traceback
from uuid import uuid4

import websockets

import packet


class GameEventEmitter:
    def __init__(self, TOKEN):
        if TOKEN is None:
            raise Exception("TOKEN cannot be None")
        self.TOKEN = TOKEN
        self.ws_callback = lambda _: 0
        self.websocket = None
        self.initialized = False
        self.verified = False

        self.game = None

        self.messages = {}
        self.tasks = {}
        self.disconnected = False

        self.player_uuid = None

    async def initialize_server_connection(self, url):
        self.initialized = True
        websocket = websockets.connect(url)

        # Register process hook
        async def hook():
            async with websocket as ws:
                self.websocket = ws
                while True:
                    # try:
                    data = await self.websocket.recv()
                    self.on_recv(data)

        # send keymaps
        async def update_keymaps():
            while not self.disconnected:
                await asyncio.sleep(0.05)
                if not self.game:
                    continue

                async def sendc():
                    try:
                        return await self.websocket.send(
                            packet.GamePacket(events=self.game.key_map).send()
                        )
                    except Exception:
                        self.disconnected = True

                asyncio.get_event_loop().create_task(sendc())

        self.h = asyncio.create_task(hook())
        self.u = asyncio.create_task(update_keymaps())
        # no time to implement
        await asyncio.sleep(1)
        return True

    def on_init(self, game):
        self.game = game

    def on_recv(self, data):
        # print(f"recieved {data}")
        packet_data = None
        try:
            packet_data = json.loads(data)
        except json.decoder.JSONDecodeError:
            """Error while loading dumps"""
            print(f"Recieved {data}. Not a valid json")
            return
        # print(data)
        action_type = packet_data["action"]
        pl = packet_data["payload"]

        # Callback packets
        if "packet_id" in packet_data:
            print("has packet id")
            self.messages[packet_data["packet_id"]] = pl
            self.tasks[packet_data["packet_id"]].cancel()
            return

        # Stream packets
        if action_type == packet.GamePacket.ACTION:
            if self.game:
                self.game.load(pl["entities"])
        # if action_type == packet.VerifyResponse.ACTION:
        #     print("verification packet recieved")
        #     p = packet.VerifyResponse.load(pl)
        #     print(p)
        #     if p.is_verified():
        #         self.verified = True
        #         print("is verified")
        #     else:
        #         self.verified = False
        #         print("verified fail")
        #     self.verification.cancel()

    async def send_packet_expect_response(self, packet_data: object, id):
        """Sends a packet and returns the response packet in dict. Returns None if there was no response"""
        assert self.websocket is not None
        id = None
        # print(packet_data)
        try:
            id = packet_data.packet_id
        except Exception:
            raise Exception("packet does not have a packet id")
        try:
            asyncio.create_task(self.send(self.websocket, packet_data))
            # timeout
            task = asyncio.create_task(asyncio.sleep(10))
            self.tasks[str(id)] = task
            await task
        except asyncio.CancelledError:
            msg = self.messages.get(str(id), None)
            self.messages.pop(str(id), None)
            return msg
        self.messages.pop(str(id), None)
        return None

    def assert_init(self):
        if not self.initialized:
            raise Exception("server was not initialized")

    def assert_verficiation(self):
        if not self.verified:
            raise Exception("client was not verified")

    def send_sync(self, websocket, packet):
        try:
            asyncio.create_task(self.send(websocket, packet))
        except Exception:
            traceback.print_exc()

    async def send(self, websocket, packet_data):
        return await websocket.send(packet_data.send())

    async def verify(self):
        self.assert_init()
        vp = packet.Verify(self.TOKEN)
        res = await self.send_packet_expect_response(vp, vp.packet_id)
        pl = packet.Status.load(res)
        print(pl)
        if pl.status:
            return True
        return False

    async def get_lobby(self) -> str:
        self.assert_init()
        lp = packet.RequestLobby()
        res = await self.send_packet_expect_response(lp, lp.packet_id)
        pl = packet.Status.load(res)
        if res is None:
            return False
        print(pl)
        return pl.error  # This returns the uuid

    #     try:
    #         vp = packet.Verify(self.TOKEN)
    #         asyncio.create_task(self.websocket.send(vp.send()))
    #         await asyncio.sleep(10)
    #     except asyncio.CancelledError:
    #         return self.verified
    #     return False

    def set_hook():
        """Sets the callback (only 1 callback allowed)"""

    def destroy(self):
        try:
            self.h.cancel()
            self.u.cancel()
        except Exception:
            """Connection was not initialized anyway"""
            pass


# async def main():
#     url = "wss://echo.websocket.org/"

#     async with websockets.connect(url) as ws:
#         print("connected")


# asyncio.get_event_loop().run_until_complete(main())
