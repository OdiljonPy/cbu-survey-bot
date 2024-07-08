MoreAnswer = {}


async def get_answer(user_id: int | str, clear: bool = False):
    global MoreAnswer
    user_id = str(user_id)
    answer = MoreAnswer[user_id]['answer']
    if user_id not in MoreAnswer:
        MoreAnswer[user_id] = {'answer': []}
        return True
    if clear:
        MoreAnswer[user_id] = {'answer': []}
    return answer


async def check_answer(user_id: int | str, answer_id: int):
    global MoreAnswer
    user_id = str(user_id)
    if user_id not in MoreAnswer:
        MoreAnswer[user_id] = {'answer': [answer_id]}
        return False
    if answer_id not in MoreAnswer[user_id]['answer']:
        MoreAnswer[user_id]['answer'].append(answer_id)
        return False
    else:
        MoreAnswer[user_id]['answer'].remove(answer_id)
        return True


async def check_answer_not_update(user_id: int | str, answer_id: int):
    global MoreAnswer
    user_id = str(user_id)
    if user_id not in MoreAnswer:
        return False
    if answer_id not in MoreAnswer[user_id]['answer']:
        return False
    return True
