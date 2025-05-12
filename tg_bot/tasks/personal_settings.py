from .dialog_states import unset_all_states
from .dialog_states.collection import DialogStates
from ..base import DISPATCHER
from ..global_tools import ContainerCallback, edit_callback
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ContentType
from ai import get_user, get_personal_settings, edit_personal_settings, models as ai_models


class ChangePersonalSettingsCallbacks:
    GO_BACK_TO_PERSONAL_SETTINGS = "personal_settings"
    CHANGE_TEXT_MODEL_LOOK = ContainerCallback("change_text_model:look")
    CHANGE_TEXT_MODEL_SELECT = ContainerCallback("change_text_model:select")
    CHANGE_IMAGE_MODEL = "change_image_model"
    CHANGE_TEXT_MODEL_SYSTEM_PROMPT = "change_text_model_system_prompt"


PERSONAL_SETTINGS_TO_CHANGE = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text="Text model",
            callback_data=ChangePersonalSettingsCallbacks.CHANGE_TEXT_MODEL_LOOK.get(0),
        ),
        InlineKeyboardButton(
            text="Graphic model",
            callback_data="TODO",
        ),
    ],
    [
        InlineKeyboardButton(
            text="Prompt for text model",
            callback_data="TODO",
        ),
    ],
    [
        InlineKeyboardButton(
            text="✖️Close",
            callback_data="CLOSE_MSG",
        ),
    ],
])


class UserTextModelsToChoose:
    __USER_TEXT_MODELS_TO_CHOOSE: dict[int, list[str]] = {}
    __DEFAULT_MODELS = list(ai_models.get_text_models())

    @classmethod
    def set(cls, user_tg_peer_id: int, models: list[str] | None) -> list[str]:
        if models:
            cls.__USER_TEXT_MODELS_TO_CHOOSE[user_tg_peer_id] = models
        elif user_tg_peer_id in cls.__USER_TEXT_MODELS_TO_CHOOSE:
            del cls.__USER_TEXT_MODELS_TO_CHOOSE[user_tg_peer_id]
        return cls.get(user_tg_peer_id)

    @classmethod
    def get(cls, user_tg_peer_id: int) -> list[str]:
        return cls.__USER_TEXT_MODELS_TO_CHOOSE.setdefault(user_tg_peer_id, cls.__DEFAULT_MODELS.copy())


@DISPATCHER.callback_query_handler(text=ChangePersonalSettingsCallbacks.GO_BACK_TO_PERSONAL_SETTINGS, state="*")
@DISPATCHER.message_handler(commands=["personal_settings"], state="*")
async def show_personal_settings(callback_or_message: CallbackQuery | Message):
    UserTextModelsToChoose.set(callback_or_message.from_user.id, None)
    await unset_all_states(callback_or_message.from_user.id)
    user_settings = get_personal_settings(callback_or_message.from_user.id)
    text = f"""{get_user(callback_or_message.from_user.id).user_full_name}, your actual properties:
    \n_Text model_:\n*{user_settings.text_model_name}*
    \n_Prompt for text model_:\n*{user_settings.text_model_system_prompt}*
    \n\nChoose what you want to edit 👇
    """
    if isinstance(callback_or_message, CallbackQuery):
        await edit_callback(callback=callback_or_message, text=text, kb=PERSONAL_SETTINGS_TO_CHANGE)
    elif isinstance(callback_or_message, Message):
        await callback_or_message.reply(text=text, parse_mode="Markdown", reply_markup=PERSONAL_SETTINGS_TO_CHANGE)


def get_text_models_kb(page: int, models: list[str]) -> InlineKeyboardMarkup:  # TODO: requires caching
    MODELS_PER_LINE = 3
    LINES_QTY = 4

    total_models = len(models)
    models_per_page = MODELS_PER_LINE * LINES_QTY
    total_pages = (total_models + models_per_page - 1) // models_per_page

    # page = max(0, min(page, total_pages - 1))
    page %= total_pages

    start_idx = page * models_per_page
    end_idx = min(start_idx + models_per_page, total_models)

    keyboard = [[
        InlineKeyboardButton(text=model, callback_data=ChangePersonalSettingsCallbacks.CHANGE_TEXT_MODEL_SELECT.get(model))
        for model in models[i:i + MODELS_PER_LINE]
    ] for i in range(start_idx, end_idx, MODELS_PER_LINE)]

    keyboard.insert(0, [
        InlineKeyboardButton(text="🔙Back", callback_data=ChangePersonalSettingsCallbacks.GO_BACK_TO_PERSONAL_SETTINGS)
    ])
    keyboard.append([
        InlineKeyboardButton(text="⬅️", callback_data=ChangePersonalSettingsCallbacks.CHANGE_TEXT_MODEL_LOOK.get(page-1)),
        InlineKeyboardButton(text="➡️", callback_data=ChangePersonalSettingsCallbacks.CHANGE_TEXT_MODEL_LOOK.get(page+1)),
    ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


@DISPATCHER.callback_query_handler(ChangePersonalSettingsCallbacks.CHANGE_TEXT_MODEL_LOOK.callback_filter, state="*")
@DISPATCHER.message_handler(content_types=ContentType.ANY, state=DialogStates.choosing_text_model)
async def change_text_model_look(callback_or_message: CallbackQuery | Message):
    text = "*Choose a new text model* from the available options\n\n🔎 Or enter a name to search:"
    await DialogStates.choosing_text_model.set()
    if isinstance(callback_or_message, CallbackQuery):
        page = ChangePersonalSettingsCallbacks.CHANGE_TEXT_MODEL_LOOK.parse(callback_or_message.data, required_type=int)
        if page is None:
            page = 0
        await edit_callback(
            callback=callback_or_message, text=text,
            kb=get_text_models_kb(page, UserTextModelsToChoose.get(callback_or_message.from_user.id))
        )
    elif isinstance(callback_or_message, Message):
        request = callback_or_message.text or callback_or_message.caption
        if not request:
            await callback_or_message.reply(
                text="🤷 Sorry, but I can't find a model if the query does *not* contain *text* (model name)",
                parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
                    InlineKeyboardButton(text="✅OK", callback_data="CLOSE_MSG")
                ]])
            )
            return
        await callback_or_message.reply(text=text, parse_mode="Markdown", reply_markup=get_text_models_kb(
            0, UserTextModelsToChoose.set(callback_or_message.from_user.id, ai_models.find_closest_text_models(request)))
        )


@DISPATCHER.callback_query_handler(ChangePersonalSettingsCallbacks.CHANGE_TEXT_MODEL_SELECT.callback_filter, state="*")
async def change_text_model_select(callback: CallbackQuery):
    model = ChangePersonalSettingsCallbacks.CHANGE_TEXT_MODEL_SELECT.parse(callback.data)
    try:
        if not model:
            raise ValueError
        edit_personal_settings(user_id=callback.from_user.id, text_model_name=model)
        await callback.answer("🤓 New text model successfully set!", show_alert=True)
        await show_personal_settings(callback)
    except ValueError:
        await callback.answer("💆 Failed to set the selected model, please try again", show_alert=True)
        await change_text_model_look(callback)
