import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll

group_key = ('vk1.a.SUGHutp5el1aE60W3e05RJKyJvj_Cp33RhpHsyIjlewR8MDOJaE_knIKXND8Oj9Yx8_OMUxNnk09i6Ar1DQgKIs4iv2Cd'
             'WA8qA-y-_hIZmc0_a5dAFMZLolTF1hR70tJPgkIzzZOPB1xrmAvOHajbIybkU4gXRH02GFmEmw8Xrli0EjWXi7OffVH'
             'bH4ZL2KArJw3VbeGONJB_eGUPFJegg')

vk_session = vk_api.VkApi(token=group_key)
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()
keyboard = VkKeyboard()
keyboard.add_button('Начать', color=VkKeyboardColor.POSITIVE)
