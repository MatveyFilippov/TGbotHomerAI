from .collection import DialogStates
from .dialog_allowance import DialogNotAvailable
from ...base import DISPATCHER
from aiogram.dispatcher import FSMContext
from aiogram.types import Message


@DISPATCHER.message_handler(DialogNotAvailable())
async def send_answer_if_dialog_not_available(message: Message):
    await message.answer(
        text="Sorry, you *cannot* use this bot, please contact the person who gave you the link 🤐",
        parse_mode="Markdown",
    )


@DISPATCHER.message_handler(state=DialogStates.answer_is_creating)
async def set_web_search_state(message: Message, state: FSMContext):
    await message.reply(
        text="⏰ Your **previous message** is currently **being processed**, please wait for the response before making a new request...",
        parse_mode="Markdown"
    )
