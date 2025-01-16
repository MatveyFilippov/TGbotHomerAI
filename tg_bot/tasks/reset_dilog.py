from ..base import DISPATCHER
import ai
from aiogram.types import Message


@DISPATCHER.message_handler(commands=["reset"], state="*")
async def reset_dialog_history(message: Message):
    ai.delete_all_dialog(message.from_user.id)
    await message.reply("Бот забыл всё о чём вы говорили 🧹")
