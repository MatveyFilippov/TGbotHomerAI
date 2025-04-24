from datetime import timedelta
from aiogram.types import Message
from aiogram.dispatcher.filters import Filter
import ai
from functools import lru_cache
from ...base import DISPATCHER
from .collection import DIALOG_NOT_AVAILABLE_STATE
import settings


class DialogAvailabilityCache:
    @staticmethod
    def is_dialog_available_without_cache(tg_peer_id: int) -> bool:
        if not ai.is_user_in_database(tg_peer_id):
            return False
        return ai.get_available_days_to_use(tg_peer_id) > 0

    __CACHE = lru_cache()(is_dialog_available_without_cache)
    __CACHE_CLEAR_PERIOD = timedelta(days=1)
    __last_reset = settings.datetime_now()

    @classmethod
    def clear_cache(cls):
        cls.__CACHE.cache_clear()
        cls.__last_reset = settings.datetime_now()

    @classmethod
    def is_dialog_available(cls, tg_peer_id: int) -> bool:
        current_time = settings.datetime_now()
        if (current_time - cls.__last_reset) > cls.__CACHE_CLEAR_PERIOD:
            cls.__CACHE.cache_clear()
            cls.__last_reset = current_time
        return cls.__CACHE(tg_peer_id)


class DialogNotAvailable(Filter):
    async def check(self, message: Message) -> bool:
        if DialogAvailabilityCache.is_dialog_available(tg_peer_id=message.from_user.id):
            await DISPATCHER.current_state().set_state()
            return False
        else:
            await DIALOG_NOT_AVAILABLE_STATE.set()
            return True
