from aiogram import types
from aiogram.dispatcher import Dispatcher

from app.bot.handlers.client.client_menu import (client_input_first_name,
                                                 client_input_last_name,
                                                 client_input_town,
                                                 data_reconciliation,
                                                 main_client_menu,
                                                 restart_user_registration,
                                                 user_registration)
from app.bot.handlers.client.documents import (files_command,
                                               get_all_documents_from_page,
                                               get_certain_files, get_one_file)
from app.bot.handlers.client.info import help_command
from app.bot.handlers.client.support import (answer_support_call, exit_support,
                                             get_support_message,
                                             not_supported, send_to_support,
                                             start_dailog_support, support,
                                             support_call)
from app.bot.keyboard import (cancel_support_callback, documents_callback,
                              support_callback)
from app.bot.states import AdminMenu, ClientMenu, Support


def register_clients_handlers(dp: Dispatcher):
    dp.register_message_handler(not_supported, state=Support.wait_in_support)
    dp.register_message_handler(
        main_client_menu,
        commands=["start"],
        state="*",
    )
    dp.register_message_handler(files_command, commands=["files"], state="*")
    dp.register_message_handler(
        support_call, commands=["support_call"], state="*"
    )
    dp.register_message_handler(support, commands=["support"], state="*")
    dp.register_message_handler(help_command, commands=["info"], state="*")
    dp.register_callback_query_handler(
        client_input_first_name,
        lambda callback_query: callback_query.data == "registration",
        state="*",
    )
    dp.register_message_handler(
        client_input_last_name, state=ClientMenu.input_first_name
    )
    dp.register_message_handler(
        client_input_town, state=ClientMenu.input_last_name
    )
    dp.register_message_handler(
        data_reconciliation, state=ClientMenu.input_town
    )
    dp.register_callback_query_handler(
        user_registration,
        lambda callback_query: callback_query.data == "yes",
        state=ClientMenu.reconciliation,
    )
    dp.register_callback_query_handler(
        restart_user_registration,
        lambda callback_query: callback_query.data == "no",
        state=ClientMenu.reconciliation,
    )
    dp.register_callback_query_handler(
        send_to_support, support_callback.filter(messages="one"), state="*"
    )
    dp.register_message_handler(
        get_support_message,
        state=Support.wait_for_support,
        content_types=types.ContentTypes.ANY,
    )
    dp.register_callback_query_handler(
        start_dailog_support,
        support_callback.filter(messages="many", as_user="yes"),
        state="*",
    )
    dp.register_callback_query_handler(
        answer_support_call,
        support_callback.filter(messages="many", as_user="no"),
    )
    dp.register_callback_query_handler(
        exit_support,
        cancel_support_callback.filter(),
        state=["*", None],
    )
    dp.register_callback_query_handler(
        get_certain_files,
        documents_callback.filter(action="get", type_object="files"),
        state=ClientMenu.select_documents,
    )
    dp.register_callback_query_handler(
        get_one_file,
        documents_callback.filter(action="get", type_object="files"),
        state=AdminMenu.data_pagination,
    )
    dp.register_callback_query_handler(
        get_all_documents_from_page,
        lambda callback_query: callback_query.data == "get_all",
        state=AdminMenu.data_pagination,
    )
