import asyncio
import json
import traceback
from types import SimpleNamespace

import websockets

import packet

from .lobby import Lobby


class Server:
    def __init__(self, port):
        self.port = port

        # key: websocket value: SimpleNamespace
        self.clients = {}

        self.lobbies = {}

        self.create_lobby()

        self.counter = 0

    def run(self):
        start_server = websockets.serve(self.application, "localhost", self.port)
        asyncio.get_event_loop().run_until_complete(start_server)

    def send_sync(self, websocket, data):
        return asyncio.create_task(websocket.send(data))

    def create_lobby(self):
        lob = Lobby(self)
        self.lobbies[lob] = lob

    def close_lobby(self, lobby):
        # clean up client data
        for client in list(self.clients.values()):
            if client.lobby.ID == lobby.ID:
                client.lobby = None

        self.lobbies.pop(lobby)

    async def application(self, websocket, path):
        # Ignore path
        self.counter += 1
        client_id = self.counter
        try:
            w = self.clients[client_id] = SimpleNamespace()
            w.lobby = None
            w.token = None
            w.verified = False
            w.websocket = None
            async for message in websocket:
                w.websocket = websocket
                print(websocket.__hash__())
                # Handle events
                print(message)
                packet_data = None
                try:
                    packet_data = json.loads(message)
                except json.JSONDecodeError:
                    print("invalid json")
                action_type = packet_data.get("action", "INVALID")
                pl = packet_data.get("payload", None)
                if action_type == "INVALID":
                    print("invalid action type")
                    continue
                if pl is None:
                    print("invalid payload")
                    continue

                # below might be triggered because of an invalid packet
                # or because there was an internal server error
                try:

                    # CALLBACK PACKETS
                    # Currently only the client sends call back packets
                    # so no need to implement a message manager
                    uuid = None
                    if "packet_id" in packet_data:
                        uuid = packet_data["packet_id"]
                        print(f"uuid was {uuid}")

                    # Verify packet
                    if action_type == packet.Verify.ACTION:
                        if True:  # HERE HERE ADD AUTH
                            self.send_sync(
                                websocket, packet.Status(True, uuid=uuid).send()
                            )
                            w.verified = True
                            print(client_id)
                        else:
                            self.send_sync(packet.Status(False, "Invalid Token").send())
                            w.verified = False
                        continue
                    print(w.verified)
                    if w.verified:
                        # Get lobby request
                        if action_type == packet.RequestLobby.ACTION:
                            if w.lobby:
                                # listen for game_init
                                self.send_sync(
                                    websocket,
                                    packet.Status(
                                        False, "Already in a lobby", uuid
                                    ).send(),
                                )
                            else:
                                # HERE HERE
                                w.lobby = list(self.lobbies.values())[0]
                                puuid = w.lobby.add_player()
                                self.send_sync(
                                    websocket,
                                    packet.Status(True, str(puuid), uuid=uuid).send(),
                                )
                        if action_type == packet.GamePacket.ACTION:
                            pass
                    else:
                        # Ignore the message
                        print("client sent a non verify packet without verification")

                    # STREAM PACKETS
                    # like game packeets
                except Exception:
                    traceback.print_exc()
        except websockets.exceptions.ConnectionClosed as e:
            print("client closed connection")
            self.clients.pop(websockets)
        except Exception as e:
            traceback.print_exc()
        finally:
            self.clients.pop(client_id, None)
