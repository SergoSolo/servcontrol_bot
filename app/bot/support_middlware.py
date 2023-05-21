from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from app.bot.handlers.client.support import Support
from app.core.config import dp


class SupportMiddleware(BaseMiddleware):
    async def on_pre_process_message(self, message: types.Message, data: dict):
        state = dp.current_state(
            chat=message.from_user.id, user=message.from_user.id
        )
        if str(await state.get_state()) == str(Support.in_support.state):
            data = await state.get_data()
            second_id = data.get("second_id")
            await message.copy_to(second_id)
            raise CancelHandler()
