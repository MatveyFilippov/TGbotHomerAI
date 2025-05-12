from . import Session, PersonalSettings
from .. import models


def __get_or_create_personal_settings(session: Session, user_id: int) -> PersonalSettings:
    personal_settings = session.get(PersonalSettings, user_id)
    if not personal_settings:
        session.add(PersonalSettings(user_id=user_id))
        session.commit()
        personal_settings = session.get(PersonalSettings, user_id)
    return personal_settings


def get_personal_settings(user_id: int) -> PersonalSettings:
    with Session() as session:
        return __get_or_create_personal_settings(session, user_id)


def edit_personal_settings(user_id: int, text_model_system_prompt: str | None = None, text_model_name: str | None = None):
    with Session() as session:
        personal_settings = __get_or_create_personal_settings(session, user_id)
        if text_model_system_prompt and personal_settings.text_model_system_prompt != text_model_system_prompt:
            personal_settings.text_model_system_prompt = text_model_system_prompt
        if text_model_name and personal_settings.text_model_name != text_model_name:
            if text_model_name not in models.get_text_models():
                raise ValueError("Unknown text model name: " + text_model_name)
            personal_settings.text_model_name = text_model_name
        session.commit()
