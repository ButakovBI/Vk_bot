from vk_api.keyboard import VkKeyboard

from vk_bot.all_data import users, questions_success, questions
from vk_bot.init import vk
from vk_bot.sending_messages import send_message_with_keyboard


def register(user_id):
    user = vk.users.get(user_id=user_id, fields='first_name, id')[0]
    username = user['first_name']
    keyboard = VkKeyboard()
    if username in users:
        
        keyboard.add_button('Авторизация')
        send_message_with_keyboard(user_id, keyboard, 'Вы уже зарегистрированы. Авторизуйтесь')

    else:
        users[username] = {
            'notifications': False,
            'change_name_flag': False,
            'start_schedule_flag': False,
            'questions': 0,
            'right': 0,
            'authorisation_flag': False,
            'value': 0,
            'id': user['id'],
            'ans_flag': False
        }
        questions_success[username] = dict()
        for ctg in questions:
            questions_success[username][ctg] = False
        keyboard.add_button('Авторизация')
        send_message_with_keyboard(user_id, keyboard,
                                   'Вы успешно зарегистрированы! Авторизуйтесь, чтобы продолжить работу с ботом')
    return username


def authorisation(username, cur_user_id):
    keyboard = VkKeyboard()
    if username in users and users[username]['authorisation_flag']:
        keyboard.add_button('Темы')
        keyboard.add_line()
        keyboard.add_button('Вернуться на начальную страницу')
        send_message_with_keyboard(cur_user_id, keyboard, 'Вы уже авторизованы! Переходите к темам)')
    elif username in users:
        users[username]['authorisation_flag'] = True
        keyboard.add_button('Темы')
        keyboard.add_line()
        keyboard.add_button('Вернуться на начальную страницу')
        send_message_with_keyboard(cur_user_id, keyboard, 'Вы успешно авторизованы! Переходите к темам)')
    else:
        keyboard.add_button('Регистрация')
        send_message_with_keyboard(cur_user_id, keyboard, 'Вы не зарегистрированы. Сначала зарегистрируйтесь')
