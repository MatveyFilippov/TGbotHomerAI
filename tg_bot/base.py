import aiogram
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging
import settings


BOT = aiogram.Bot(settings.BOT_API_TOKEN)
DISPATCHER = aiogram.Dispatcher(BOT, storage=MemoryStorage())
LOGGER = logging.getLogger()
