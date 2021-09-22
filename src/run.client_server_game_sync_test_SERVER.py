# Note: this will stop working at one point

import asyncio

from game.engine import Engine
from server.server import Server

# server_game = Engine(debug=True, is_server=True, is_client=False)

# uuid = server_game.add_player()

# asyncio.get_event_loop().create_task(server_game.run())

s = Server(3001)
s.run()


# Run the loop
asyncio.get_event_loop().run_forever()
