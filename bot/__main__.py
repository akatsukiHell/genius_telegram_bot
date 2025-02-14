import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode


from fluent_loader import get_fluent_localization

from congif_reader import Settings
from handlers import commands, callbacks

async def main():
    logging.basicConfig(level=logging.WARNING),
    config = Settings()

    bot = Bot(
        token=config.bot_token.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    l10n = get_fluent_localization(config.bot_language)

    dp = Dispatcher(
        l10n=l10n,
        config=config
    )
    
    dp.include_router(commands.router)
    dp.include_router(callbacks.router)


    try:
        await dp.start_polling(bot)
    except:
        await bot.session.close()
        
if __name__ == "__main__":
    asyncio.run(main())