import aiogram as __aiogram
from .base import DISPATCHER as __DISPATCHER, LOGGER as __LOGGER
from .global_tools import send_message_to_developer as __send_message_to_developer
from .error_handler import error_handler as __error_handler
from .tasks import register_all as __register_all_tasks


async def __on_startup(dispatcher):
    await __send_message_to_developer("The bot was disabled, now it works 🐥")
    print("Bot is alive")


async def __on_shutdown(dispatcher):
    __LOGGER.critical("Bot is shut down")
    await __send_message_to_developer("⚠️*The bot is shut down*⚠️")


def start():
    __DISPATCHER.register_errors_handler(__error_handler)
    __register_all_tasks()
    __aiogram.executor.start_polling(__DISPATCHER, on_startup=__on_startup, on_shutdown=__on_shutdown)
