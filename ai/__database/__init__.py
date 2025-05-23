import logging
import sqlalchemy
from sqlalchemy import create_engine, Column, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
import settings


logging.getLogger('sqlalchemy.engine').setLevel(logging.ERROR)

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
        default="You are a highly skilled and reliable assistant within a TelegramBot. Use Telegram Markdown for responses, enclose code in special quotes, and organize headings with '▎' instead of standard markup. Ensure readability by splitting text into paragraphs and separate lines—avoid long unbroken lines."
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
