from aiogram import types
from aiogram.dispatcher import FSMContext

from app.bot.keyboard import create_category_keyboard, create_options_keyboard
from app.bot.states import AdminMenu
from app.core.config import bot
from app.core.db.repository import category_service, document_service


async def select_documents_option(
    call: types.CallbackQuery, state: FSMContext
):
    categories = await category_service.get_all_objects()
    await call.message.edit_text(
        "<i>Выберите категорию файлов с которой хотите работать.</i>",
        reply_markup=await create_category_keyboard(categories),
        parse_mode=types.ParseMode.HTML,
    )
    await state.set_state(AdminMenu.selected_documents_options.state)


async def select_work_options(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(category_id=int(call.data.split(":")[3]))
    documents = await document_service.get_all_documents_by_type(
        type_id=int(call.data.split(":")[3])
    )
    await state.update_data(objects=documents)
    await call.message.edit_text(
        (
            "<i>Вы можете добавить, обновить или удалить "
            "файл, нажав на кнопки ниже.</i>"
        ),
        reply_markup=create_options_keyboard(
            type_object=call.data.split(":")[2]
        ),
        parse_mode=types.ParseMode.HTML,
    )
    await state.set_state(AdminMenu.select_documents_work_options.state)


async def selected_add_document(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text(
        "<i>Прикрепите файл, который хотите добавить.</i>",
        parse_mode=types.ParseMode.HTML,
    )
    await state.set_state(AdminMenu.waiting_document_to_add.state)


async def delete_document(call: types.CallbackQuery, state: FSMContext):
    await document_service.delete_object(
        object_id=int(call.data.split(":")[3])
    )
    await call.message.edit_text(
        "<i>Файл удален.</i>", parse_mode=types.ParseMode.HTML
    )
    await state.finish()


async def document_selected_to_update(
    call: types.CallbackQuery, state: FSMContext
):
    await state.update_data(db_document_id=int(call.data.split(":")[3]))
    await call.message.edit_text(
        "<i>Прикрепите файл, который хотите добавить.</i>",
        parse_mode=types.ParseMode.HTML,
    )
    await state.set_state(AdminMenu.waiting_document_to_update.state)


async def update_document(message: types.Message, state: FSMContext):
    await state.update_data(
        name=message.document.file_name, document_id=message.document.file_id
    )
    document_data = await state.get_data()
    await document_service.update_object(
        object_id=document_data.get("db_document_id"), data=document_data
    )
    await bot.send_message(
        message.from_user.id,
        (f"<i>Файл {message.document.file_name.split('.')[0]} обновлен.</i>"),
        parse_mode=types.ParseMode.HTML,
    )
    await state.finish()


async def add_document(message: types.Message, state: FSMContext):
    data = await state.get_data()
    documents_data = {
        "name": message.document.file_name.split(".")[0],
        "document_id": message.document.file_id,
        "category_id": data.get("category_id"),
    }
    await document_service.create_object(documents_data)
    await bot.send_message(
        message.from_user.id,
        (f"<i>Файл {message.document.file_name.split('.')[0]} добавлен.</i>"),
        parse_mode=types.ParseMode.HTML,
    )
