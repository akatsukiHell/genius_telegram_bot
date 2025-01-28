import asyncio
import logging
import sys
import os
import dotenv

from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties


router = Router()

async def main():
    dotenv.load_dotenv()
    bot = Bot(os.getenv("BOT_TOKEN"), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    try:
        dp.include_router(router)
        await dp.start_polling(bot)
        await bot.session.close()
    except Exception as ex:
        print(f'{ex}')


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, 
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s", 
        stream=sys.stdout)
    asyncio.run(main())