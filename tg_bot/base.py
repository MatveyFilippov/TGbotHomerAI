import aiogram
from aiogram.utils import exceptions
from aiogram.types import InlineKeyboardMarkup, Message
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging
import settings


BOT = aiogram.Bot(settings.BOT_API_TOKEN)
DISPATCHER = aiogram.Dispatcher(BOT, storage=MemoryStorage())
LOGGER = logging.getLogger()


async def send_message_to_developer(text: str, kb: InlineKeyboardMarkup | None = None):
    try:
        await BOT.send_message(chat_id=settings.BOT_DEVELOPER_TG_ID, parse_mode="Markdown", text=text, reply_markup=kb)
    except (aiogram.utils.exceptions.ChatNotFound, aiogram.utils.exceptions.BotBlocked):
        LOGGER.warning("Bot hasn't (or blocked by) 'BOT_DEVELOPER_TG_ID'!")


async def send_message_to_user(user_tg_peer_id: int, text: str, kb: InlineKeyboardMarkup | None = None) -> Message:
    try:
        return await BOT.send_message(
            chat_id=user_tg_peer_id, parse_mode="Markdown", text=text, reply_markup=kb,
        )
    except (aiogram.utils.exceptions.ChatNotFound, aiogram.utils.exceptions.BotBlocked):
        pass


async def on_startup(dispatcher):
    await send_message_to_developer("Бот был отключен -> работает 🐥")
    print("Bot is alive")


async def on_shutdown(dispatcher):
    LOGGER.critical("Bot is shut down")
    await send_message_to_developer("⚠️<b>Бот выключен</b>⚠️")
