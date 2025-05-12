from .base import Session, User
from datetime import datetime
import settings


def __rewrite_if_needed(user: User, user_full_name: str, note: str | None = "",
                        last_availability_update: datetime | None = None,
                        days_period_for_using: int | None = None) -> bool:
    rewritten = False
    if user.user_full_name != user_full_name:
        user.user_full_name = user_full_name
        rewritten = True
    if note is not None and user.note != note:
        user.note = note
        rewritten = True
    if last_availability_update is not None and user.last_availability_update != last_availability_update:
        user.last_availability_update = last_availability_update
        rewritten = True
    if days_period_for_using is not None and user.days_period_for_using != days_period_for_using:
        user.days_period_for_using = days_period_for_using
        rewritten = True
    return rewritten


def write_or_rewrite_new_user_info(user_id: int, user_full_name: str, note: str | None = "",
                                   last_availability_update: datetime | None = None,
                                   days_period_for_using: int | None = None):
    if days_period_for_using is not None and not (0 <= days_period_for_using <= 366):
        raise ValueError(f"Invalid days period: {days_period_for_using}")
    with Session() as session:
        user: User = session.get(User, user_id)
        if not user:
            session.add(User(
                user_id=user_id, user_full_name=user_full_name,
                note=note, days_period_for_using=days_period_for_using,
            ))
            session.commit()
            return
        if __rewrite_if_needed(user, user_full_name, note, last_availability_update, days_period_for_using):
            session.commit()


def is_user_in_database(user_id: int) -> bool:
    with Session() as session:
        return bool(session.get(User, user_id))


def get_user(user_id: int) -> User:
    with Session() as session:
        user = session.get(User, user_id)
        if not user:
            raise KeyError(f"No such user in database with ID: {user_id}")
        return user


def get_available_days_to_use(user_id: int) -> int:
    with Session() as session:
        user: User = session.get(User, user_id)
        if not user:
            raise KeyError(f"No such user in database with ID: {user_id}")
        if not user.days_period_for_using:
            return 1
        days_passed = (datetime.now(settings.BOT_TIMEZONE) - user.last_availability_update).day
        return user.days_period_for_using - days_passed


def get_users_qty() -> int:
    with Session() as session:
        return len(session.query(User).all())


def iter_all_users() -> iter(list[User]):
    with Session() as session:
        users = session.query(User).all()
    for user_obj in users:
        yield user_obj
