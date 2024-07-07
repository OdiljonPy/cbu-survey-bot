from keyboards.inline.inline_btn import create_inline_btn
from contextlib import suppress
from static_base.cache import get_answer, check_answer
from aiogram import types, F, Router
from data.config import db
from utils.misc.assistant import delete_message
from static_base.database_all_method import get_question_answers

router = Router()


@router.callback_query(F.data.startswith('user_lang'))
async def user_lang_callback(call: types.CallbackQuery):
    lang = call.data.split(':')[1]

    await db.create_user(
        user_id=call.from_user.id,
        full_name=call.from_user.full_name,
        lang=lang
    )

    await delete_message(call)
    message = await create_inline_btn(call.from_user.id, question_id=1)
    await call.message.answer(
        text=message.get('text'),
        reply_markup=message.get('btn')
    )


@router.callback_query(F.data.startswith('more_answer_checked'))
async def more_answer_handler_step(call: types.CallbackQuery):
    question_id = int(call.data.split(':')[1])
    answer_id = int(call.data.split(':')[2])

    await check_answer(call.from_user.id, answer_id)
    message = await create_inline_btn(call.from_user.id, question_id)
    with suppress(Exception):
        await call.message.edit_text(
            text=message.get('text'),
            reply_markup=message.get('btn')
        )
    return


@router.callback_query(F.data.startswith('more_answer_done'))
async def more_answer_handler_done(call: types.CallbackQuery):
    question_id = int(call.data.split(':')[1])
    answer_ids = await get_answer(call.from_user.id, clear=True)
    if question_id + 1 == 16:
        await delete_message(call)
        user_lang = await db.get_user(call.from_user.id)
        lang = user_lang.get('lang')
        await call.message.answer(
            text={
                'uz': "Ushbu so‘rovnomada ishtirok etganingiz uchun rahmat!",
                'ru': "Благодарим вас за участие в нашем опросе!",
                'kr': "Ушбу сўровномада иштирок этганингиз учун раҳмат!"
            }.get(lang)
        )
        await db.save_answer(
            user_id=call.from_user.id,
            question_id=question_id,
            answer_ids=answer_ids,
        )
        await db.create_user(
            user_id=call.from_user.id,
            full_name=call.from_user.full_name,
            lang=lang,
            status=True
        )
        return
    await db.save_answer(
        user_id=call.from_user.id,
        question_id=question_id,
        answer_ids=answer_ids,
    )

    message = await create_inline_btn(call.from_user.id, question_id + 1)
    await delete_message(call)
    await call.message.answer(
        text=message.get('text'),
        reply_markup=message.get('btn')
    )
    return


@router.callback_query(F.data.startswith('one_answer_done'))
async def one_answer_handler_checked(call: types.CallbackQuery):
    question_id = int(call.data.split(':')[1])
    answer_id = int(call.data.split(':')[2])
    if question_id + 1 == 16:
        await delete_message(call)
        user_lang = await db.get_user(call.from_user.id)
        lang = user_lang.get('lang')
        await call.message.answer(
            text={
                'uz': "Ushbu so‘rovnomada ishtirok etganingiz uchun rahmat!",
                'ru': "Благодарим вас за участие в нашем опросе!",
                'kr': "Ушбу сўровномада иштирок этганингиз учун раҳмат!"
            }.get(lang)
        )
        await db.save_answer(
            user_id=call.from_user.id,
            question_id=question_id,
            answer_ids=answer_id,
        )
        await db.create_user(
            user_id=call.from_user.id,
            full_name=call.from_user.full_name,
            lang=lang,
            status=True
        )
        return
    message = await create_inline_btn(call.from_user.id, question_id + 1)

    if question_id == 5:  # 5
        text = await get_question_answers(question_id=5, user_id=call.from_user.id)
        if text[answer_id] in ["йўқ", "yo‘q", "нет"]:
            message = await create_inline_btn(call.from_user.id, question_id + 2)

    if question_id == 7:  # 7
        text = await get_question_answers(question_id=7, user_id=call.from_user.id)
        if text[answer_id] in ["йўқ", "yo‘q", "нет"]:
            message = await create_inline_btn(call.from_user.id, question_id + 6)

    await db.save_answer(
        user_id=call.from_user.id,
        question_id=question_id,
        answer_ids=answer_id,
    )

    await delete_message(call)
    await call.message.answer(
        text=message.get('text'),
        reply_markup=message.get('btn')
    )
