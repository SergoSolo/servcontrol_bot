from aiogram import types
from aiogram.dispatcher import FSMContext

from app.bot.handlers.pagination_handler import pagination_objects
from app.bot.keyboard import (create_category_keyboard,
                              create_registration_keyboard)
from app.bot.states import ClientMenu
from app.core.config import bot
from app.core.db.repository import document_service, user_service


async def files_command(message: types.Message, state: FSMContext):
    user = await user_service.get_user_by_telegram_id(
        telegram_id=message.from_user.id
    )
    if user:
        if user.is_banned:
            bot.send_message(
                message.from_user.id,
                "<i>Доступ запрещен.</i>",
                parse_mode=types.ParseMode.HTML,
            )
        await bot.send_message(
            message.from_user.id,
            "<i>Выберите какие файлы вам нужны.</i>",
            reply_markup=await create_category_keyboard(),
            parse_mode=types.ParseMode.HTML,
        )
        await state.set_state(ClientMenu.select_documents.state)
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


async def get_certain_files(call: types.CallbackQuery, state: FSMContext):
    documents = await document_service.get_all_documents_by_type(
        type_id=int(call.data.split(":")[3])
    )
    await state.update_data(objects=documents)
    await pagination_objects(call, state)


async def get_one_file(call: types.CallbackQuery, state: FSMContext):
    document = await document_service.get_object(
        object_id=int(call.data.split(":")[3])
    )
    await bot.send_document(call.from_user.id, document=document.document_id)


async def get_all_documents_from_page(
    call: types.CallbackQuery, state: FSMContext
):
    data = await state.get_data()
    document_media = types.MediaGroup()
    for document in data.get("objects_on_page"):
        document_media.attach_document(document=document.document_id)
    await bot.send_media_group(call.from_user.id, media=document_media)
