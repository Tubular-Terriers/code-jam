import asyncio

from client.websocket import GameEventEmitter


async def main():
    gee = GameEventEmitter("my token")
    uri = "ws://localhost:3001"
    if await gee.initialize_server_connection(uri):
        print("successfully connected to server!")
        try:
            await gee.verify()
        except Exception as e:
            print(e)
            print("errro")


asyncio.get_event_loop().run_until_complete(main())
asyncio.get_event_loop().run_forever()
