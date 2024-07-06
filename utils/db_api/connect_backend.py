import requests
from typing import Union


class DatabaseRequest:
    def __init__(self, url: str):
        self.url = url

    async def get_user(self, user_id: int) -> Union[str, bool]:
        response = requests.get(
            url=self.url + '/user?user_id=' + str(user_id)
        )
        if response.status_code == 200:
            return response.json().get('result').get('lang')
        return False

    async def create_user(self, user_id: int, full_name: str, username: str, lang: str) -> bool:
        response = requests.post(
            url=self.url + '/createUser',
            json={
                'user_id': user_id,
                'full_name': full_name,
                'username': username,
                'lang': lang,
            }
        )
        if response.status_code == 201:
            return response.json().get('ok')
        return False

    async def save_answer(self, user_id: int, question_id: int, answer: Union[list, int]) -> bool:
        response = requests.post(
            url=self.url + '/saveAnswer',
            json={
                'user_id': user_id,
                'question_id': question_id,
                'answer': answer,
            }
        )
        if response.status_code == 201:
            return response.json().get('ok')
        return False
