from typing import Type
from . import Session, Dialog


def get_dialog(user_tg_peer_id: int) -> list[Type[Dialog]]:
    with Session() as session:
        return session.query(Dialog).filter_by(
            dialog_owner_tg_peer_id=user_tg_peer_id
        ).all()


def get_dialog_step(message_id: int) -> Type[Dialog]:
    with Session() as session:
        step = session.query(Dialog).get(message_id)
        if step:
            return step
    raise KeyError(f"No dialog step by message_id: '{message_id}' id database")


def delete_dialog_step(message_id: int):
    with Session() as session:
        step = session.query(Dialog).get(message_id)
        if step:
            session.delete(step)
            session.commit()


def delete_all_dialog(user_tg_peer_id: int):
    with Session() as session:
        dialog = session.query(Dialog).filter_by(
            dialog_owner_tg_peer_id=user_tg_peer_id
        ).all()
        for step in dialog:
            session.delete(step)
        if dialog:
            session.commit()


def append_step_in_dialog(user_tg_peer_id: int, message_id: int, request: str, response: str):
    with Session() as session:
        session.add(Dialog(
            message_id=message_id,
            dialog_owner_tg_peer_id=user_tg_peer_id,
            request=request,
            response=response,
        ))
        session.commit()
