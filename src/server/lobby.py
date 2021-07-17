import asyncio
import json
from uuid import uuid4

import websockets

import packet


class Lobby:
    def __init__(self, server):
        self.server = server
        self.ID = uuid4()
