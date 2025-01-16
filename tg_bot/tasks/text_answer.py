from ..base import DISPATCHER
import ai
from aiogram.types import Message, ContentType
from aiogram import exceptions


@DISPATCHER.message_handler(content_types=ContentType.ANY, state="*")
async def handle_message(message: Message):
    for _ in range(2):
        response = await ai.process_text_request(message)
        try:
            await message.reply(response, parse_mode="Markdown")
            return
        except exceptions.CantParseEntities:
            ai.delete_dialog_step(message.message_id)
    await message.reply("🌋Извините, произошла ошибка, попробуйте сделать новый запрос", parse_mode="Markdown")
