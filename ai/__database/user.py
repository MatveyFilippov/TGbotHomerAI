from typing import Type
from . import Session, User


def register_new_user(user_tg_peer_id: int, user_full_name: str, note: str | None = ""):
    with Session() as session:
        session.add(User(
            tg_peer_id=user_tg_peer_id,
            user_full_name=user_full_name,
            note=note,
        ))
        session.commit()


def is_user_in_database(user_tg_peer_id: int) -> bool:
    with Session() as session:
        return bool(session.query(User).get(user_tg_peer_id))


def get_users_qty() -> int:
    with Session() as session:
        return len(session.query(User).all())


def iter_all_users() -> iter(list[Type[User]]):
    with Session() as session:
        users = session.query(User).all()
    for user_obj in users:
        yield user_obj
