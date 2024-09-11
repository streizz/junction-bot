import asyncio
import logging

from pyrogram.errors import FloodWait 
from aiogram import Bot, Dispatcher

from config import TOKEN
from app.handlers import router
from app.middlewares.data import DataMiddleware
from app.updater import update_loops


bot = Bot(token=TOKEN)
dp = Dispatcher()


async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    dp.include_router(router)


    try:
        print(f"Bot Junction V1.0 started!")
        await asyncio.gather(
            dp.start_polling(bot),
            update_loops(bot)
        )
    except FloodWait as e: 
        await asyncio.sleep(e.value)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')