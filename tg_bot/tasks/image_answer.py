from ..base import DISPATCHER
from aiogram.types import Message


@DISPATCHER.message_handler(commands=["image"], state="*")
async def start_creating_image(message: Message):
    await message.reply(text="🧑‍💻Данный блок находится в разработке...")
