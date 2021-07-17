# Note: this will stop working at one point

import asyncio
import traceback

from pynput import keyboard

import packet
from client.websocket import GameEventEmitter
from game.engine import Engine
from game.events.move_player import MovePlayer


# Before running the game, request a player from the server
async def main():
    gee = GameEventEmitter("my token")
    print("made client")
    await gee.initialize_server_connection("ws://localhost:3001")

    status = await gee.verify()
    if status:
        print("verified")
    else:
        print("something went wrong")
        return
    lobby = await gee.get_lobby()
    if lobby:
        print("yes")
    else:
        print("no")

    print(lobby)

    client_game = Engine(
        debug=True, is_server=False, is_client=True, ignore_self_control=True
    )
    client_game.add_player(lobby)
    gee.on_init(client_game)

    await client_game.run()

    while True:
        # simulate inputs
        client_game.update_keymap(False, True, False, False, False, False, False, False)
        await asyncio.sleep(0.1)

    # print(status.is_ok)


asyncio.get_event_loop().create_task(main())

# Run the loop
asyncio.get_event_loop().run_forever()
