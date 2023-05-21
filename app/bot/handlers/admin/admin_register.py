from aiogram.dispatcher import Dispatcher

from app.bot.handlers.admin.admin_menu import admin_menu, cancel_option
from app.bot.handlers.admin.category import (
    add_category,
    category_selected_to_update,
    delete_category,
    input_category_name,
    select_categories_option,
    update_category,
)
from app.bot.handlers.admin.documents import (
    add_document,
    delete_document,
    document_selected_to_update,
    select_documents_option,
    select_work_options,
    selected_add_document,
    update_document,
)
from app.bot.handlers.admin.users import (
    add_moderator,
    add_to_blacklist,
    delete_user,
    remove_from_blacklist,
    remove_moderator,
    selected_users_option,
    users_options,
)
from app.bot.keyboard import documents_callback, methods, users_callback
from app.bot.states import AdminMenu


def register_admins_handlers(dp: Dispatcher):
    dp.register_message_handler(admin_menu, commands=["admin"], state="*")
    dp.register_callback_query_handler(
        selected_users_option,
        lambda callback_query: callback_query.data == "users",
        state=AdminMenu.select_main_options,
    )
    dp.register_callback_query_handler(
        cancel_option,
        lambda callback_query: callback_query.data == "cancel",
        state="*",
    )
    dp.register_callback_query_handler(
        users_options,
        users_callback.filter(),
        state=AdminMenu.selected_users_options,
    )
    dp.register_callback_query_handler(
        delete_user,
        documents_callback.filter(action="delete", type_object="users"),
        state=AdminMenu.data_pagination,
    )
    dp.register_callback_query_handler(
        add_moderator,
        documents_callback.filter(
            action="add_to_moderators", type_object="users"
        ),
        state=AdminMenu.data_pagination,
    )
    dp.register_callback_query_handler(
        remove_moderator,
        documents_callback.filter(
            action="remove_from_moderators", type_object="users"
        ),
        state=AdminMenu.data_pagination,
    )
    dp.register_callback_query_handler(
        add_to_blacklist,
        documents_callback.filter(
            action="add_to_blacklist", type_object="users"
        ),
        state=AdminMenu.data_pagination,
    )
    dp.register_callback_query_handler(
        remove_from_blacklist,
        documents_callback.filter(
            action="remove_from_blacklist", type_object="users"
        ),
        state=AdminMenu.data_pagination,
    )
    dp.register_callback_query_handler(
        select_documents_option,
        lambda callback_query: callback_query.data == "files",
        state=AdminMenu.select_main_options,
    )
    dp.register_callback_query_handler(
        select_work_options,
        lambda callback_query: True,
        state=AdminMenu.selected_documents_options,
    )
    dp.register_callback_query_handler(
        selected_add_document,
        methods.filter(action="add", type_object="files"),
        state=AdminMenu.select_documents_work_options,
    )
    dp.register_callback_query_handler(
        document_selected_to_update,
        documents_callback.filter(action="update", type_object="files"),
        state=AdminMenu.data_pagination,
    )
    dp.register_callback_query_handler(
        delete_document,
        documents_callback.filter(action="delete", type_object="files"),
        state=AdminMenu.data_pagination,
    )
    dp.register_message_handler(
        update_document,
        state=AdminMenu.waiting_document_to_update,
        content_types=["document", "text"],
    )
    dp.register_message_handler(
        add_document,
        state=AdminMenu.waiting_document_to_add,
        content_types=["document", "text"],
    )
    dp.register_callback_query_handler(
        select_categories_option,
        lambda callback_query: callback_query.data == "categories",
        state=AdminMenu.select_main_options,
    )
    dp.register_callback_query_handler(
        input_category_name,
        methods.filter(action="add", type_object="categories"),
        state=AdminMenu.selected_categories_options,
    )
    dp.register_message_handler(
        add_category, state=AdminMenu.select_categories_work_options
    )
    dp.register_callback_query_handler(
        delete_category,
        documents_callback.filter(action="delete", type_object="categories"),
        state=AdminMenu.data_pagination,
    )
    dp.register_callback_query_handler(
        category_selected_to_update,
        documents_callback.filter(action="update", type_object="categories"),
        state=AdminMenu.data_pagination,
    )
    dp.register_message_handler(
        update_category, state=AdminMenu.waiting_category_to_update
    )
