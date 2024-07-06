MoreAnswer = {}


async def add_answer(user_id: int | str, answer_id: int):
    global MoreAnswer
    user_id = str(user_id)
    if user_id not in MoreAnswer:
        MoreAnswer[user_id] = {'answer': [answer_id]}
        return True
    MoreAnswer[user_id]['answer'].append(answer_id)
    return True


async def check_answer(user_id: int | str, answer_id: int):
    global MoreAnswer
    user_id = str(user_id)
    if user_id not in MoreAnswer:
        return True
    return answer_id in MoreAnswer[user_id]['answer']


async def get_answer(user_id: int | str, clear: bool = False):
    global MoreAnswer
    user_id = str(user_id)
    answer = MoreAnswer[user_id]['answer']
    if user_id not in MoreAnswer:
        return True
    if clear:
        MoreAnswer[user_id]['answer'] = []
    return answer
