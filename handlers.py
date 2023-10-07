import time

from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from vk_bot.all_data import questions_success, questions, users, materials
from vk_bot.init import vk
from vk_bot.sending_messages import send_message_with_keyboard, send_message

keyboard = VkKeyboard()


def get_questions(username, this_user_id, text):
    global keyboard
    for question in questions[text]:

        answer = questions[text][question]
        send_message(this_user_id, question + "\nУ вас 20 секунд на ответ")

        history = vk.messages.getHistory(user_id=this_user_id, count=1)
        last_message = history['items'][0]['text']
        old_message = history['items'][0]['text']
        start = time.perf_counter()
        users[username]['ans_flag'] = False
        while time.perf_counter() - start < 20:
            if (vk.messages.getHistory(user_id=this_user_id, count=1)['items'][0]['text'].lower()
                    != last_message.lower()):

                last_message = vk.messages.getHistory(user_id=this_user_id, count=1)['items'][0]['text']
                if last_message.lower() == answer.lower():
                    if time.perf_counter() - start < 10:
                        send_message(this_user_id, 'Верно! +2 очка за скорость!')
                        users[username]['value'] += 2
                    else:
                        send_message(this_user_id, 'Верно! +1 очко')
                        users[username]['value'] += 1
                    users[username]['right'] += 1
                    users[username]['ans_flag'] = True
                    break
                elif last_message.lower() != 'Не совсем. Подумайте ещё'.lower():
                    send_message(this_user_id, 'Не совсем. Подумайте ещё')
        if not users[username]['ans_flag']:
            if last_message.lower() == old_message.lower():
                send_message(this_user_id, 'Вы проспали вопрос')
            else:
                send_message(this_user_id,
                             'Время вышло. ' + f'Правильный ответ: {answer}. Ссылка на материал: {materials[text]}')

        users[username]['questions'] += 1
    questions_success[username][text] = True


def get_topics(username, user_id):
    global keyboard
    keyboard = VkKeyboard()
    if username in questions_success:
        cnt = 0
        ans = 'Вот ваши темы на сегодня:\n'
        for category in questions:
            ans += category + '\n'
            if not questions_success[username][category]:
                cnt += 1
                keyboard.add_button(category)
                keyboard.add_line()
                if cnt == 4:
                    break
        keyboard.add_button('Вернуться на начальную страницу')
        send_message_with_keyboard(user_id, keyboard, ans)
    else:
        keyboard.add_button('Регистрация')
        keyboard.add_button('Авторизация')
        send_message_with_keyboard(user_id, keyboard, "Сначала зарегистрируйтесь или авторизуйтесь")


def get_statistics(username, user_id):
    global keyboard
    if username in questions_success:
        send_message(user_id, "Ваша статистика:\n"
                              f"Правильных ответов: {users[username]['right']}\n"
                              f"Всего было задано вопросов: {users[username]['questions']}\n"
                              f"Всего очков: {users[username]['value']}")
    else:
        keyboard = VkKeyboard()
        keyboard.add_button('Регистрация')
        keyboard.add_button('Авторизация')
        send_message_with_keyboard(user_id, keyboard, "Сначала зарегистрируйтесь или авторизуйтесь")


def greeting(user_id):
    global keyboard
    keyboard = VkKeyboard()
    keyboard.add_button('Регистрация')
    keyboard.add_line()
    keyboard.add_button('Авторизация')
    send_message_with_keyboard(user_id, keyboard,
                               'Привет! Я чат-бот с интересными вопросами!'
                               ' Войди или зарегистрируйся, чтобы продолжить.')


def start_test(username, user_id, text):
    global keyboard
    if username in questions_success:
        if not questions_success[username][text]:
            send_message(user_id, "Поехали!")
            get_questions(username, user_id, text)
            send_message_with_keyboard(user_id, keyboard, 'Викторина завершена!')
        else:
            send_message(user_id, "Вы уже проходили эту викторину")
    else:
        keyboard = VkKeyboard()
        keyboard.add_button('Регистрация')
        keyboard.add_button('Авторизация')
        send_message_with_keyboard(user_id, keyboard,
                                   "Прежде чем приступить к викторине, зарегистрируйтесь или авторизуйтесь")


def go_to_hub(user_id):
    global keyboard
    keyboard = VkKeyboard()
    keyboard.add_button('Статистика')
    keyboard.add_line()
    keyboard.add_button('Уведомления')
    keyboard.add_line()
    keyboard.add_button('Темы', color=VkKeyboardColor.POSITIVE)
    send_message_with_keyboard(user_id, keyboard, 'Вы на начальной странице')
