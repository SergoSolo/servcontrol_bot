import random

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from app.core.config import dp
from app.core.constants import UserRoleConstant
from app.core.db.repository import category_service, user_service

users_callback = CallbackData("users", "role_name", "role_id", "is_banned")
documents_callback = CallbackData(
    "documents", "action", "type_object", "document_id"
)
navigation = CallbackData("navigation", "method", "type_object", "action")
methods = CallbackData("methods", "action", "type_object")
support_callback = CallbackData("support", "messages", "user_id", "as_user")
cancel_support_callback = CallbackData("cancel_support", "user_id")


def create_acception_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton(text="Да", callback_data="yes"),
        InlineKeyboardButton(text="Нет", callback_data="no"),
    )
    return keyboard


def create_admin_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton(text="Файлы", callback_data="files"),
        InlineKeyboardButton(text="Пользователи", callback_data="users"),
        InlineKeyboardButton(
            text="Категории файлов", callback_data="categories"
        ),
    ).row(InlineKeyboardButton(text="❌", callback_data="cancel"))
    return keyboard


def create_users_keyboard(user_role: int):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton(
            "Активные пользователи",
            callback_data=users_callback.new(
                role_name="user", role_id=3, is_banned=0
            ),
        ),
        InlineKeyboardButton(
            "Пользователи в ЧС",
            callback_data=users_callback.new(
                role_name="user", role_id=3, is_banned=1
            ),
        ),
    )
    if user_role == UserRoleConstant.ADMIN.value:
        keyboard.add(
            InlineKeyboardButton(
                "Модераторы",
                callback_data=users_callback.new(
                    role_name="moderator", role_id=2, is_banned=0
                ),
            )
        )
    keyboard.row(InlineKeyboardButton("❌", callback_data="cancel"))
    return keyboard


def create_registration_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("Регистрация", callback_data="registration")
    ).row(InlineKeyboardButton("❌", callback_data="cancel"))
    return keyboard


async def create_category_keyboard():
    document_types = await category_service.get_all_objects()
    keqyboard = InlineKeyboardMarkup(row_width=2)
    buttons = []
    for category in document_types:
        buttons.append(
            InlineKeyboardButton(
                text=category.name,
                callback_data=documents_callback.new(
                    action="get", type_object="files", document_id=category.id
                ),
            )
        )
    keqyboard.add(*buttons).row(
        InlineKeyboardButton("❌", callback_data="cancel")
    )
    return keqyboard


def create_users_option_keyboard(callback_data: str, current_user_role: int):
    role = callback_data.split(":")[1]
    is_banned = bool(int(callback_data.split(":")[3]))
    keyboard = InlineKeyboardMarkup(row_width=2)
    if not is_banned:
        if (
            role == "user"
            and current_user_role == UserRoleConstant.ADMIN.value
        ):
            keyboard.add(
                InlineKeyboardButton(
                    "Добавит в модераторы",
                    callback_data=methods.new(
                        action="add_to_moderators", type_object="users"
                    ),
                ),
                InlineKeyboardButton(
                    "Добавить в ЧС",
                    callback_data=methods.new(
                        action="add_to_blacklist", type_object="users"
                    ),
                ),
            )
        elif role == "moderator":
            keyboard.add(
                InlineKeyboardButton(
                    "Убрать из модераторов",
                    callback_data=methods.new(
                        action="remove_from_moderators", type_object="users"
                    ),
                )
            )
    else:
        keyboard.add(
            InlineKeyboardButton(
                "Убрать из ЧС",
                callback_data=methods.new(
                    action="remove_from_blacklist", type_object="users"
                ),
            )
        )
    keyboard.add(
        InlineKeyboardButton(
            "Удалить пользователя",
            callback_data=methods.new(action="delete", type_object="users"),
        )
    ).row(InlineKeyboardButton("❌", callback_data="cancel"))
    return keyboard


def create_paginated_keyboard(
    callback_data: str, documents: list, page: int = 0
):
    keyboard = InlineKeyboardMarkup(row_width=5)
    action = callback_data.split(":")[1]
    type_object = callback_data.split(":")[2]
    buttons = []
    if len(documents) != 0:
        for num, file in enumerate(documents[page]):
            buttons.append(
                InlineKeyboardButton(
                    text=f"{num + 1}",
                    callback_data=documents_callback.new(
                        action=action,
                        type_object=type_object,
                        document_id=file.id,
                    ),
                )
            )
    keyboard.add(*buttons)
    get_all_button = InlineKeyboardButton(
        text="Получить файлы со страницы", callback_data="get_all"
    )
    next_button = InlineKeyboardButton(
        "➡️",
        callback_data=navigation.new(
            action="next", method=action, type_object=type_object
        ),
    )
    prev_button = InlineKeyboardButton(
        "⬅️",
        callback_data=navigation.new(
            action="previous", method=action, type_object=type_object
        ),
    )
    cancel_button = InlineKeyboardButton("❌", callback_data="cancel")
    if action == "get":
        keyboard.row(get_all_button)
    if len(documents) <= 1 and page == 0:
        keyboard.row(cancel_button)
    elif page == 0:
        keyboard.row(cancel_button, next_button)
    elif page == len(documents) - 1:
        keyboard.row(prev_button, cancel_button)
    else:
        keyboard.row(prev_button, cancel_button, next_button)
    return keyboard


def create_options_keyboard(type_object: str):
    file_options_keqyboard = InlineKeyboardMarkup(row_width=2)
    file_options_keqyboard.add(
        InlineKeyboardButton(
            text="Добавить",
            callback_data=methods.new(action="add", type_object=type_object),
        ),
        InlineKeyboardButton(
            text="Обновить",
            callback_data=methods.new(
                action="update", type_object=type_object
            ),
        ),
        InlineKeyboardButton(
            text="Удалить",
            callback_data=methods.new(
                action="delete", type_object=type_object
            ),
        ),
    ).row(InlineKeyboardButton(text="❌", callback_data="cancel"))
    return file_options_keqyboard


async def check_support_available(support_id):
    state = dp.current_state(chat=support_id, user=support_id)
    state_string = str(await state.get_state())
    if state_string == "in_support":
        return
    else:
        return support_id


async def get_support_manager(support_ids):
    random.shuffle(support_ids)
    for support_id in support_ids:
        support_id = await check_support_available(support_id)
        if support_id:
            return support_id
    else:
        return


async def support_keyboard(messages, user_id=None):
    support_ids = await user_service.get_users_telegram_ids_by_role(
        role_id=UserRoleConstant.MODERATOR.value
    )
    if user_id:
        contact_id = int(user_id)
        as_user = "no"
        text = "Ответить пользователю."
    else:
        contact_id = await get_support_manager(support_ids)
        as_user = "yes"
        if messages == "many" and contact_id is None:
            return False
        elif messages == "one" and contact_id is None:
            contact_id = random.choice(support_ids)
        if messages == "one":
            text = "Напишите свой вопрос"
        else:
            text = "Написать оператору"
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(
            text=text,
            callback_data=support_callback.new(
                messages=messages, user_id=contact_id, as_user=as_user
            ),
        )
    )
    if messages == "many":
        keyboard.add(
            InlineKeyboardButton(
                text="Завершить сеанс",
                callback_data=cancel_support_callback.new(
                    user_id=contact_id,
                ),
            )
        )
    return keyboard


def cancel_support(user_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Завершить",
                    callback_data=cancel_support_callback.new(user_id=user_id),
                )
            ]
        ]
    )


def create_help_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton(
            text="Образ Live CD",
            url=(
                "https://sergeistrelec.name/winpe_10_8/"
                "227-winpe-10-8-sergei-strelec-x86x64native-x86-"
                "20230314-русская-версия.html"
            ),
        ),
        InlineKeyboardButton(
            text="Как записать образ",
            url=(
                "https://ichip.ru/sovety/ekspluataciya/"
                "ultraiso-kak-zapisat-obraz-na-fleshku-683112"
            ),
        ),
        InlineKeyboardButton(
            text="Оценка состояния HDD",
            url="https://www.ixbt.com/storage/hdd-smart-testing.shtml",
        ),
    ).row(InlineKeyboardButton(text="❌", callback_data="cancel"))
    return keyboard


def create_cancel_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="❌", callback_data="cancel"))
    return keyboard
