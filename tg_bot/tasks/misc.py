from ..base import DISPATCHER
from ..global_tools import delete_message
from ai import get_user
from aiogram.types import CallbackQuery, Message


HELP_ANSWER_TEXT = """Welcome to the bot, {full_name}!

This bot is designed for *free access* to various neural models, including:
- Document processing
- Image generation
- Text response generation
- And much more

*Text Generation*
Send messages and receive responses.
Each conversation step is saved in the model's memory, allowing for continuous dialogue.
If you reply to the model's message using `reply`, the model will receive the narrowed conversation context up to that step.

*Analysis of Attached Documents and Photos*
Works on the principle of regular _text generation_.
Simply attach your file or photo and add a task description.

*Image Generation*
Use the `/image` command to start a separate dialogue thread specifically for image creation.

*Web Search*
The `/web_search` command will add a network search flag to your next text query.
The model will also consider your dialogue context, just like in regular _text generation_.

*Other Commands*
- `/reset` - clear the dialogue from the model's memory
- `/personal_settings` - customize the bot for your needs

Currently, the bot is under development, and many features are unavailable..."""


@DISPATCHER.message_handler(commands=["start", "help"], state="*")
async def handle_start_help_command(message: Message):
    await message.reply(
        text=HELP_ANSWER_TEXT.format(full_name=get_user(message.from_user.id).user_full_name), parse_mode="Markdown"
    )


@DISPATCHER.callback_query_handler(text="CLOSE_MSG", state="*")
async def handle_close_message_request(callback: CallbackQuery):
    await callback.answer("Message is closed")
    await delete_message(callback.message)
    await delete_message(callback.message.reply_to_message)


@DISPATCHER.callback_query_handler(text="TODO", state="*")
async def handle_todo_callback(callback: CallbackQuery):
    await callback.answer("👷 This block is under development...", show_alert=True)


@DISPATCHER.callback_query_handler(state="*")
async def handle_unknown_callback(callback: CallbackQuery):
    await callback.answer(f"Unknown callback: '{callback.data}'", show_alert=True)


@DISPATCHER.edited_message_handler(state="*")
async def handle_edited_message(message: Message):
    await message.reply("""🚫You made changes, but unfortunately, our bot *DOES NOT SUPPORT* this feature(
    \nThe model *WILL NOT SEE* your changes. Please send another message to make a request""", parse_mode="Markdown")
