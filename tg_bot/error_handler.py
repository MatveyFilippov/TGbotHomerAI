import settings
from aiogram.types import Update
import traceback
from . import base


async def error_handler(update: Update, exception: Exception):
    err_time = settings.datetime_now().strftime(settings.DATETIME_FORMAT)
    err_name, def_name = type(exception).__name__, traceback.extract_tb(exception.__traceback__)[-1].name
    error_text = "".join(traceback.format_exception(type(exception), exception, exception.__traceback__))

    base.LOGGER.error(f"{err_name} in '{def_name}'", exc_info=True)

    error_creator = await get_error_creator(update, err_time)

    await base.send_message_to_developer(
        f"{err_time}\nПроизошла ошибка *{err_name}* в функции *{def_name}*"
    )
    await base.send_message_to_developer(error_creator + f"\n\n```{error_text}```")


async def get_error_creator(update: Update, err_time: str) -> str:
    creator = "Ошибка в самом коде"
    try:
        await base.send_message_to_user(
            user_tg_peer_id=update.message.chat.id,
            text=f"{err_time} --- *ERROR*\nПередал информацию об ошибке разработчику, попробуйте позже",
        )
        creator = f"Ошибка от @{update.message.from_user.username}"
    except AttributeError:
        pass
    return creator
