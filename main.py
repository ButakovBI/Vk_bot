import threading

from vk_api.longpoll import VkEventType

from vk_bot.all_data import questions
from vk_bot.auth import register, authorisation
from vk_bot.handlers import get_statistics, start_test, get_topics, go_to_hub, greeting
from vk_bot.init import longpoll
from vk_bot.notifications import set_notifications, notify_about_new_tests

news_thread = threading.Thread(target=notify_about_new_tests, daemon=True)
news_thread.start()

cur_username = ''
while True:
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:

            if event.text.lower() == 'начать':
                greeting(user_id=event.user_id)

            elif event.text.lower() == 'уведомления':
                set_notifications(cur_username, user_id=event.user_id)

            elif event.text.lower() == 'статистика':
                get_statistics(username=cur_username, user_id=event.user_id)

            elif event.text in questions:
                start_test(cur_username, event.user_id, event.text)

            elif event.text.lower() == 'темы':
                get_topics(cur_username, event.user_id)

            elif event.text.lower() == 'регистрация':
                cur_username = register(event.user_id)

            elif event.text.lower() == 'авторизация':
                authorisation(cur_username, event.user_id)

            elif event.text.lower() == 'вернуться на начальную страницу':
                go_to_hub(user_id=event.user_id)
