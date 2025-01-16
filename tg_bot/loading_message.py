from aiogram import types
from aiogram import exceptions


class LoadingMessage:
    def __init__(self, request_message: types.Message):
        self.__request_message = request_message
        self.__loading_message: types.Message = None

    async def send(self):
        self.__loading_message = await self.__request_message.answer("Думаю...")

    async def delete(self):
        if self.__loading_message is None:
            return
        try:
            await self.__loading_message.delete()
        except (exceptions.MessageToDeleteNotFound, exceptions.MessageCantBeDeleted):
            pass
