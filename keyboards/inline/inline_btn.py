from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton, InlineKeyboardMarkup
from static_base.database_all_method import is_more_answers, get_question_answers, is_long_answers, get_question_text
from static_base.cache import check_answer_not_update


async def create_more_answer_btn(user_id: int, question_id: int) -> InlineKeyboardMarkup:
    btn_list = await get_question_answers(question_id, user_id)
    btn = InlineKeyboardBuilder()
    for text in btn_list:
        answer_id = btn_list.index(text)
        if await check_answer_not_update(user_id, answer_id):
            text = '✅ ' + text

        btn.add(
            InlineKeyboardButton(text=text, callback_data=f"more_answer_checked:{question_id}:{answer_id}"),
        )
    btn.add(InlineKeyboardButton(text='Tasdiqlash', callback_data=f"more_answer_done:{question_id}"))
    btn.adjust(*[1])
    return btn.as_markup()


async def create_more_answer_btn_long(user_id: int, question_id: int) -> InlineKeyboardMarkup:
    btn_list = await get_question_answers(question_id, user_id)
    btn = InlineKeyboardBuilder()
    for text in btn_list:
        answer_id = btn_list.index(text)
        if await check_answer_not_update(user_id, answer_id):
            text = '✅ ' + str(answer_id + 1)
        else:
            text = str(answer_id + 1)

        btn.add(
            InlineKeyboardButton(text=text, callback_data=f"more_answer_checked:{question_id}:{answer_id}"),
        )
    btn.add(InlineKeyboardButton(text='Tasdiqlash', callback_data=f"more_answer_done:{question_id}"))
    btn.adjust(*([3] * (len(btn_list) // 3)) + [1])
    return btn.as_markup()


async def create_one_answer_btn(user_id: int, question_id: int):
    btn_list = await get_question_answers(question_id, user_id)
    btn = InlineKeyboardBuilder()
    for text in btn_list:
        answer_id = btn_list.index(text)
        btn.add(
            InlineKeyboardButton(text=text, callback_data=f"one_answer_done:{question_id}:{answer_id}"),
        )
    btn.adjust(*[1])
    return btn.as_markup()


async def create_one_answer_btn_long(user_id: int, question_id: int):
    btn_list = await get_question_answers(question_id, user_id)
    btn = InlineKeyboardBuilder()
    for text in btn_list:
        answer_id = btn_list.index(text)
        btn.add(
            InlineKeyboardButton(text=str(answer_id + 1), callback_data=f"one_answer_done:{question_id}:{answer_id}"),
        )
    btn.adjust(*([3] * (len(btn_list) // 3)) + [1])
    return btn.as_markup()


async def create_inline_btn(user_id: int, question_id: int) -> dict:
    if await is_long_answers(question_id):
        btn_list = await get_question_answers(question_id, user_id)
        ans_text = await get_question_text(question_id, user_id)
        ans_text = f'{question_id}. ' + ans_text + '\n\n'
        for text in btn_list:
            answer_id = btn_list.index(text)
            ans_text += f"\n{answer_id + 1}. {text}"

        if await is_more_answers(question_id):
            btn = await create_more_answer_btn_long(user_id, question_id)
        else:
            btn = await create_one_answer_btn_long(user_id, question_id)

        return {
            'text': ans_text,
            'btn': btn
        }

    if await is_more_answers(question_id):
        btn = await create_more_answer_btn(user_id, question_id)
    else:
        btn = await create_one_answer_btn(user_id, question_id)

    ans_text = await get_question_text(question_id, user_id)
    ans_text = f'{question_id}. ' + ans_text + '\n\n'
    return {
        'text': ans_text,
        'btn': btn
    }


async def user_lang_btn() -> InlineKeyboardMarkup:
    btn = InlineKeyboardBuilder()
    btn.add(InlineKeyboardButton(text="O'zbek tili", callback_data='user_lang:uz'))
    btn.add(InlineKeyboardButton(text="Ўзбек тили", callback_data='user_lang:kr'))
    btn.add(InlineKeyboardButton(text="Русский язык", callback_data='user_lang:ru'))
    btn.adjust(*[2, 1])
    return btn.as_markup()
