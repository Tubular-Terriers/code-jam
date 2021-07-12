# write argument acceptor here

# import game engine and do server side calculations/validations
# broadcast states to all clients

import argparse
import threading

import game

parser = argparse.ArgumentParser(description="Server for Pong Console")
parser.add_argument("address", help="Server port [port]")
# Add these options later
# parser.add_argument("-p", "--players", default=10, type=int, help="Max player count")
# parser.add_argument(
#     "-i",
#     "--instances",
#     default=100,
#     type=int,
#     help="Sets the amount of game instances running ",
# )
# parser.add_argument(
#     "-x",
#     "--minimum",
#     default=2,
#     type=int,
#     help="Wait for a minimum of count of players to start",
# )
# parser.add_argument(
#     "-s",
#     "--startanyway",
#     default=60,
#     type=int,
#     help="Wait for amount time before starting the game",
# )

# threading.Thread(target=server.listen_clients, daemon=True).start()
