from playwright.sync_api import sync_playwright

import logging
from consts import LOGIN_URL, FOLLOWING_URL, FOLLOWERS_URL, MYUSERNAME, PASSWORD
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

    # Переходим на страницу подписок
    page.goto(FOLLOWING_URL, wait_until="load")
    page.wait_for_selector('div._aano')
    page.wait_for_selector('span._ap3a._aaco._aacw._aacx._aad7._aade')

    # Начинаем скроллить подписки
    SCROLL_CONTAINER_SELECTOR = 'div._aano'
    for i in range(SCROLL_FOLLOWINGS):
        page.evaluate(f"document.querySelector('{SCROLL_CONTAINER_SELECTOR}').scrollTo({i * 1000}, {i * 2000});")
        page.wait_for_timeout(2000)
    # Берем содержимое страницы подписок и парсим их имена
    current_page_content = page.content()
    our_followings = find_elements_with_classes(current_page_content)
    write_data_to_file(our_followings, 'followings.txt')

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


    res = set(our_followings) - set(our_followers)
    print(f'following =  {len(our_following)}\nfollowers = {len(our_followers)}\ndiff = {len(res)}')
    print(res)


    write_data_to_file(our_followers, 'followers.txt')
    write_data_to_file(our_following, 'following.txt')
    write_data_to_file(diff, 'unfollowers')


    def get_list_from_file(filename: str):
        with open('file.txt', 'r') as file:
            usernames = [line.strip() for line in file]
            return usernames


    usernames_from_file = get_list_srom_file('unfollowers.')
    print(set(usernames_from_file))

