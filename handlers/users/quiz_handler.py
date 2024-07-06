from keyboards.inline.inline_btn import create_inline_btn
from contextlib import suppress
from static_base.cache import add_answer, get_answer
from aiogram import types, F, Router
from data.config import db
from utils.misc.assistant import delete_message
from static_base.database_uz import (
    get_question_text_uz,
    get_question_answers_uz
)
from static_base.databese_ru import (
    get_question_text_ru,
    get_question_answers_ru
)

router = Router()


@router.message(F.text.startswith('boshlash'))
async def quiz_handler(message: types.Message):
    pass


@router.callback_query(F.data.startswith('more_answer_checked'))
async def more_answer_handler_step(call: types.CallbackQuery):
    user_lang = await db.get_user(call.from_user.id)
    question_id = int(call.data.split(':')[1])
    answer_id = int(call.data.split(':')[2])
    await add_answer(user_id=call.from_user.id, answer_id=answer_id)
    if user_lang == 'ru':
        question_text = await get_question_text_ru(question_id)
        answer_list = await get_question_answers_ru(question_id)
    else:
        question_text = await get_question_text_uz(question_id)
        answer_list = await get_question_answers_uz(question_id)
    with suppress(Exception):
        await call.message.edit_text(
            text=question_text,
            reply_markup=await create_inline_btn(
                call.from_user.id, question_id, answer_list)
        )
    return


@router.callback_query(F.data.startswith('more_answer_done'))
async def more_answer_handler_done(call: types.CallbackQuery):
    user_lang = await db.get_user(call.from_user.id)
    question_id = int(call.data.split(':')[1])
    answer_ids = await get_answer(call.from_user.id, clear=True)

    # save db

    if user_lang == 'ru':
        question_text = await get_question_text_ru(question_id)
        answer_list = await get_question_answers_ru(question_id)
    else:
        question_text = await get_question_text_uz(question_id)
        answer_list = await get_question_answers_uz(question_id)
    await delete_message(call)
    await call.message.answer(
        text=question_text,
        reply_markup=await create_inline_btn(
            call.message.from_user.id, question_id, answer_list)
    )
    return


@router.callback_query(F.data.startswith('one_answer_checked'))
async def one_answer_handler_checked(call: types.CallbackQuery):
    user_lang = await db.get_user(call.from_user.id)
    question_id = int(call.data.split(':')[1])
    answer_id = int(call.data.split(':')[2])

    # save db

    if user_lang == 'ru':
        question_text = await get_question_text_ru(question_id)
        answer_list = await get_question_answers_ru(question_id)
    else:
        question_text = await get_question_text_uz(question_id)
        answer_list = await get_question_answers_uz(question_id)
    await delete_message(call)
    await call.message.answer(
        text=question_text,
        reply_markup=await create_inline_btn(
            call.from_user.id, question_id, answer_list
        )
    )
