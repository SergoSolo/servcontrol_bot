from aiogram.types import ReplyKeyboardMarkup
from bot.buttons import (BTN_ADD_FILES, BTN_ADMINS, BTN_FILES, BTN_INFO,
                         BTN_TECHNICAL_SUPPORT, BTN_USERS)

start_mune_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(
    BTN_FILES, BTN_TECHNICAL_SUPPORT
)
admin_menu_keyboard = (
    ReplyKeyboardMarkup(resize_keyboard=True)
    .add(BTN_ADD_FILES, BTN_INFO)
    .row(BTN_ADMINS, BTN_USERS)
)
