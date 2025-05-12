from .dialog_states.collection import FlagsToTextCreating
from ..base import DISPATCHER
from ..loading_message import LoadingMessage
from aiogram import exceptions as aiogram_exceptions
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ContentType
import ai


@DISPATCHER.message_handler(content_types=ContentType.ANY, state="*")
async def handle_message(message: Message, state: FSMContext):
    request_text = message.text
    if not request_text:  # TODO: process also for photo&document
        await message.reply("💔 Sorry, currently *only text queries are supported*", parse_mode="Markdown")
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
        except (aiogram_exceptions.CantParseEntities, aiogram_exceptions.MessageIsTooLong):
            ai.delete_dialog_step(message.message_id)

    await loading.delete()
    await message.reply("🌋 Sorry, an error occurred, please try making a new request", parse_mode="Markdown")
