from . import base
import settings
from typing import Callable
from functools import lru_cache
from aiogram.utils import exceptions as aiogram_exceptions
from aiogram.dispatcher.filters import Filter
from aiogram.types import InlineKeyboardMarkup, CallbackQuery, Message


class CallbackChecker(Filter):
    def __init__(self, checker: Callable[[CallbackQuery], bool]):
        self.checker = checker

    async def check(self, callback: CallbackQuery) -> bool:
        return self.checker(callback)


class ContainerCallback:
    def __init__(self, callback_startswith: str):
        self.__callback_startswith = callback_startswith

    @lru_cache
    def get(self, appender) -> str:
        return self.__callback_startswith + ":" + str(appender)

    @lru_cache
    def parse(self, callback: str, required_type=str):
        try:
            appender = callback.removeprefix(f"{self.__callback_startswith}:")
            if not appender:
                raise ValueError
            return required_type(appender)
        except ValueError:
            return None

    @property
    def callback_filter(self) -> Filter:
        return CallbackChecker(lambda c: c.data.startswith(self.__callback_startswith))


async def send_message_to_developer(text: str, kb: InlineKeyboardMarkup | None = None):
    try:
        await base.BOT.send_message(chat_id=settings.BOT_DEVELOPER_TG_ID, parse_mode="Markdown", text=text, reply_markup=kb)
    except (aiogram_exceptions.ChatNotFound, aiogram_exceptions.BotBlocked):
        base.LOGGER.warning("Bot hasn't (or blocked by) 'BOT_DEVELOPER_TG_ID'!")


async def send_message_to_user(user_tg_peer_id: int, text: str, kb: InlineKeyboardMarkup | None = None) -> Message:
    try:
        return await base.BOT.send_message(
            chat_id=user_tg_peer_id, parse_mode="Markdown", text=text, reply_markup=kb,
        )
    except (aiogram_exceptions.ChatNotFound, aiogram_exceptions.BotBlocked):
        pass


async def delete_message(message: Message):
    try:
        await message.delete()
    except (aiogram_exceptions.MessageToDeleteNotFound, aiogram_exceptions.MessageCantBeDeleted):
        pass


async def edit_callback(callback: CallbackQuery, text: str, kb: InlineKeyboardMarkup | None = None):
    try:
        if callback.message.text:
            await callback.message.edit_text(text=text, parse_mode="Markdown", reply_markup=kb)
        else:
            await delete_message(callback.message)
            raise aiogram_exceptions.MessageToEditNotFound(message="message doesn't contain text")
    except aiogram_exceptions.MessageNotModified:
        await callback.answer("Callback try to edit msg, but nothing was modified")
    except aiogram_exceptions.MessageToEditNotFound:
        await callback.message.answer(text=text, parse_mode="Markdown", reply_markup=kb, disable_notification=True)
