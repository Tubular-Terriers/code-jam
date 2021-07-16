# write argument parser here

# starts a ui

import asyncio

from client.only_game_app import app

# Someone set up a logger
# import logging


async def main():
    await app.run()


asyncio.run(main())
