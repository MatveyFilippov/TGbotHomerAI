import sqlalchemy
from sqlalchemy import create_engine, Column, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
import settings


engine = create_engine(settings.LINK_TO_DATABASE, echo=False)
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    tg_peer_id = Column(sqlalchemy.BIGINT, primary_key=True)
    registered = Column(sqlalchemy.DateTime, nullable=False, default=settings.datetime_now)

    user_full_name = Column(sqlalchemy.Text, nullable=False)
    note = Column(sqlalchemy.Text, nullable=True)

    last_availability_update = Column(sqlalchemy.DateTime, nullable=False, default=settings.datetime_now)
    days_period_for_using = Column(sqlalchemy.Integer, nullable=True)


class PersonalSettings(Base):
    __tablename__ = 'personal_settings'

    tg_peer_id = Column(sqlalchemy.BIGINT, ForeignKey('users.tg_peer_id'), primary_key=True)

    text_model_system_prompt = Column(
        sqlalchemy.Text, nullable=False,
        default="Вы высококвалифицированный и надежный помощник. Во время своих ответов используйте разметку Telegram Markdow. При предоставлении кода убедитесь, что он внесён в специальные ковычки. Если в тексте вы хотите создать заголовок, то используй символ '▎' вместо '#' или других стандартных методов разметки, но только где это необходимо для организации текста."
    )
    text_model_name = Column(sqlalchemy.Text, nullable=False, default="gpt-4o")


class Dialog(Base):
    __tablename__ = 'dialogs'

    message_id = Column(sqlalchemy.BIGINT, primary_key=True)
    dialog_owner_tg_peer_id = Column(sqlalchemy.BIGINT, ForeignKey('users.tg_peer_id'), nullable=False)
    response_time = Column(sqlalchemy.DateTime, nullable=False, default=settings.datetime_now)

    request = Column(sqlalchemy.Text, nullable=False)
    response = Column(sqlalchemy.Text, nullable=False)


Base.metadata.create_all(engine)
Session = scoped_session(sessionmaker(bind=engine))
