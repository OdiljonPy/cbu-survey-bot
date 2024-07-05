from aiogram import types, Router
from aiogram.filters import CommandStart

router = Router()


@router.message(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(
        text="Xush kelibsiz!"
    )
