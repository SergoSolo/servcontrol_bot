from aiogram import Dispatcher, types
from bot.keyboard import admin_menu_keyboard, start_mune_keyboard
from core.config import bot
from core.db.repository.base import user_service


async def bot_start(message: types.Message):

    await bot.send_message(
        message.from_user.id,
        (
            "Привет! Данный бот создан для помощи инженерам. \n"
            "\nТут вы можете задать свой вопрос сотруднику ТП, "
            "а так же скачать все необходимые инструкции и файлы."
        ),
        reply_markup=start_mune_keyboard,
    )


async def admin(message: types.Message):
    if await user_service.is_staff(telegram_id=message.from_user.id):
        await bot.send_message(
            message.from_user.id,
            ("Добро пожаловать в меню администратора."),
            reply_markup=admin_menu_keyboard,
        )
    else:
        await bot.send_message(
            message.from_user.id, ("Вы не являетесь администратором.")
        )


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(bot_start, commands=["start", "help"])
    dp.register_message_handler(admin, commands=["admin"])
