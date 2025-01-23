from ...base import DISPATCHER
from .collection import DialogStates
from .dialog_allowance import DialogNotAvailable
from aiogram.types import Message
from aiogram.dispatcher import FSMContext


@DISPATCHER.message_handler(DialogNotAvailable())
async def send_answer_if_dialog_not_available(message: Message):
    await message.answer(
        text="Извините, вы *не можете* пользоваться этим ботом, обратитесь к человеку, который дал вам ссылку 🤐",
        parse_mode="Markdown",
    )


@DISPATCHER.message_handler(state=DialogStates.answer_is_creating)
async def set_web_search_state(message: Message, state: FSMContext):
    await message.reply(
        text="⏰В настоящий момент **обрабатывается** ваше **прошлое сообщение**, пожалуйста, дождитесь ответа и задайте новый запрос...",
        parse_mode="Markdown"
    )
