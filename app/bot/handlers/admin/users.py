from aiogram import types
from aiogram.dispatcher import FSMContext

from app.bot.keyboard import (create_users_keyboard,
                              create_users_option_keyboard)
from app.bot.states import AdminMenu
from app.core.constants import UserRoleConstant
from app.core.db.repository import user_service


async def selected_users_option(call: types.CallbackQuery, state: FSMContext):
    user = await user_service.get_user_by_telegram_id(
        telegram_id=call.from_user.id
    )
    await state.update_data(current_user_role=user.role_id)
    await call.message.edit_text(
        "<i>Выберите с какими пользователями вы хотите работать.</i>",
        reply_markup=create_users_keyboard(user_role=user.role_id),
        parse_mode=types.ParseMode.HTML,
    )
    await state.set_state(AdminMenu.selected_users_options.state)


async def users_options(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    role_id = int(call.data.split(":")[2])
    is_banned = bool(int(call.data.split(":")[3]))
    users = await user_service.get_users_by_filters(
        role_id=role_id, is_banned=is_banned
    )
    if len(users) == 0:
        await call.message.answer(
            "<i>В данной категории нет пользователей.</i>",
            parse_mode=types.ParseMode.HTML,
        )
    else:
        await state.update_data(objects=users)
        await call.message.edit_text(
            "<i>Выберите действие.</i>",
            reply_markup=create_users_option_keyboard(
                call.data, data.get("current_user_role")
            ),
            parse_mode=types.ParseMode.HTML
        )
        await state.set_state(AdminMenu.select_user_work_options.state)


async def delete_user(call: types.CallbackQuery, state: FSMContext):
    user = await user_service.get_object(
        object_id=int(call.data.split(":")[3])
    )
    await user_service.delete_object(object_id=int(call.data.split(":")[3]))
    await call.message.edit_text(
        f"<i>Пользователь {user.get_full_name()} удален.</i>",
        parse_mode=types.ParseMode.HTML,
    )
    await state.finish()


async def add_moderator(call: types.CallbackQuery, state: FSMContext):
    user = await user_service.get_object(
        object_id=int(call.data.split(":")[3])
    )
    await user_service.update_object(
        object_id=int(call.data.split(":")[3]),
        data={"role_id": UserRoleConstant.MODERATOR.value},
    )
    await call.message.edit_text(
        f"<i>{user.get_full_name()} добавлен в модераторы.</i>",
        parse_mode=types.ParseMode.HTML,
    )
    await state.finish()


async def remove_moderator(call: types.CallbackQuery, state: FSMContext):
    user = await user_service.get_object(
        object_id=int(call.data.split(":")[3])
    )
    await user_service.update_object(
        object_id=int(call.data.split(":")[3]),
        data={"role_id": UserRoleConstant.USER.value},
    )
    await call.message.edit_text(
        f"<i>{user.get_full_name()} убран из модераторов.</i>",
        parse_mode=types.ParseMode.HTML,
    )
    await state.finish()


async def add_to_blacklist(call: types.CallbackQuery, state: FSMContext):
    user = await user_service.get_object(
        object_id=int(call.data.split(":")[3])
    )
    await user_service.update_object(
        object_id=int(call.data.split(":")[3]), data={"is_banned": True}
    )
    await call.message.edit_text(
        f"<i>{user.get_full_name()} добавлен в ЧС.</i>",
        parse_mode=types.ParseMode.HTML,
    )
    await state.finish()


async def remove_from_blacklist(call: types.CallbackQuery, state: FSMContext):
    user = await user_service.get_object(
        object_id=int(call.data.split(":")[3])
    )
    await user_service.update_object(
        object_id=int(call.data.split(":")[3]), data={"is_banned": False}
    )
    await call.message.edit_text(
        f"<i>{user.get_full_name()} убран из ЧС.</i>",
        parse_mode=types.ParseMode.HTML,
    )
    await state.finish()
