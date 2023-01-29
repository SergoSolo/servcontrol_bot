import asyncio

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from bot.start import register_handlers
from core.config import logger_config, settings


async def main():
    logger_config()
    storage = MemoryStorage()
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher(bot, storage=storage)
    register_handlers(dp)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
