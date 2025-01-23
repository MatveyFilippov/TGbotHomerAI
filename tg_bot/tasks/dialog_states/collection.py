from aiogram.dispatcher.filters.state import State, StatesGroup


DIALOG_NOT_AVAILABLE_STATE = State()


class FlagsToTextCreating(StatesGroup):  # TODO: add state when bot already creating answer
    web_search = State()


class DialogStates(StatesGroup):
    answer_is_creating = State()
