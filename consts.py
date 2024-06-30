import random

BASE_URL = 'https://www.instagram.com/'

MYUSERNAME = 'fatfry666'
PASSWORD = "taim666"

LOGIN_URL = BASE_URL + 'accounts/login/'
PROFILE_URL = BASE_URL + f'{MYUSERNAME}/'
FOLLOWING_URL = PROFILE_URL + 'following/'
FOLLOWERS_URL = PROFILE_URL + 'followers/'

LOOP = 2
AMOUNT_OF_UNFOLLOW = 30

# Пути к кнопкам
FOLLOW_BUTTON_CSS_SELECTOR = "//div[contains(text(), 'Удалить')]"
UNFOLLOW_BUTTON_CSS_SELECTOR = 'button._a9--._ap36._a9-_'

DEFAULT_TIME_SLEEP = random.randint(5, 8)