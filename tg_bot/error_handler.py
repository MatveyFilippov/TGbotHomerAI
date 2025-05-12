import settings
from aiogram.types import Update
import traceback
from . import global_tools
import logging
from datetime import datetime


async def error_handler(update: Update, exception: Exception):
    err_time = datetime.now(settings.BOT_TIMEZONE).strftime(settings.DATETIME_FORMAT)
    err_name, def_name = type(exception).__name__, traceback.extract_tb(exception.__traceback__)[-1].name
    error_text = "".join(traceback.format_exception(type(exception), exception, exception.__traceback__))

    logging.error(f"{err_name} in '{def_name}'", exc_info=True)

    error_creator = await get_error_creator(update, err_time)

    await global_tools.send_message_to_developer((
        f"{err_time} ({settings.BOT_TIMEZONE.zone})"
        "\nUnexpected error occurred <b>{err_name}</b> in <b>{def_name}</b>"
    ))
    await global_tools.send_message_to_developer(error_creator + f"\n\n```log\n{error_text}\n```")


async def get_error_creator(update: Update, err_time: str) -> str:
    try:
        await global_tools.send_message_to_user(user_tg_peer_id=update.message.chat.id, text=(
            f"{err_time} ({settings.BOT_TIMEZONE.zone}) --- <b>ERROR</b>"
            "\nOops, something went wrong 🛠️\nReported the bug — please try again soon"
        ))
        return "Error from @" + update.message.from_user.username
    except AttributeError:
        return "Error in source code"
