import asyncio
import json
import traceback
from types import SimpleNamespace

import websockets

import packet

from .lobby import Lobby

from ..website.dcauth.auth_manager import AuthManager


class Server:
    def __init__(self, port):
        self.port = port

        # key: websocket value: SimpleNamespace
        self.clients = {}

        self.lobbies = {}

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
        try:
            async for message in websocket:
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

                client_id = packet_data.get("client_id", None)
                if client_id is None:
                    print("packet didn't have client_id")
                    return

                if len(client_id) > 100:
                    print("client id is too long")
                    return

                # Regiser the client
                # There is no way to unregister a client at the moment
                if client_id not in self.clients:
                    w = self.clients[client_id] = SimpleNamespace()
                    w.lobby = None
                    w.token = None
                    w.verified = False

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
                        if AuthManager.check(uuid):  # HERE HERE ADD AUTH
                            self.send_sync(
                                websocket, packet.Status(True, uuid=uuid).send()
                            )
                            self.clients[client_id].verified = True
                            print(client_id)
                        else:
                            self.send_sync(packet.Status(False, "Invalid Token").send())
                            self.clients[client_id].verified = False
                        return

                    if self.clients[client_id].verified:
                        # Get lobby request
                        if action_type == packet.RequestLobby.ACTION:
                            if self.clients[client_id].lobby:
                                # listen for game_init
                                self.send_sync(
                                    websocket,
                                    packet.Status(
                                        False, "Already in a lobby", uuid
                                    ).send(),
                                )
                            else:
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
