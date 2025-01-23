from ...base import DISPATCHER
from .collection import DialogStates
from aiogram.types import Message
from aiogram.dispatcher import FSMContext


@DISPATCHER.message_handler(state=DialogStates.answer_is_creating)
async def set_web_search_state(message: Message, state: FSMContext):
    await message.reply(
        text="⏰В настоящий момент **обрабатывается** ваше **прошлое сообщение**, пожалуйста, дождитесь ответа и задайте новый запрос...",
        parse_mode="Markdown"
    )
