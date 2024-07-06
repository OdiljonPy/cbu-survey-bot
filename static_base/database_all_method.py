async def is_more_answers(question_id: int) -> bool:
    from .database_uz import BaseUz
    return BaseUz[question_id].get('more_answers')


async def get_question_text(question_id: int, lang: str) -> str:
    from .database_uz import BaseUz
    from .database_kr import BaseKr
    from .databese_ru import BaseRu
    if lang == 'uz':
        return BaseUz[question_id - 1].get('question')

    if lang == 'kr':
        return BaseKr[question_id - 1].get('question')

    if lang == 'ru':
        return BaseRu[question_id - 1].get('question')


async def get_question_answers(question_id: int, lang: str) -> list:
    from .database_uz import BaseUz
    from .database_kr import BaseKr
    from .databese_ru import BaseRu
    if lang == 'uz':
        return list(BaseUz[question_id - 1].get('answers'))

    if lang == 'kr':
        return list(BaseKr[question_id - 1].get('answers'))

    if lang == 'ru':
        return list(BaseRu[question_id - 1].get('answers'))
