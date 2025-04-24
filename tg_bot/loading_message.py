from .tasks.dialog_states import unset_all_states
from .tasks.dialog_states.collection import DialogStates
from aiogram import types, exceptions


class LoadingMessage:
    def __init__(self, request_message: types.Message):
        self.__user_tg_peer_id = request_message.from_user.id
        self.__request_message = request_message
        self.__loading_message: types.Message = None

    async def send(self):
        await DialogStates.answer_is_creating.set()
        self.__loading_message = await self.__request_message.answer("Thinking...")

    async def delete(self):
        await unset_all_states(self.__user_tg_peer_id)
        if self.__loading_message is None:
            return
        try:
            await self.__loading_message.delete()
        except (exceptions.MessageToDeleteNotFound, exceptions.MessageCantBeDeleted):
            pass
