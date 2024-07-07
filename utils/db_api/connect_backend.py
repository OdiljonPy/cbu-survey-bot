import requests
from typing import Union
from static_base.database_all_method import get_question_text, get_question_answers


class DatabaseRequest:
    def __init__(self, url: str):
        self.url = url

    async def get_user(self, user_id: int) -> dict:
        response = requests.get(
            url=self.url + '/user?user_id=' + str(user_id)
        )
        if response.status_code == 200:
            res = response.json().get('result')
            return {
                'lang': res.get('language'),
                'status': res.get('status')
            }
        return {}

    async def create_user(self, user_id: int, full_name: str, lang: str = '', status: bool = False) -> bool:
        response = requests.post(
            url=self.url + '/create/user/',
            json={
                'tg_user_id': user_id,
                'full_name': full_name,
                'language': lang,
                'status': status
            }
        )
        if response.status_code == 201:
            return response.json().get('ok')
        return False

    async def save_answer(self, user_id: int, question_id: int, answer_ids: Union[list, int]) -> bool:
        question_text = await get_question_text(question_id, user_id)
        answers_list = await get_question_answers(question_id, user_id)
        answer_text = ''
        if isinstance(answer_ids, list):
            for pk in answer_ids:
                answer_text += f"{answers_list[pk]}\n\n"
        else:
            answer_text = answers_list[answer_ids]
        response = requests.post(
            url=self.url + '/create/answer/',
            json={
                'tg_user': user_id,
                'question': question_text,
                'answer': answer_text,
            }
        )
        if response.status_code == 201:
            return response.json().get('ok')
        return False
