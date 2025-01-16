from typing import Type
from . import Session, Dialog


def get_dialog(user_id: int) -> list[Type[Dialog]]:
    with Session() as session:
        return session.query(Dialog).filter_by(
            dialog_owner_user_id=user_id
        ).all()


def get_dialog_step(request_id: int) -> Type[Dialog]:
    with Session() as session:
        step = session.get(Dialog, request_id)
        if step:
            return step
    raise KeyError(f"No dialog step with request ID: '{request_id}' id database")


def delete_dialog_step(request_id: int):
    with Session() as session:
        step = session.get(Dialog, request_id)
        if step:
            session.delete(step)
            session.commit()


def delete_all_dialog(user_id: int):
    with Session() as session:
        dialog = session.query(Dialog).filter_by(
            dialog_owner_user_id=user_id
        ).all()
        for step in dialog:
            session.delete(step)
        if dialog:
            session.commit()


def append_step_in_dialog(user_id: int, request_id: int, request: str, response: str):
    with Session() as session:
        session.add(Dialog(
            request_id=request_id,
            dialog_owner_user_id=user_id,
            request=request,
            response=response,
        ))
        session.commit()
