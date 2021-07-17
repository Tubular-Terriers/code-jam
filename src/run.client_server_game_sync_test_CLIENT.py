# Note: this will stop working at one point

import asyncio

from game.engine import Engine

client_game = Engine(debug=True, is_server=False, is_client=True)

# Before running the game, request a player from the server

asyncio.get_event_loop().create_task(client_game.run())

# Run the loop
asyncio.get_event_loop().run_forever()
