from typing import Type
from . import Session, PersonalSettings


def get_personal_settings(user_id: int) -> Type[PersonalSettings]:
    with Session() as session:
        personal_settings = session.get(PersonalSettings, user_id)
        if not personal_settings:
            session.add(PersonalSettings(user_id=user_id))
            session.commit()
            personal_settings = session.get(PersonalSettings, user_id)
    return personal_settings
