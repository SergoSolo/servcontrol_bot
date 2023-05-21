from aiogram import types
from aiogram.dispatcher import FSMContext

from app.bot.keyboard import create_help_keyboard, create_registration_keyboard
from app.core.config import bot
from app.core.db.repository import user_service


async def help_command(message: types.Message, state: FSMContext):
    user = await user_service.get_user_by_telegram_id(
        telegram_id=message.from_user.id
    )
    if user:
        await bot.send_message(
            message.from_user.id,
            (
                "<b>❗❗ВАЖНАЯ ИНФОРМАЦИЯ❗❗</b>\n\n"
                "<b><i>Для упрощения вашей работы, у вас должна быть "
                "флешка с данным образом!</i></b> \n\n"
                "<i>Основные программы для диагностики:\n"
                "HDD - Victoria и crystal disk info\n"
                "ОЗУ - Memtest86\n"
                "CPU и не только - Aida64\n\n"
                "Live CD является операционной системой, "
                "загружаемой с любых носителей. Она не требует "
                "установки на жесткий диск компьютера. Операционные "
                "системы такого типа чаще всего применяют для реанимации ПК "
                "или диагностики компонентов ПК.\n\n"
                "Для удаления сообщения нажмите ❌</i>"
            ),
            reply_markup=create_help_keyboard(),
            parse_mode=types.ParseMode.HTML,
        )
        await message.delete()
    else:
        await bot.send_message(
            message.from_user.id,
            text=(
                "<i>Для работы с ботом вам необходимо зарегистрироваться.</i>"
            ),
            parse_mode=types.ParseMode.HTML,
            reply_markup=create_registration_keyboard(),
        )
