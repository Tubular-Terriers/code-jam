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
        self.engine = Engine(debug=False, is_server=True, is_client=False)
        asyncio.get_event_loop().create_task(self.engine.run())
        # Constantly update

        self.client_mappings = {}

        async def update_loop():
            # Get clients that are in this lobby
            event_stack = []

            # Not utilized for now
            def add_event(e, v):
                event_stack.append(e)

            self.engine.hook(add_event)
            try:
                while True:
                    dump = self.engine.dump()

                    # print(dump)

                    for client in list(server.clients.values()):
                        # print(list(server.clients.values()))
                        if client.lobby is None:
                            continue
                        if client.lobby.ID == self.ID:
                            # print("send")
                            asyncio.get_event_loop().create_task(
                                client.websocket.send(
                                    packet.GamePacket(event_stack, dump).send()
                                )
                            )
                            # print("send2")

                        event_stack = []
                    await asyncio.sleep(0.05)
            except Exception:
                print("HERE")

        asyncio.get_event_loop().create_task(update_loop())

    def on_recv(self, pl, id):
        # Only accept player controls
        keys = pl["events"]
        uuid = self.client_mappings[id]
        self.engine._process_player_keys(uuid, keys)

    def add_player(self, client_id):
        uuid = self.engine.add_player()
        self.client_mappings[client_id] = uuid
        return uuid
