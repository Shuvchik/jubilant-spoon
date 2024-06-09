from selenium import webdriver  # класс управления браузером
from selenium.webdriver.chrome.options import Options  # Настройки
from selenium.webdriver.common.by import By  # селекторы
from selenium.webdriver.support.ui import WebDriverWait  # класс для ожидания
from selenium.webdriver.support import expected_conditions as EC
import time
import json
from bs4 import BeautifulSoup


def scrape_recipe_info(url):
    try:
        # Установка опций браузера
        options = webdriver.ChromeOptions()
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        options.add_argument(f"user-agent={user_agent}")

        # Создание экземпляра браузера
        driver = webdriver.Chrome(options=options)

        # Загрузка целевой страницы
        driver.get(url)

        # Ожидание загрузки страницы
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

        # Прокрутка страницы для загрузки всего контента
        total_height = int(driver.execute_script("return document.body.scrollHeight"))

        # for i in range(1, total_height, 10):
        #     driver.execute_script(f"window.scrollTo(0, {i});")
        #     time.sleep(0.5)

        # Парсинг содержимого страницы с помощью BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Извлечение элементов HTML, содержащих нужную информацию
        recipe_info = []

        for i, x in enumerate(soup.find_all('div', {'class': 'card__title title'}), 1):
            title = x.text.strip()
            recipe_info.append({'id': i, 'title': title})


        for i, x in enumerate(soup.find_all('div', {'class': 'text-icon text-icon_views'})):
            views = x.text.strip()
            recipe_info[i]['views'] = views


        for i, x in enumerate(soup.find_all('div', {'class': 'person__name'})[1:]):
            author = x.text.strip()
            recipe_info[i]['author'] = author

        # Сохранение извлеченных данных в файл JSON

        with open('recipe_info.json', 'w', encoding='utf-8') as f:
            json.dump(recipe_info, f, ensure_ascii=False, indent=4)

            # Закрытие браузера
        driver.quit()

    except Exception as e:
        print(f'Произошла ошибка: {e}')

    # Запуск функции скрейпинга


scrape_recipe_info('https://www.edimdoma.ru/video_retsepty')
