from aiogram.utils import exceptions
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ContentType
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging
import aiogram
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import traceback
from datetime import datetime
import settings


BOT = Bot(settings.BOT_API_TOKEN)
dp = Dispatcher(BOT, storage=MemoryStorage())
LOGGER = logging.getLogger()


async def send_message_to_developer(text: str, kb: InlineKeyboardMarkup | None = None):
    try:
        await BOT.send_message(chat_id=settings.BOT_DEVELOPER_TG_ID, parse_mode="HTML", text=text, reply_markup=kb)
    except (aiogram.utils.exceptions.ChatNotFound, aiogram.utils.exceptions.BotBlocked):
        LOGGER.warning("Bot hasn't (or blocked by) 'BOT_DEVELOPER_TG_ID'!")


async def error_handler(update: types.Update, exception: Exception):
    err_time = datetime.now(settings.BOT_TIMEZONE).strftime(settings.DATETIME_FORMAT)
    error_text = "".join(traceback.format_exception(type(exception), exception, exception.__traceback__))
    tb = traceback.extract_tb(exception.__traceback__)
    LOGGER.error(f"{type(exception).__name__} in '{tb[-1].name}'", exc_info=True)
    try:
        await BOT.send_message(
            chat_id=update.message.chat.id, parse_mode="HTML",
            text=f"{err_time} ({settings.BOT_TIMEZONE}) --- <b>ERROR</b>\nПередал информацию об ошибке разработчику, попробуйте позже"
        )
        text = f"Ошибка от @{update.message.from_user.username}"
    except AttributeError:
        text = "Ошибка в самом коде:"
    except (aiogram.utils.exceptions.ChatNotFound, aiogram.utils.exceptions.BotBlocked):
        text = "Ошибка от пользователя, который перестал пользоваться ботом"

    await send_message_to_developer(
        f"{err_time} ({settings.BOT_TIMEZONE})\nПроизошла ошибка <b>{type(exception).__name__}</b> в функции {tb[-1].name}"
    )
    await send_message_to_developer(text + f"\n\n<code>{error_text}</code>")


@dp.message_handler(commands=["start"], state="*")
async def handle_start_command(message: types.Message):
    await message.reply("Приветствую!")


@dp.message_handler(content_types=ContentType.ANY, state="*")
async def handle_message(message: types.Message):
    await message.reply(
        text="Извините, я не понял ваш запрос 😔", parse_mode="HTML",
    )


@dp.callback_query_handler(state="*")
async def handle_unknown_callback(callback: types.CallbackQuery):
    await callback.answer(f"Unknown callback: '{callback.data}'", show_alert=True)


@dp.edited_message_handler(state="*")
async def handle_edited_message(message: types.Message):
    await message.reply("""🚫Вы внесли изменения, а, к сожалению, в нашем боте <b>НЕ ПРЕДУСМОТРЕНА</b> такая функция(
    \nМодель <b>НЕ УВИДИТ</b> ваших изменений. Для запроса отправьте ещё одно сообщение""", parse_mode="HTML")


async def on_startup(dispatcher):
    await send_message_to_developer("Бот был отключен -> работает 🐥")
    print("Bot is alive")


async def on_shutdown(dispatcher):
    LOGGER.critical("Bot is shut down")
    await send_message_to_developer("⚠️<b>Бот выключен</b>⚠️")


if __name__ == "__main__":
    dp.register_errors_handler(error_handler)
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
