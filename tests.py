import threading

from vk_bot.all_data import users, materials, questions_success
from vk_bot.auth import register, authorisation
from vk_bot.handlers import greeting, get_topics, start_test, get_statistics, go_to_hub
from vk_bot.notifications import set_notifications, notify_about_new_tests
from vk_bot.init import vk
import time

from vk_bot.sending_messages import send_message

user_id = 307377747
username = vk.users.get(user_id=user_id, fields='first_name')[0]['first_name']


fake_data = {
    'IT': {
        '1. Компьютер, подключенный к Internet, обязательно имеет: (..-адрес)': 'IP',
        '2. Для передачи в сети web-страниц используется протокол:': 'HTTP',
        '3. Как называется программа файловый менеджер, входящая в состав операционной среды Windows?': 'Проводник'
    },
    'История': {
        '1. Кто первым правил на Руси?': 'Рюрик',
        '2. В каком году началась вторая мировая война?': '1939',
        '3. При каком императоре Россия имела наибольшую по площади территорию?(Назовите только его/её имя)':
            'Александр'

    }
}

fake_questions = {
    'Автомобили': {
        '1. В какой стране была создана автомобильная компания «Феррари»?': 'Италия',
        '2. Какая категория водительского удостоверения дает право работать водителем автобуса?': 'D',
        '3. Эта машина подняла репутацию автомобильной промышленности СССР. Интерес к ней оказался настолько '
        'высоким, что она продавалась за рубежом.': 'Победа'
    },
    'Природа': {
        '1. Сколько ног у паука?': '8',
        '2. Назовите самое умное животное среди морских животных.': 'Дельфин',
        '3. Назовите самое быстрое животное на нашей планете.': 'Гепард',
        '4. Какое дерево является самым высоким в мире?': "Эвкалипт",
        '5. Назовите самое крупное млекопитающее на земле(одно слово)': "Кит"
    }
}


def test01_greeting():

    greeting(user_id)

    expected_message = 'Привет! Я чат-бот с интересными вопросами! Войди или зарегистрируйся, чтобы продолжить.'
    assert vk.messages.getHistory(user_id=user_id, count=1)['items'][0]['text'] == expected_message
    assert username not in users
    assert username not in questions_success


def test02_topics_not_registered():

    get_topics(username=username, user_id=user_id)

    expected_message = "Сначала зарегистрируйтесь или авторизуйтесь"
    assert vk.messages.getHistory(user_id=user_id, count=1)['items'][0]['text'] == expected_message
    assert username not in users
    assert username not in questions_success


def test03_get_statistics_not_registered():

    get_statistics(username=username, user_id=user_id)

    expected_message = "Сначала зарегистрируйтесь или авторизуйтесь"
    assert vk.messages.getHistory(user_id=user_id, count=1)['items'][0]['text'] == expected_message
    assert username not in users
    assert username not in questions_success


def test04_start_test_not_registered():

    start_test(username=username, user_id=user_id, text='Автомобили')

    expected_message = "Прежде чем приступить к викторине, зарегистрируйтесь или авторизуйтесь"
    assert vk.messages.getHistory(user_id=user_id, count=1)['items'][0]['text'] == expected_message
    assert username not in users
    assert username not in questions_success


def test05_set_notifications_not_registered():

    set_notifications(username=username, user_id=user_id)

    expected_message = "Сначала зарегистрируйтесь или авторизуйтесь"
    assert vk.messages.getHistory(user_id=user_id, count=1)['items'][0]['text'] == expected_message
    assert username not in users
    assert username not in questions_success


def test06_authorisation_not_registered():

    authorisation(username, user_id)

    expected_message = 'Вы не зарегистрированы. Сначала зарегистрируйтесь'
    assert vk.messages.getHistory(user_id=user_id, count=1)['items'][0]['text'] == expected_message
    assert username not in users
    assert username not in questions_success


def test07_register_new_user():

    register(user_id)

    assert users[username] == {
        'notifications': False,
        'change_name_flag': False,
        'start_schedule_flag': False,
        'questions': 0,
        'right': 0,
        'authorisation_flag': False,
        'value': 0,
        'id': user_id,
        'ans_flag': False
    }

    assert questions_success[username] == {
        'Автомобили': False,
        'Природа': False,
    }

    for ctg in fake_questions:
        assert not questions_success[username][ctg]

    assert (vk.messages.getHistory(user_id=user_id, count=1)['items'][0]['text'] ==
            'Вы успешно зарегистрированы! Авторизуйтесь, чтобы продолжить работу с ботом')


def test08_register_existing_user():

    register(user_id)

    assert users[vk.users.get(user_id=user_id, fields='first_name')[0]['first_name']] == {
        'notifications': False,
        'change_name_flag': False,
        'start_schedule_flag': False,
        'questions': 0,
        'right': 0,
        'authorisation_flag': False,
        'value': 0,
        'id': user_id,
        'ans_flag': False
    }
    for ctg in fake_questions:
        assert not questions_success[username][ctg]

    assert (vk.messages.getHistory(user_id=user_id, count=1)['items'][0]['text'] ==
            'Вы уже зарегистрированы. Авторизуйтесь')


def test09_authorisation_registered():

    authorisation(username, user_id)

    expected_message = 'Вы успешно авторизованы! Переходите к темам)'
    assert vk.messages.getHistory(user_id=user_id, count=1)['items'][0]['text'] == expected_message
    assert username in users
    assert users[username]['authorisation_flag']


def test10_authorisation_already_authorised():

    authorisation(username, user_id)

    expected_message = 'Вы уже авторизованы! Переходите к темам)'
    assert vk.messages.getHistory(user_id=user_id, count=1)['items'][0]['text'] == expected_message
    assert username in users
    assert users[username]['authorisation_flag']


def test11_get_topics_authorised():

    get_topics(username, user_id)

    expected_message = 'Вот ваши темы на сегодня:\nАвтомобили\nПрирода'
    assert vk.messages.getHistory(user_id=user_id, count=1)['items'][0]['text'] == expected_message


def test12_get_statistics_number1():

    get_statistics(username=username, user_id=user_id)

    expected_message = (f'Ваша статистика:\n'
                        f'Правильных ответов: {users[username]["right"]}\n'
                        f'Всего было задано вопросов: {users[username]["questions"]}\n'
                        f'Всего очков: {users[username]["value"]}')
    assert vk.messages.getHistory(user_id=user_id, count=1)['items'][0]['text'] == expected_message


def test13_go_to_hub():

    go_to_hub(user_id=user_id)

    expected_message = 'Вы на начальной странице'
    assert vk.messages.getHistory(user_id=user_id, count=1)['items'][0]['text'] == expected_message


def test14_notifications1():
    assert not users[username]['notifications']
    set_notifications(username=username, user_id=user_id)
    assert users[username]['notifications']
    expected_message = 'Вы подписались на рассылку! Новая викторина будет приходить каждый час.'
    assert vk.messages.getHistory(user_id=user_id, count=1)['items'][0]['text'] == expected_message


def test15_notifications2():
    assert users[username]['notifications']
    set_notifications(username=username, user_id=user_id)
    assert not users[username]['notifications']
    expected_message = 'Вы отписались от рассылки!'
    assert vk.messages.getHistory(user_id=user_id, count=1)['items'][0]['text'] == expected_message


def test16_notifications3():
    assert not users[username]['notifications']
    set_notifications(username=username, user_id=user_id)
    assert users[username]['notifications']
    expected_message = 'Вы подписались на рассылку! Новая викторина будет приходить каждый час.'
    assert vk.messages.getHistory(user_id=user_id, count=1)['items'][0]['text'] == expected_message


test_answers = ['италия', 'D', 'd']
sleeps = [5, 10, 5]


def beta_start_test(username, this_user_id, text):
    idx = 0
    for question in fake_questions[text]:
        answer = fake_questions[text][question]
        send_message(this_user_id, question + "\nУ вас 20 секунд на ответ")

        history = vk.messages.getHistory(user_id=this_user_id, count=1)
        last_message = history['items'][0]['text']
        old_message = history['items'][0]['text']
        start = time.perf_counter()
        users[username]['ans_flag'] = False
        while time.perf_counter() - start < 20:
            time.sleep(sleeps[idx])
            send_message(cur_user_id=user_id, message=test_answers[idx])
            time.sleep(1)
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
                    idx += 1
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
    send_message(this_user_id, 'Викторина завершена!')


def test17_start_test():

    assert username in questions_success
    assert username in users
    assert not questions_success[username]['Автомобили']
    beta_start_test(username=username, this_user_id=user_id, text='Автомобили')

    assert vk.messages.getHistory(user_id=user_id, count=1)['items'][0]['text'] == 'Викторина завершена!'
    assert users[username]['value'] == 3
    assert users[username]['right'] == 2
    assert users[username]['questions'] == 3


def test18_start_test2():
    start_test(username=username, user_id=user_id, text='Автомобили')

    expected_message = 'Вы уже проходили эту викторину'
    assert vk.messages.getHistory(user_id=user_id, count=1)['items'][0]['text'] == expected_message
    assert questions_success[username]['Автомобили']


def beta_notify_about_new_tests():
    fake_news_thread = threading.Thread(target=notify_about_new_tests, daemon=True)
    fake_news_thread.start()
    while fake_data:
        time.sleep(30)
        last_key = list(fake_data)[-1]
        fake_questions[last_key] = fake_data.pop(last_key)
        for user in users:
            questions_success[user][last_key] = False
            if users[user]['notifications']:
                send_message(users[user]['id'], 'Новая викторина! Посмотри скорее')


def test19_notifications4():
    beta_notify_about_new_tests()
    assert len(fake_questions) == 4
    assert len(fake_data) == 0
    assert len(questions_success[username]) == 4
    for key in questions_success[username]:
        if key != 'Автомобили':
            assert not questions_success[username][key]
        else:
            assert questions_success[username][key]
