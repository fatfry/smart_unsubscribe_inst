from playwright.sync_api import sync_playwright

import logging
from consts import LOGIN_URL, FOLLOWERS_URL, MYUSERNAME, PASSWORD, PROFILE_URL
from bs4 import BeautifulSoup


logging.basicConfig(filename='logs.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


username = MYUSERNAME
password = PASSWORD

SCROLL_FOLLOWERS = 130
SCROLL_FOLLOWINGS = 1630


def write_data_to_file(data: list, filename: str):
    with open(filename, 'a') as file:
        for line in data:
            file.write(line + '\n')


def find_elements_with_classes(html_content):
    # Создаем объект BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Ищем все элементы span с заданными классами
    classes = ["_ap3a", "_aaco", "_aacw", "_aacx", "_aad7", "_aade"]
    elements = soup.find_all('span', class_=lambda x: x and all(item in x.split() for item in classes))

    # Извлекаем текстовое содержимое найденных элементов
    texts = [element.get_text() for element in elements]

    return texts


with sync_playwright() as p:
    logging.info('Запускаем браузер')
    browser = p.chromium.launch(headless=False, slow_mo=50)
    context = browser.new_context()
    page = context.new_page()
    page.wait_for_timeout(10000)

    page.goto(LOGIN_URL, wait_until="load")

    # Ожидаем появления поля ввода логина и заполняем его
    LOGIN_INPUT_CSS_SELECTOR = 'input[name="username"]'
    page.wait_for_selector(LOGIN_INPUT_CSS_SELECTOR)
    page.fill(LOGIN_INPUT_CSS_SELECTOR, username)

    # Ожидаем появления поля пароля и заполняем его
    PASSWORD_INPUT_CSS_SELECTOR = 'input[name="password"]'
    page.wait_for_selector(PASSWORD_INPUT_CSS_SELECTOR)
    page.fill(PASSWORD_INPUT_CSS_SELECTOR, password)

    # Нажимаем кнопку войти
    page.click('button._acan._acap._acas._aj1-._ap30')
    page.wait_for_timeout(10000)

    #Открываем профиль
    page.goto(PROFILE_URL)
    page.wait_for_timeout(10000)

    # Переходим на страницу подписок
    page.click('a[href="/fatfry666/following/"]')
    page.wait_for_timeout(10000)
    page.wait_for_selector('div._ac76')
    page.wait_for_selector('div.xyi19xy.x1ccrb07.xtf3nb5.x1pc53ja.x1lliihq.x1iyjqo2.xs83m0k.xz65tgg.x1rife3k.x1n2onr6')

    # Начинаем скроллить подписки
    SCROLL_CONTAINER_SELECTOR = 'div.xyi19xy.x1ccrb07.xtf3nb5.x1pc53ja.x1lliihq.x1iyjqo2.xs83m0k.xz65tgg.x1rife3k.x1n2onr6'
    # page.evaluate("SCROLLABLE = true; addEventListener(\"scrollend\", (event) => {SCROLLABLE = false});")

    page.on("scrollend", lambda: SCROLLABLE = False)
    i = 0
    while SCROLLABLE:
        page.evaluate(f"document.querySelector('{SCROLL_CONTAINER_SELECTOR}').scrollTo({i * 1000}, {i * 2000});")
        page.wait_for_timeout(2000)
        i += 1
    logging.info('Конец скрола подписок')
    # Берем содержимое страницы подписок и парсим их имена
    current_page_content = page.content()
    our_followings = find_elements_with_classes(current_page_content)
    write_data_to_file(our_followings, 'followings.txt')
    page.wait_for_timeout(2000)

    # Начинаем скроллить подписчиков
    page.goto(FOLLOWERS_URL, wait_until="load")
    page.wait_for_selector('div._aano')
    SCROLL_CONTAINER_SELECTOR = 'div._aano'
    page.wait_for_timeout(10000)
    for i in range(SCROLL_FOLLOWERS):
        page.evaluate(f"document.querySelector('{SCROLL_CONTAINER_SELECTOR}').scrollTo({i * 1000}, {i * 2000});")
        page.wait_for_timeout(2000)
    # Берем содержимое страницы подписчиков и парсим их имена
    current_page_content = page.content()
    our_followers = find_elements_with_classes(current_page_content)
    write_data_to_file(our_followers, 'followers.txt')
