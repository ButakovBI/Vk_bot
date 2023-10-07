import threading
import time

from vk_api.keyboard import VkKeyboard
from vk_bot.all_data import data, questions_success, questions, users
from vk_bot.sending_messages import send_message, send_message_with_keyboard


def notify_about_new_tests():
    while data:
        time.sleep(3600)
        last_key = list(data)[-1]
        questions[last_key] = data.pop(last_key)
        for user in users:
            questions_success[user][last_key] = False
            if users[user]['notifications']:
                send_message(users[user]['id'], 'Новая викторина! Посмотри скорее')


def set_notifications(username, user_id):
    if username in questions_success:
        if not users[username]['notifications']:
            users[username]['notifications'] = True
            send_message(user_id, 'Вы подписались на рассылку! Новая викторина будет приходить каждый час.')
        else:
            users[username]['notifications'] = False
            send_message(user_id, 'Вы отписались от рассылки!')
        return True
    else:
        keyboard = VkKeyboard()
        keyboard.add_button('Регистрация')
        keyboard.add_button('Авторизация')
        send_message_with_keyboard(user_id, keyboard, "Сначала зарегистрируйтесь или авторизуйтесь")
