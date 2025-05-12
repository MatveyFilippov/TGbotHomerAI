from ..base import DISPATCHER
from aiogram.types import Message
import ai


@DISPATCHER.message_handler(commands=["reset"], state="*")
async def reset_dialog_history(message: Message):
    ai.delete_all_dialog(message.from_user.id)
    await message.reply("The bot forgot everything you talked about 🧹")
