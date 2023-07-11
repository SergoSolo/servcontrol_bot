from aiogram import types
from aiogram.dispatcher import FSMContext

from app.bot.keyboard import (create_admin_keyboard,
                              create_registration_keyboard)
from app.bot.states import AdminMenu
from app.core.config import bot
from app.core.constants import UserRoleConstant
from app.core.db.repository import user_service


async def admin_menu(message: types.Message, state: FSMContext):
    user = await user_service.get_user_by_telegram_id(
        telegram_id=message.from_user.id
    )
    if user:
        if (
            user.role_id == UserRoleConstant.ADMIN.value
            or user.role_id == UserRoleConstant.MODERATOR.value
            and not user.is_banned
        ):
            await bot.send_message(
                message.from_user.id,
                (
                    "<i>Добро пожаловать в меню администратора.\n\n"
                    "В данном меню вы можете работать с пользователями, "
                    "файлами и категориями файлов.</i>"
                ),
                reply_markup=create_admin_keyboard(),
                parse_mode=types.ParseMode.HTML,
            )
            await state.set_state(AdminMenu.select_main_options.state)
            await message.delete()
        else:
            await bot.send_message(
                message.from_user.id,
                "<i>У вас нет доступа.</i>",
                parse_mode=types.ParseMode.HTML,
            )
            await state.finish()
    else:
        await bot.send_message(
            message.from_user.id,
            text=(
                "<i>Для работы с ботом вам необходимо зарегистрироваться.</i>"
            ),
            parse_mode=types.ParseMode.HTML,
            reply_markup=create_registration_keyboard(),
        )


async def cancel_option(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
