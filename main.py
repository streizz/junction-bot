import asyncio
import logging

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


    # запускаем бота параллельно с циклом парсера
    try:
        print(f"Bot Junction V1.0 started!")
        await asyncio.gather(
            dp.start_polling(bot),
            update_loops(bot)
        )
    finally:
        await bot.session.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')