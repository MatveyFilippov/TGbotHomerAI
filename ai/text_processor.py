from .__database import dialog as db_dialog
from .__database import personal_settings as db_personal_settings
from g4f.client import AsyncClient


def get_all_dialog(requester_id: int) -> list[dict[str, str]]:
    result = []
    for step in db_dialog.get_dialog(requester_id):
        result.append({
            "role": "user", "content": step.request
        })
        result.append({
            "role": "assistant", "content": step.response
        })
    result.append({
        "role": "system",
        "content": db_personal_settings.get_personal_settings(requester_id).text_model_system_prompt
    })
    return result


def get_short_dialog(requester_id: int, old_request_id: int) -> list[dict[str, str]]:
    old_dialog_step = db_dialog.get_dialog_step(old_request_id)
    return [
        {
            "role": "user", "content": old_dialog_step.request
        },
        {
            "role": "assistant", "content": old_dialog_step.response
        },
        {
            "role": "system",
            "content": db_personal_settings.get_personal_settings(requester_id).text_model_system_prompt
        },
    ]


async def get_response_from_text_model(messages: list[dict[str, str]], model: str, web_search: bool) -> str:
    client = AsyncClient()
    response = await client.chat.completions.create(
        model=model, messages=messages, web_search=web_search, max_tokens=4096,
    )
    return response.choices[0].message.content


async def process_request(request_id: int, request_text: str, requester_id: int,
                          web_search=False, old_request_id_for_short_dialog: int | None = None) -> str:
    messages = get_short_dialog(
        requester_id=requester_id, old_request_id=old_request_id_for_short_dialog,
    ) if old_request_id_for_short_dialog else get_all_dialog(requester_id=requester_id)
    messages.append({"role": "user", "content": request_text})

    response_text = await get_response_from_text_model(
        messages=messages, model=db_personal_settings.get_personal_settings(requester_id).text_model_name,
        web_search=web_search,
    )

    db_dialog.append_step_in_dialog(
        user_id=requester_id, request_id=request_id,
        request=request_text, response=response_text,
    )

    return response_text
