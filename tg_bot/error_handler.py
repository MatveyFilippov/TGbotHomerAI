from . import global_tools
import logging
import traceback
from datetime import datetime
from aiogram.types import Update
import settings


async def error_handler(update: Update, exception: Exception):
    err_time = datetime.now(settings.BOT_TIMEZONE).strftime(settings.DATETIME_FORMAT)
    err_name, def_name = type(exception).__name__, traceback.extract_tb(exception.__traceback__)[-1].name
    error_text = "".join(traceback.format_exception(type(exception), exception, exception.__traceback__))

    logging.error(f"{err_name} in '{def_name}'", exc_info=True)

    error_creator = await get_error_creator(update, err_time)

    await global_tools.send_message_to_developer((
        f"{err_time} ({settings.BOT_TIMEZONE.zone})"
        "\nUnexpected error occurred **{err_name}** in **{def_name}**"
    ))
    await global_tools.send_message_to_developer(error_creator + f"\n\n```log\n{error_text}\n```")


async def get_error_creator(update: Update, err_time: str) -> str:
    try:
        await global_tools.send_message_to_user(user_tg_peer_id=update.message.chat.id, text=(
            f"{err_time} ({settings.BOT_TIMEZONE.zone}) --- **ERROR**"
            "\nOops, something went wrong 🛠️\nReported the bug — please try again soon"
        ))
        if update.message.from_user.username:
            return f"Error from @{update.message.from_user.username}"
        else:
            return f"Error from {update.message.from_user.full_name}"
    except AttributeError:
        return "Error in source code"
