from vk_api.utils import get_random_id
from init import vk


def send_message(cur_user_id, message):
    vk.messages.send(
        user_id=cur_user_id,
        message=message,
        random_id=get_random_id()
    )


# %%
def send_message_with_keyboard(cur_user_id, kb, message):
    vk.messages.send(keyboard=kb.get_keyboard(),
                     key='eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJxdWV1ZV9pZCI6IjIyMjc1MjU5OCIsI'
                         'nVudGlsIjoxNjk2MjQzMTA0MjkyMTgzMjAxfQ.F2McngYBbWubHsVqJEU4O6xz5wNW5Ub8'
                         'lhu0ysXJ4PUVVTTEzNaCj-YkbuJKzpeOuL9RpZ3DQK90d2aijf6SCQ',
                     server='https://lp.vk.com/whp/222752598',
                     ts='74',
                     user_id=cur_user_id,
                     random_id=get_random_id(),
                     message=message
                     )
