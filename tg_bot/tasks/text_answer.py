from ..base import DISPATCHER
from .dialog_states.collection import FlagsToTextCreating
from ..loading_message import LoadingMessage
import ai
from aiogram import exceptions
from aiogram.types import Message, ContentType
from aiogram.dispatcher import FSMContext


@DISPATCHER.message_handler(content_types=ContentType.ANY, state="*")
async def handle_message(message: Message, state: FSMContext):
    request_text = message.text
    if not request_text:  # TODO: process also for photo&document
        await message.reply("💔 Извините, в данный момент *поддерживаются только текстовые запросы*", parse_mode="Markdown")
        return
    is_web_search_required = await state.get_state() == FlagsToTextCreating.web_search.state

    loading = LoadingMessage(message)
    await loading.send()

    for _ in range(2):
        response = await ai.process_text_request(  # TODO: process also for replied messages by old_request_id_for_short_dialog
            request_id=message.message_id, request_text=request_text, requester_id=message.from_user.id,
            web_search=is_web_search_required
        )
        try:
            await message.reply(response, parse_mode="Markdown")
            await loading.delete()
            return
        except (exceptions.CantParseEntities, exceptions.MessageIsTooLong):
            ai.delete_dialog_step(message.message_id)

    await loading.delete()
    await message.reply("🌋Извините, произошла ошибка, попробуйте сделать новый запрос", parse_mode="Markdown")
