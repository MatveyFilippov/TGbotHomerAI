import aiogram
from .base import BOT, DISPATCHER
from .base import on_startup as __on_startup
from .base import on_shutdown as __on_shutdown
from .error_handler import error_handler as __error_handler
from .tasks import register_all as __register_all_tasks


def start():
    DISPATCHER.register_errors_handler(__error_handler)
    __register_all_tasks()
    aiogram.executor.start_polling(DISPATCHER, on_startup=__on_startup, on_shutdown=__on_shutdown)
