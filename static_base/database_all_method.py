async def is_long_answers(question_id: int) -> bool:
    from .database_uz import BaseUz
    return BaseUz[question_id - 1].get('long_answers')


async def is_more_answers(question_id: int) -> bool:
    from .database_uz import BaseUz
    return BaseUz[question_id - 1].get('more_answers')


async def get_question_text(question_id: int, user_id: int) -> str:
    from data.config import db
    from .database_uz import BaseUz
    from .database_kr import BaseKr
    from .databese_ru import BaseRu
    user_lang = await db.get_user(user_id)
    lang = user_lang.get('lang')
    if lang == 'uz':
        return BaseUz[question_id - 1].get('question')

    if lang == 'kr':
        return BaseKr[question_id - 1].get('question')

    if lang == 'ru':
        return BaseRu[question_id - 1].get('question')


async def get_question_answers(question_id: int, user_id: int) -> list:
    from data.config import db
    from .database_uz import BaseUz
    from .database_kr import BaseKr
    from .databese_ru import BaseRu
    user_lang = await db.get_user(user_id)
    lang = user_lang.get('lang')
    if lang == 'uz':
        return list(BaseUz[question_id - 1].get('answers'))

    if lang == 'kr':
        return list(BaseKr[question_id - 1].get('answers'))

    if lang == 'ru':
        return list(BaseRu[question_id - 1].get('answers'))
