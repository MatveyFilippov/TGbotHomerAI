from typing import Type
from . import Session, PersonalSettings


def get_personal_settings(user_tg_peer_id: int) -> Type[PersonalSettings]:
    with Session() as session:
        personal_settings = session.query(PersonalSettings).get(user_tg_peer_id)
        if not personal_settings:
            personal_settings = PersonalSettings(tg_peer_id=user_tg_peer_id)
            session.add(personal_settings)
            session.commit()
        return personal_settings
