import sqlalchemy
from sqlalchemy import create_engine, Column, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
import settings


engine = create_engine(settings.LINK_TO_DATABASE, echo=False)
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    user_id = Column(sqlalchemy.BIGINT, primary_key=True)
    registered_at = Column(sqlalchemy.DateTime, nullable=False, default=settings.datetime_now)

    user_full_name = Column(sqlalchemy.Text, nullable=False)
    note = Column(sqlalchemy.Text, nullable=True)

    last_availability_update = Column(sqlalchemy.DateTime, nullable=False, default=settings.datetime_now)
    days_period_for_using = Column(sqlalchemy.Integer, nullable=True)


class PersonalSettings(Base):
    __tablename__ = 'personal_settings'

    user_id = Column(sqlalchemy.BIGINT, ForeignKey('users.user_id'), primary_key=True)

    text_model_system_prompt = Column(
        sqlalchemy.Text, nullable=False,
        default="Вы высококвалифицированный и надежный помощник внутри TelegramBot. Во время своих ответов используйте разметку Telegram Markdow. При предоставлении кода убедитесь, что он внесён в специальные ковычки. Если в тексте вы хотите создать заголовок, то используй символ '▎' вместо '#' или других стандартных методов разметки, но только где это необходимо для организации текста. Не забывайте создавать абзацы и разделять текст на строчки для поднятия читаемости ответов."
    )
    text_model_name = Column(sqlalchemy.Text, nullable=False, default="gpt-4o")


class Dialog(Base):
    __tablename__ = 'dialogs'

    request_id = Column(sqlalchemy.BIGINT, primary_key=True)
    dialog_owner_user_id = Column(sqlalchemy.BIGINT, ForeignKey('users.user_id'), nullable=False)
    response_time = Column(sqlalchemy.DateTime, nullable=False, default=settings.datetime_now)

    request = Column(sqlalchemy.Text, nullable=False)
    response = Column(sqlalchemy.Text, nullable=False)


Base.metadata.create_all(engine)
Session = scoped_session(sessionmaker(bind=engine))
