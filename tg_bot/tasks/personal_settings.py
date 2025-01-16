from ..base import DISPATCHER
from aiogram.types import Message


@DISPATCHER.message_handler(commands=["personal_settings"], state="*")
async def change_personal_settings(message: Message):
    await message.reply(text="🧑‍💻Данный блок находится в разработке...")
