from ..base import DISPATCHER
from ..loading_message import LoadingMessage
import ai
from aiogram.types import Message, ContentType
from aiogram import exceptions
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


# TODO: process also for photo&document
# TODO: process also for replied messages


class TextDialogStates(StatesGroup):
    web_search = State()


@DISPATCHER.message_handler(commands=["web_search"])
async def set_web_search_state(message: Message):
    await TextDialogStates.web_search.set()
    await message.reply(
        text="➡️ Ваше следующее сообщение будет загружено в модель с флагом __Поиск в интернете__",
        parse_mode="Markdown"
    )


@DISPATCHER.message_handler(state=TextDialogStates.web_search)
async def handle_request_and_use_web_search(message: Message, state: FSMContext):
    loading = LoadingMessage(message)
    await loading.send()
    response = await ai.process_text_request(
        request_id=message.message_id, request_text=message.text,
        requester_tg_peer_id=message.from_user.id, web_search=True,
    )
    await loading.delete()
    try:
        await message.reply(response, parse_mode="Markdown")
        await state.set_state()
    except exceptions.CantParseEntities:
        ai.delete_dialog_step(message.message_id)
        await message.reply("🌋Извините, произошла ошибка, попробуйте сделать новый запрос", parse_mode="Markdown")


@DISPATCHER.message_handler(state="*")
async def handle_message(message: Message):
    loading = LoadingMessage(message)
    await loading.send()
    for _ in range(2):
        response = await ai.process_text_request(
            request_id=message.message_id, request_text=message.text, requester_tg_peer_id=message.from_user.id,
        )
        try:
            await message.reply(response, parse_mode="Markdown")
            await loading.delete()
            return
        except exceptions.CantParseEntities:
            ai.delete_dialog_step(message.message_id)
    await loading.delete()
    await message.reply("🌋Извините, произошла ошибка, попробуйте сделать новый запрос", parse_mode="Markdown")
