from contextlib import suppress
from aiogram.types import Message, CallbackQuery
from typing import Union


async def delete_message(message: Union[Message, CallbackQuery]):
    if isinstance(message, Message):
        with suppress(Exception):
            await message.delete()
    else:
        with suppress(Exception):
            await message.message.delete()
    return True
