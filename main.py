import asyncio

from aiogram import Dispatcher, types

from app.bot.register import main_register_handlers
from app.bot.support_middlware import SupportMiddleware
from app.core.config import bot, dp, logger_config


async def set_default_commands(dp: Dispatcher):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Главное меню."),
            types.BotCommand("info", "Диагностическая флешка."),
            types.BotCommand("files", "Полезные файлы для работы."),
            types.BotCommand("support", "Сообщение сотруднику ТП."),
            types.BotCommand("support_call", "Диалог с сотрудником ТП."),
            types.BotCommand("admin", "Меню администратора."),
        ]
    )


async def start_bot():
    logger_config()
    await set_default_commands(dp)
    main_register_handlers(dp)
    dp.middleware.setup(SupportMiddleware())
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(start_bot())
