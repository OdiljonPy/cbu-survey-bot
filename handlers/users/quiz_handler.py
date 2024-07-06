from keyboards.inline.inline_btn import create_inline_btn
from contextlib import suppress
from static_base.cache import add_answer, get_answer
from aiogram import types, F, Router
from data.config import db
from utils.misc.assistant import delete_message
from static_base.database_all_method import (
    get_question_text,
    get_question_answers
)

router = Router()


@router.callback_query(F.data.startswith('user_lang'))
async def user_lang_callback(call: types.CallbackQuery):
    lang = call.data.split(':')[1]

    # update user/ save lang

    question_text = await get_question_text(question_id=1, lang=lang)
    answer_list = await get_question_answers(question_id=1, lang=lang)

    await call.message.answer(
        text=question_text,
        reply_markup=await create_inline_btn(
            call.from_user.id, question_id=1, btn_list=answer_list)
    )


@router.callback_query(F.data.startswith('more_answer_checked'))
async def more_answer_handler_step(call: types.CallbackQuery):
    user_lang = await db.get_user(call.from_user.id)
    question_id = int(call.data.split(':')[1])
    answer_id = int(call.data.split(':')[2])
    await add_answer(user_id=call.from_user.id, answer_id=answer_id)

    question_text = await get_question_text(question_id, user_lang)
    answer_list = await get_question_answers(question_id, user_lang)
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

    question_text = await get_question_text(question_id + 1, user_lang)
    answer_list = await get_question_answers(question_id + 1, user_lang)
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

    question_text = await get_question_text(question_id + 1, user_lang)
    answer_list = await get_question_answers(question_id + 1, user_lang)
    await delete_message(call)
    await call.message.answer(
        text=question_text,
        reply_markup=await create_inline_btn(
            call.from_user.id, question_id, answer_list
        )
    )
