from ...base import DISPATCHER
from .collection import *
from aiogram.types import Message


@DISPATCHER.message_handler(commands=["web_search"])
async def set_web_search_state(message: Message):
    await FlagsToTextCreating.web_search.set()
    await message.reply(
        text="➡️ Your next message will be loaded into the model with _WebSearch_ flag",
        parse_mode="Markdown"
    )


async def unset_all_states(user_tg_peer_id: int):
    await DISPATCHER.current_state(chat=user_tg_peer_id, user=user_tg_peer_id).set_state(None)
