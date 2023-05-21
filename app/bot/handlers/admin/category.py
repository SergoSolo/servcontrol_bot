from aiogram import types
from aiogram.dispatcher import FSMContext

from app.bot.keyboard import create_options_keyboard
from app.bot.states import AdminMenu
from app.core.config import bot
from app.core.db.repository import category_service


async def select_categories_option(
    call: types.CallbackQuery, state: FSMContext
):
    await call.message.edit_text(
        (
            "<i>Вы можете добавить, обновить или удалить "
            "категорию, нажав на кнопки ниже.\n\n"
            "<b>При удалении категории будут удалены ВСЕ "
            "файлы, которые находятся в ней❗</b></i>"
        ),
        reply_markup=create_options_keyboard(type_object=call.data),
        parse_mode=types.ParseMode.HTML,
    )
    categories = await category_service.get_all_objects()
    await state.update_data(objects=categories)
    await state.set_state(AdminMenu.selected_categories_options.state)


async def input_category_name(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text(
        "<i>Введте название новой категории</i>",
        parse_mode=types.ParseMode.HTML,
    )
    await state.set_state(AdminMenu.select_categories_work_options.state)


async def add_category(message: types.Message, state: FSMContext):
    await category_service.create_object({"name": message.text})
    await bot.send_message(
        message.from_user.id,
        f"<i>Добавлена категория: {message.text}</i>",
        parse_mode=types.ParseMode.HTML,
    )
    await state.finish()


async def delete_category(call: types.CallbackQuery, state: FSMContext):
    await category_service.delete_object(
        object_id=int(call.data.split(":")[3])
    )
    await call.message.edit_text(
        "<i>Категория удалена и все файлы в ней.</i>",
        parse_mode=types.ParseMode.HTML,
    )


async def category_selected_to_update(
    call: types.CallbackQuery, state: FSMContext
):
    await call.message.delete()
    await state.update_data(category_id=int(call.data.split(":")[3]))
    await call.message.answer(
        "<i>Введите новое название категории</i>",
        parse_mode=types.ParseMode.HTML,
    )
    await state.set_state(AdminMenu.waiting_category_to_update.state)


async def update_category(message: types.Message, state: FSMContext):
    document_data = await state.get_data()
    await category_service.update_object(
        object_id=document_data.get("category_id"), data={"name": message.text}
    )
    await bot.send_message(
        message.from_user.id,
        (f"<i>Категория переименована: {message.text}</i>"),
        parse_mode=types.ParseMode.HTML,
    )
    await state.finish()
