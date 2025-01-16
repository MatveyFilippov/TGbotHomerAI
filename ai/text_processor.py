from .__database import dialog as db_dialog
from .__database import personal_settings as db_personal_settings
from g4f.client import AsyncClient
from .misc_helpers import LoadingMessage
from aiogram import types


def get_messages_for_model_from_db(requester_tg_peer_id: int) -> list[dict[str, str]]:
    result = [{
        "role": "system",
        "content": db_personal_settings.get_personal_settings(requester_tg_peer_id).text_model_system_prompt
    }]
    for step in db_dialog.get_dialog(requester_tg_peer_id):
        result.append({
            "role": "user", "content": step.request
        })
        result.append({
            "role": "assistant", "content": step.response
        })
    return result


def get_messages_for_model_from_message(message: types.Message) -> list[dict[str, str]]:
    return [
        {
            "role": "system",
            "content": db_personal_settings.get_personal_settings(message.from_user.id).text_model_system_prompt
        },
        {
            "role": "user", "content": message.reply_to_message.reply_to_message.text  # TODO: AttributeError: 'NoneType' object has no attribute 'text'
        },
        {
            "role": "assistant", "content": message.reply_to_message.text
        },
    ]


async def get_response_from_text_model(messages: list[dict[str, str]], model: str) -> str:
    client = AsyncClient()
    response = await client.chat.completions.create(model=model, messages=messages, web_search=False)
    return response.choices[0].message.content


async def process_request(message: types.Message, send_loading=True) -> str:
    loading = None
    if send_loading:
        loading = LoadingMessage(message)
        await loading.send()

    if message.reply_to_message:
        messages = get_messages_for_model_from_message(message)
    else:
        messages = get_messages_for_model_from_db(message.from_user.id)
    messages.append({"role": "user", "content": message.text})

    response_text = await get_response_from_text_model(
        messages=messages, model=db_personal_settings.get_personal_settings(message.from_user.id).text_model_name
    )

    db_dialog.append_step_in_dialog(
        user_tg_peer_id=message.from_user.id, message_id=message.message_id,
        request=message.text, response=response_text,
    )

    if loading:
        await loading.delete()
    return response_text
