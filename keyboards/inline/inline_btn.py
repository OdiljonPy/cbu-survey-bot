from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton, InlineKeyboardMarkup
from static_base.cache import check_answer
from static_base.database_uz import is_more_answers


async def create_more_answer_btn(user_id: int, question_id: int, btn_list: list) -> InlineKeyboardMarkup:
    btn = InlineKeyboardBuilder()
    for text in btn_list:
        answer_id = btn_list.index(text)
        if not await check_answer(user_id, answer_id):
            text = '✅ ' + text
        else:
            text = '☑ ' + text
        btn.add(
            InlineKeyboardButton(text=text, callback_data=f"more_answer_checked:{question_id}:{answer_id}"),
        )
    btn.add(InlineKeyboardButton(text='Tasdiqlash', callback_data=f"more_answer_done:{question_id}"))
    btn.adjust(*([2] * (len(btn_list) // 2)) + [1])
    return btn.as_markup()


async def create_one_answer_btn(question_id: int, btn_list: list):
    btn = InlineKeyboardBuilder()
    for text in btn_list:
        answer_id = btn_list.index(text)
        btn.add(
            InlineKeyboardButton(text=text, callback_data=f"one_answer_checked:{question_id}:{answer_id}"),
        )
    btn.adjust(*([2] * (len(btn_list) // 2)) + [1])
    return btn.as_markup()


async def create_inline_btn(user_id: int, question_id: int, btn_list: list) -> InlineKeyboardMarkup:
    if is_more_answers(user_id):
        return await create_more_answer_btn(user_id, question_id, btn_list)
    return await create_one_answer_btn(question_id, btn_list)
