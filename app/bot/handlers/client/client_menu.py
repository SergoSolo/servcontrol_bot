from aiogram import types
from aiogram.dispatcher import FSMContext

from app.bot.keyboard import (
    create_acception_keyboard,
    create_cancel_keyboard,
    create_registration_keyboard,
)
from app.bot.states import ClientMenu
from app.bot.utils import validate
from app.core.config import bot
from app.core.constants import UserRoleConstant
from app.core.db.repository import user_service


async def main_client_menu(message: types.Message, state: FSMContext):
    user = await user_service.get_user_by_telegram_id(
        telegram_id=message.from_user.id
    )
    if user:
        if user.is_banned:
            await bot.send_message(message.from_user.id, "Вы забанены.")
            await state.finish()
        await bot.send_message(
            message.from_user.id,
            text=(
                f"<i><b>Привет, {user.first_name}!</b>"
                "\n\nДанный бот создан для помощи инженерам. "
                "У бота есть следующие команды:\n\n"
                "/info - <b>Важная информация с которой "
                "необходимо ознакомиться❗</b>\n\n"
                "/files - вы можете получить определенные "
                "инструкции, файлы, акты и т.д.\n\n"
                "/support - вы можете проинформировать сотрудника "
                "ТП одним сообщением о неисправности функционала "
                "бота и т.п.\n\n/support_call - вы можете начать диалог "
                "c сотрудником ТП для решения рабочих проблем.\n\n"
                "/admin - рабочая панель администратора.\n\n"
                "Для удаления сообщения нажмите ❌</i>"
            ),
            reply_markup=create_cancel_keyboard(),
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
        await state.set_state(ClientMenu.user_registeration.state)


async def client_input_first_name(
    call: types.CallbackQuery, state: FSMContext
):
    await call.message.edit_text(
        "<i>Введите имя.</i>", parse_mode=types.ParseMode.HTML
    )
    await state.set_state(ClientMenu.input_first_name.state)


async def client_input_last_name(message: types.Message, state: FSMContext):
    if validate(message.text):
        await state.update_data(
            first_name=message.text.capitalize(),
            telegram_id=message.from_user.id,
        )
        await bot.send_message(
            message.from_user.id,
            "<i>Введите фамилию.</i>",
            parse_mode=types.ParseMode.HTML,
        )
        await state.set_state(ClientMenu.input_last_name.state)
    else:
        await bot.send_message(
            message.from_user.id,
            "Имя должно быть написано на русском без чисел и пробелов.",
        )


async def client_input_town(message: types.Message, state: FSMContext):
    if validate(message.text):
        await state.update_data(last_name=message.text.capitalize())
        await bot.send_message(
            message.from_user.id,
            "<i>Введите свой город.</i>",
            parse_mode=types.ParseMode.HTML,
        )
        await state.set_state(ClientMenu.input_town.state)
    else:
        await bot.send_message(
            message.from_user.id,
            "Фамилия должена быть написана на русском без чисел и пробелов.",
        )


async def data_reconciliation(message: types.Message, state: FSMContext):
    if validate(message.text):
        await state.update_data(town=message.text.capitalize())
        user_data = await state.get_data()
        await bot.send_message(
            message.from_user.id,
            (
                f"<i>Давайте сверимся.\nФИО: {user_data.get('first_name')} "
                f"{user_data.get('last_name')}\nГород: "
                f"{user_data.get('town')}\nВсе верно?</i>"
            ),
            parse_mode=types.ParseMode.HTML,
            reply_markup=create_acception_keyboard(),
        )
        await state.set_state(ClientMenu.reconciliation.state)
    else:
        await bot.send_message(
            message.from_user.id,
            "Город должн быть написан на русском без чисел и пробелов.",
        )


async def user_registration(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    user_data = await state.get_data()
    moderators = await user_service.get_users_telegram_ids_by_role(
        role_id=UserRoleConstant.MODERATOR.value
    )
    await user_service.create_object(user_data)
    for moderator in moderators:
        await bot.send_message(
            moderator,
            (
                "<i><b>Зарегистрировался новый пользователь.</b>\n\n"
                f"Инженер {user_data.get('first_name')} "
                f"{user_data.get('last_name')} из города "
                f"{user_data.get('town')}</i>"
            ),
            parse_mode=types.ParseMode.HTML,
        )
    await state.finish()
    return await main_client_menu(call, state)


async def restart_user_registration(
    call: types.CallbackQuery, state: FSMContext
):
    await call.message.edit_text(
        "<i>Повторное прохождение регистрации.</i>",
        parse_mode=types.ParseMode.HTML,
        reply_markup=create_registration_keyboard(),
    )
