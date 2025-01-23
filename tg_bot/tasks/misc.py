from ..base import DISPATCHER
from ai import get_user
from aiogram.types import CallbackQuery, Message


HELP_ANSWER_TEXT = """Добро пожаловать в бота, {full_name}!

Этот бот разработан для *свободного доступа* к различным нейронным моделям, включая:
- Обработку документов
- Создание изображений
- Генерацию текстовых ответов
- И многое другое

*Текстовая генерация*
Отправляйте сообщения и получайте ответы.
Каждый шаг переписки сохраняется в памяти модели, что позволяет вести диалог.
Если вы отвечаете на сообщение модели через `reply`, то модель получит суженную переписку до данного шага.

*Анализ вложенных документов и фотографий*
Работает по принципу обычной _текстовой генерации_.
Просто прикрепляйте ваш файл или фото и добавляйте описание задачи.

*Генерация изображений*
Используйте команду `/image`, чтобы запустить отдельную ветку диалога только для создания фотографии.

*Поиск в интернете*
Команда `/web_search` при следующем текстовом запросе добавит в модель флаг поиска ответов в сети.
Также будет учитываться контекст вашего диалога, как и при обычной _текстовой генерации_.

*Прочее*
- `/reset` - сбросить диалог из памяти модели
- `/personal_settings` - настройка бота под себя

В настоящий момент бот находится в разработке, и множество функций недоступны..."""


@DISPATCHER.message_handler(commands=["start", "help"], state="*")
async def handle_start_help_command(message: Message):
    await message.reply(
        text=HELP_ANSWER_TEXT.format(full_name=get_user(message.from_user.id).user_full_name), parse_mode="Markdown"
    )


@DISPATCHER.callback_query_handler(text="TODO", state="*")
async def handle_todo_callback(callback: CallbackQuery):
    await callback.answer("👷Данный блок находится в разработке...", show_alert=True)


@DISPATCHER.callback_query_handler(state="*")
async def handle_unknown_callback(callback: CallbackQuery):
    await callback.answer(f"Unknown callback: '{callback.data}'", show_alert=True)


@DISPATCHER.edited_message_handler(state="*")
async def handle_edited_message(message: Message):
    await message.reply("""🚫Вы внесли изменения, а, к сожалению, в нашем боте *НЕ ПРЕДУСМОТРЕНА* такая функция(
    \nМодель *НЕ УВИДИТ* ваших изменений. Для запроса отправьте ещё одно сообщение""", parse_mode="Markdown")
