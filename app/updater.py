import asyncio
from app.services.pg import pg




async def update_loops(bot):
    while True:
        await asyncio.sleep(40)
        client = pg(bot)
        await client.pars()
        print('updated')