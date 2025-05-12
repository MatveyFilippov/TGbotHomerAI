import json
import logging
from typing import Final
import pytz


class SettingsJSON:
    SETTINGS_FILEPATH = "BotSettings.JSON"

    @classmethod
    def __get_dict_from_json_file(cls) -> dict:
        result = dict()
        try:
            with open(cls.SETTINGS_FILEPATH, "r", encoding="UTF-8") as jf:
                result = dict(json.load(jf))
        except FileNotFoundError:
            with open(cls.SETTINGS_FILEPATH, "w", encoding="UTF-8") as jf:
                json.dump(result, jf, ensure_ascii=False)
        return result

    @classmethod
    def get(cls, var_name: str, required_type=str, prompt: str | None = None):
        json_file_dict = cls.__get_dict_from_json_file()
        try:
            return required_type(json_file_dict[var_name])
        except (KeyError, TypeError):
            if not prompt:
                prompt = f"{var_name}: "
            return cls.__ask_and_write(var_name=var_name, required_type=required_type, prompt=prompt)

    @classmethod
    def get_optional(cls, var_name: str, default=None, write_default=True):
        json_file_dict = cls.__get_dict_from_json_file()
        try:
            return json_file_dict[var_name]
        except (KeyError, TypeError):
            if default is not None and write_default:
                cls.__append_to_json_file(key=var_name, value=default)
            return default

    @classmethod
    def __ask_value(cls, prompt: str, required_type=str):
        while True:
            try:
                return required_type(input(prompt))
            except ValueError:
                print(f" >>> Value should be '{required_type}'")

    @classmethod
    def __append_to_json_file(cls, key: str, value):
        json_file_dict = cls.__get_dict_from_json_file()
        json_file_dict[key] = value
        with open(cls.SETTINGS_FILEPATH, "w", encoding="UTF-8") as jf:
            json.dump(json_file_dict, jf, ensure_ascii=False)

    @classmethod
    def __ask_and_write(cls, var_name: str, prompt: str, required_type=str):
        value = cls.__ask_value(prompt=prompt, required_type=required_type)
        cls.__append_to_json_file(key=var_name, value=value)
        return value


BOT_API_TOKEN: Final = SettingsJSON.get(var_name="BOT_API_TOKEN")
BOT_DEVELOPER_TG_ID: Final = SettingsJSON.get(var_name="BOT_DEVELOPER_TG_ID", required_type=int)
LINK_TO_DATABASE: Final = SettingsJSON.get(var_name="LINK_TO_DATABASE", prompt=(
    "Use:\n * SQLite: '"
    "sqlite:///{path_to_db_file}"
    "'\n * PostgreSQL: '"
    "postgresql+psycopg2://{user}:{password}@{ip}:{port}/{db_name}"
    "'\nWrite link to db: "
))
BOT_TIMEZONE: Final = pytz.timezone(SettingsJSON.get_optional(var_name="BOT_TIMEZONE", default="Europe/Moscow"))
DATETIME_FORMAT: Final = SettingsJSON.get_optional(var_name="DATETIME_FORMAT", default="%Y-%m-%d %H:%M:%S")

logging.basicConfig(
    level=logging.INFO, filename=f"TGbotHomerAI.log", encoding="UTF-8", datefmt=DATETIME_FORMAT,
    format="\n\n'%(name)s':\n%(levelname)s %(asctime)s --> %(message)s"
)
logging.getLogger('aiogram').setLevel(logging.ERROR)
logging.getLogger('sqlalchemy.engine').setLevel(logging.ERROR)
