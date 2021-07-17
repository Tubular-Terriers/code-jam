# write argument acceptor here

# import game engine and do server side calculations/validations
# broadcast states to all clients

import argparse
import asyncio
import json
import logging

import websockets

import game
import packet

# flake8: noqa

parser = argparse.ArgumentParser(description="Server for Pong Console")
# parser.add_argument("address", help="Server port [port]")
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
# logging.basicConfig()

# STATE = {"value": 0}

# USERS = set()


# def state_event():
#     return json.dumps({"type": "state", **STATE})


# def users_event():
#     return json.dumps({"type": "users", "count": len(USERS)})


# async def notify_state():
#     if USERS:  # asyncio.wait doesn't accept an empty list
#         message = state_event()
#         await asyncio.wait([user.send(message) for user in USERS])


# async def notify_users():
#     if USERS:  # asyncio.wait doesn't accept an empty list
#         message = users_event()
#         for user in USERS:
#             asyncio.create_task(user.send(message))


# async def register(websocket):
#     USERS.add(websocket)
#     await notify_users()


# async def unregister(websocket):
#     USERS.remove(websocket)
#     await notify_users()


async def counter(websocket, path):
    # register(websocket) sends user_event() to websocket
    # await register(websocket)
    try:
        async for message in websocket:
            print(message)
            data = json.loads(message)
            action_type = data.get("action", "INVALID")
            if action_type == "INVALID":
                continue
            print("processing")
            pl = data["payload"]
            print(f"action {action_type} recieved")
            if action_type == packet.Verify.ACTION:
                p = packet.Verify.load(pl)
                print(f"token is {p.token}")
                if True:  # HERE HERE This is a debug line
                    asyncio.create_task(
                        websocket.send(packet.VerifyResponse(True).send())
                    )
                    print("debug true so token is validated")
                elif p.token[-1] == "n":
                    asyncio.create_task(
                        websocket.send(packet.VerifyResponse(True).send())
                    )
                    print("valid token")
                else:
                    asyncio.create_task(
                        websocket.send(
                            packet.VerifyResponse(False, "Invalid token").send()
                        )
                    )
    except websockets.exceptions.ConnectionClosed as e:
        print("client abruptly closed connection")
    # try:
    #     await websocket.send(state_event())
    #     # Eternal loop
    #     async for message in websocket:
    #         try:
    #             data = json.loads(message)
    #             if data["action"] == "minus":
    #                 STATE["value"] -= 1
    #                 await notify_state()
    #             elif data["action"] == "plus":
    #                 STATE["value"] += 1
    #                 await notify_state()
    #             else:
    #                 logging.error("unsupported event: %s", data)
    #         except:
    #             logging.error("client sent an invalid packet and crashed the code")
    # finally:
    #     await unregister(websocket)


start_server = websockets.serve(counter, "localhost", 3001)

asyncio.get_event_loop().run_until_complete(start_server)
if __name__ == "__main__":
    asyncio.get_event_loop().run_forever()
