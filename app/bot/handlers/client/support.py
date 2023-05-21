from aiogram import types
from aiogram.dispatcher import FSMContext

from app.bot.keyboard import (cancel_support, check_support_available,
                              create_registration_keyboard,
                              get_support_manager, support_keyboard)
from app.bot.states import Support
from app.core.config import bot, dp
from app.core.constants import UserRoleConstant
from app.core.db.repository import user_service


async def support(message: types.Message, state: FSMContext):
    user = await user_service.get_user_by_telegram_id(
        telegram_id=message.from_user.id
    )
    if user:
        text = (
            "<i>Если хотите проинформировать сотрудника ТП, "
            "нажмите на кнопку ниже.</i>"
        )
        keyboard = await support_keyboard(messages="one")
        await state.set_state(Support.support_command.state)
        await message.answer(
            text, reply_markup=keyboard, parse_mode=types.ParseMode.HTML
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


async def send_to_support(
    call: types.CallbackQuery, state: FSMContext, callback_data: dict
):
    user_id = int(callback_data.get("user_id"))
    await call.message.edit_text(
        "<i>Пришлите ваше сообщение.</i>", parse_mode=types.ParseMode.HTML
    )
    await state.set_state(Support.wait_for_support.state)
    await state.update_data(second_id=user_id)


async def get_support_message(message: types.Message, state: FSMContext):
    data = await state.get_data()
    support_ids = await user_service.get_users_telegram_ids_by_role(
        role_id=UserRoleConstant.MODERATOR.value
    )
    second_id = data["second_id"]
    client = await user_service.get_user_by_telegram_id(
        telegram_id=message.from_user.id
    )
    keyboard = await support_keyboard(
        messages="one", user_id=message.from_user.id
    )
    if second_id in support_ids:
        await bot.send_message(
            second_id,
            (
                f"<i>Вам пришло сообщение!\n"
                f"Инженер: {client.get_full_name()}.\n"
                f"Город: {client.town}.\nСообщение: {message.text}</i>"
            ),
            reply_markup=keyboard,
            parse_mode=types.ParseMode.HTML,
        )
        await message.answer(
            "<i>Ваше сообщение передано сотруднику ТП.</i>",
            parse_mode=types.ParseMode.HTML,
        )
        await state.reset_state()
    else:
        await message.copy_to(second_id)
        await message.answer(
            "<i>Ваше сообщение передано пользователю.</i>",
            parse_mode=types.ParseMode.HTML,
        )
        await state.reset_state()


async def support_call(message: types.Message, state: FSMContext):
    user = await user_service.get_user_by_telegram_id(
        telegram_id=message.from_user.id
    )
    if user:
        text = (
            "<i>Если хотите начать диалог с сотрудником ТП, "
            "нажмите на кнопку ниже.</i>"
        )
        keyboard = await support_keyboard(messages="many")
        await state.set_state(Support.support_command.state)
        await message.answer(
            text, reply_markup=keyboard, parse_mode=types.ParseMode.HTML
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


async def start_dailog_support(
    call: types.CallbackQuery, state: FSMContext, callback_data: dict
):
    user = await user_service.get_user_by_telegram_id(
        telegram_id=call.from_user.id
    )
    support_ids = await user_service.get_users_telegram_ids_by_role(
        role_id=UserRoleConstant.MODERATOR.value
    )
    support_id = await get_support_manager(support_ids)
    # keyboard_second_user = cancel_support(user_id=call.from_user.id)
    await call.message.edit_text(
        "<i>Вы обратились к сотруднику ТП. Ждем ответа от ТП.</i>",
        parse_mode=types.ParseMode.HTML
        # reply_markup=keyboard_second_user,
    )
    user_id = int(callback_data.get("user_id"))
    if not await check_support_available(user_id):
        support_id = await get_support_manager(support_ids)
    else:
        support_id = user_id
    if not support_id:
        await call.message.edit_text(
            "<i>К сожалению оператор сейчас занят. Попробуйте позже.</i>",
            parse_mode=types.ParseMode.HTML,
        )
        await state.finish()
        return
    await state.set_state(Support.wait_in_support.state)
    await state.update_data(second_id=support_id)
    keyboard = await support_keyboard(
        messages="many", user_id=call.from_user.id
    )
    await bot.send_message(
        support_id,
        (
            f"<i>С вами хочет связаться\nИнженер: "
            f"{user.get_full_name()}\nГород: {user.town}</i>"
        ),
        reply_markup=keyboard,
        parse_mode=types.ParseMode.HTML,
    )


async def answer_support_call(
    call: types.CallbackQuery, state: FSMContext, callback_data: dict
):
    second_id = int(callback_data.get("user_id"))
    user_state = dp.current_state(user=second_id, chat=second_id)
    if str(await user_state.get_state()) != str(Support.wait_in_support.state):
        await call.message.edit_text(
            "<i>К сожалению, пользователь уже передумал.</i>",
            parse_mode=types.ParseMode.HTML,
        )
        await user_state.finish()
        return
    await state.set_state(Support.in_support.state)
    await user_state.set_state(Support.in_support.state)
    await state.update_data(second_id=second_id)
    keyboard = cancel_support(user_id=second_id)
    # keyboard_second_user = cancel_support(user_id=call.from_user.id)
    await call.message.edit_text(
        (
            "<i>Вы на связи с пользователем. "
            "Чтобы завершить нажмите на кнопку.</i>"
        ),
        reply_markup=keyboard,
        parse_mode=types.ParseMode.HTML,
    )
    await bot.send_message(
        second_id,
        "<i>Оператор включился в разговор. Задайте свои вопросы.</i>",
        # reply_markup=keyboard_second_user,
        parse_mode=types.ParseMode.HTML,
    )


async def not_supported(message: types.Message, state: FSMContext):
    data = await state.get_data()
    second_id = data.get("second_id")
    keyboard = cancel_support(user_id=second_id)
    await message.answer(
        (
            "<i>Дождитесь ответа струдника или "
            "нажмите кнопку для отмены ниже.</i>"
        ),
        reply_markup=keyboard,
        parse_mode=types.ParseMode.HTML,
    )


async def exit_support(
    call: types.CallbackQuery, state: FSMContext, callback_data: dict
):
    user_id = int(callback_data.get("user_id"))
    second_state = dp.current_state(user=user_id, chat=user_id)
    if await second_state.get_state() is not None:
        data_second = await second_state.get_data()
        second_id = data_second.get("second_id")
        if int(second_id) == call.from_user.id:
            await second_state.reset_state()
            await bot.send_message(
                user_id,
                "<i>Пользователь завершил сеанс техподдержки.</i>",
                parse_mode=types.ParseMode.HTML,
            )
    await call.message.edit_text(
        "<i>Вы завершили сеанс.</i>", parse_mode=types.ParseMode.HTML
    )
    await state.finish()
