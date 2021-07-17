import asyncio

from game.engine import Engine

print("starting game")


game = Engine(debug=True)

game.add_player()

asyncio.get_event_loop().run_until_complete(game.run())

# Run the loop
asyncio.get_event_loop().run_forever()
