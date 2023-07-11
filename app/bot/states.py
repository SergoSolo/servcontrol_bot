from aiogram.dispatcher.filters.state import State, StatesGroup


class AdminMenu(StatesGroup):
    """Состояния администратора."""
    select_main_options = State()
    selected_users_options = State()
    select_user_work_options = State()
    selected_documents_options = State()
    select_documents_work_options = State()
    waiting_document_to_add = State()
    waiting_document_to_update = State()
    selected_categories_options = State()
    select_categories_work_options = State()
    waiting_category_to_update = State()
    data_pagination = State()


class ClientMenu(StatesGroup):
    """Состояния пользователя."""
    select_main_options = State()
    select_documents = State()
    select = State()
    sel = State()
    user_registeration = State()
    input_first_name = State()
    input_last_name = State()
    input_town = State()
    reconciliation = State()
    select_support = State()
    wait_for_support = State()
    in_support = State()
    get_files = State()


class Support(StatesGroup):
    """Состояния тех.поддержки."""
    support_command = State()
    wait_for_support = State()
    in_support = State()
    wait_in_support = State()
