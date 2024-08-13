import asyncio
from app.services.pg import pg
from config import SLEEP_TIME




async def update_loops(bot):
    while True:
        await asyncio.sleep(int(SLEEP_TIME))
        client = pg(bot)
        await client.pars()
        print('updated')