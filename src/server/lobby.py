import asyncio
import json
from uuid import uuid4

import websockets

import packet
from game.engine import Engine


class Lobby:
    def __init__(self, server):
        self.server = server
        self.ID = uuid4()
        self.engine = Engine(debug=True, is_server=True, is_client=False)
        asyncio.get_event_loop().create_task(self.engine.run())
        # Constantly update

        async def update_loop():
            # Get clients that are in this lobby
            event_stack = []

            def add_event(e, v):
                event_stack.append(e)

            self.engine.hook(add_event)
            while True:
                dump = self.engine.dump()
                print(dump)

                for client in list(server.clients.values()):
                    if client.lobby is None:
                        continue
                    if client.lobby.ID == self.ID:
                        asyncio.get_event_loop().create_task(
                            client.websocket.send(
                                packet.GamePacket(event_stack, dump).send()
                            )
                        )
                    event_stack = []
                await asyncio.sleep(5)

        asyncio.get_event_loop().create_task(update_loop())

    def add_player(self):
        uuid = self.engine.add_player()
        return uuid
