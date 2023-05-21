from aiogram.dispatcher import Dispatcher

from app.bot.handlers.admin.admin_register import register_admins_handlers
from app.bot.handlers.client.client_register import register_clients_handlers
from app.bot.handlers.pagination_handler import register_pagination_handlers


def main_register_handlers(dp: Dispatcher):
    register_clients_handlers(dp)
    register_admins_handlers(dp)
    register_pagination_handlers(dp)
