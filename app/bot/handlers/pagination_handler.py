from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from app.bot.keyboard import create_paginated_keyboard, navigation
from app.bot.states import AdminMenu
from app.bot.utils import array_spliter, create_message_text


async def pagination_objects(
    call: types.CallbackQuery, state: FSMContext, page: int = 0
):
    object_type = call.data.split(":")[2]
    data = await state.get_data()
    if len(data.get("objects")) == 0:
        await call.message.answer(
            "<i>В данной категории файлов нет.</i>",
            parse_mode=types.ParseMode.HTML,
        )
    else:
        objects_on_page = array_spliter(data.get("objects"), 10)
        text = create_message_text(objects_on_page, object_type, page)
        await state.update_data(
            page=page, objects_on_page=objects_on_page[page]
        )
        keyboard = create_paginated_keyboard(call.data, objects_on_page, page)
        await call.message.edit_text(
            text=text, reply_markup=keyboard, parse_mode=types.ParseMode.HTML
        )
        await state.set_state(AdminMenu.data_pagination.state)


async def next_page(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await pagination_objects(call, state, data.get("page") + 1)


async def previous_page(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await pagination_objects(call, state, data.get("page") - 1)


def register_pagination_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(
        pagination_objects,
        lambda callback_query: True,
        state=[
            AdminMenu.select_user_work_options,
            AdminMenu.select_documents_work_options,
            AdminMenu.selected_categories_options,
        ],
    )
    dp.register_callback_query_handler(
        next_page,
        navigation.filter(action="next"),
        state=AdminMenu.data_pagination,
    )
    dp.register_callback_query_handler(
        previous_page,
        navigation.filter(action="previous"),
        state=AdminMenu.data_pagination,
    )
