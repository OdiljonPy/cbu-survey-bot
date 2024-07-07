import asyncio
from aiogram import types, Router
from aiogram.filters import CommandStart
from keyboards.inline.inline_btn import user_lang_btn
from data.config import db

router = Router()

FirstText = ("Assalomu alaykum {}\n"
             "Aholi qarz yukini aniqlash bo‘yicha so‘rovnomaga xush kelibsiz!\n"
             "Iltimos, tilni tanlang\n\n"
             "Ассалому алайкум {}\n"
             "Аҳоли қарз юкини аниқлаш бўйича сўровномага хуш келибсиз!\n"
             "Илтимос, тилни танланг\n\n"
             "Здравствуйте {}\n"
             "Добро пожаловать в опросник по определению долговой нагрузки населения!\n"
             "Пожалуйста, выберите язык")

NotSelectLang = ("Assalomu alaykum {}\n"
                 "Iltimos, tilni tanlang!\n\n"
                 "Ассалому алайкум {}\n"
                 "Илтимос, тилни танланг!\n\n"
                 "Здравствуйте {}\n"
                 "Пожалуйста, выберите язык!")

ProcessText = {
    'uz': ("Assalomu alaykum {}\n"
           "Iltimos so'rovnomani davom ettiring"),
    'kr': ("Ассалому алайкум {}\n"
           "Илтимос сўровномани давом эттиринг"),
    'ru': ("Здравствуйте {}\n"
           "Пожалуйста, продолжайте опрос")
}

FinishText = {
    'uz': ("Assalomu alaykum {}\n"
           "Siz so'rovnomamizda oldin ishtirok etgansiz!"),
    'kr': ("Ассалому алайкум {}\n"
           "Сиз сўровномамизда олдин иштирок этгансиз!"),
    'ru': ("Здравствуйте {}\n"
           "Вы уже участвовали в нашем опросе!")
}


@router.message(CommandStart())
async def bot_start(message: types.Message):
    user_lang = await db.get_user(message.from_user.id)
    if len(user_lang) < 1:
        await message.answer(
            text=FirstText.format(
                message.from_user.full_name, message.from_user.full_name, message.from_user.full_name),
            reply_markup=await user_lang_btn()
        )

        await db.create_user(
            user_id=message.from_user.id,
            full_name=message.from_user.full_name
        )
        return

    if not user_lang.get('lang'):
        await message.answer(
            text=NotSelectLang.format(
                message.from_user.full_name, message.from_user.full_name, message.from_user.full_name),
            reply_markup=await user_lang_btn()
        )

    if not user_lang.get('status'):
        await message.answer(
            text=ProcessText.get(user_lang.get('lang')).format(message.from_user.full_name),
        )
        return
    await message.answer(
        text=FinishText.get(user_lang.get('lang')).format(message.from_user.full_name)
    )
    return


def user_status(user_id):
    user = asyncio.run(db.get_user(user_id))
    return user.get('status')


@router.message(lambda msg: user_status(msg.from_user.id))
async def check_user_status(message: types.Message):
    user_lang = await db.get_user(message.from_user.id)
    lang = user_lang.get('lang')
    await message.answer(
        text=FinishText.get(lang).format(message.from_user.full_name)
    )
    return


@router.message(lambda msg: not user_status(msg.from_user.id))
async def check_user_status(message: types.Message):
    user_lang = await db.get_user(message.from_user.id)
    lang = user_lang.get('lang')
    await message.answer(
        text=ProcessText.get(lang).format(message.from_user.full_name)
    )
    return
