# Выполнить скрейпинг данных в веб-сайта http://books.toscrape.com/ и извлечь информацию о всех книгах на сайте
# во всех категориях: название, цену, количество товара в наличии (In stock (19 available)) в формате integer, описание.
# Затем сохранить эту информацию в JSON-файле.
import urllib.parse
import requests
import json
from bs4 import BeautifulSoup
from pathlib import Path
import re


# Функция получения ссылок всех страниц(книг) сайта
def get_books_links(url, books_links):
    # запрос страницы и парсинг
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # собираем ссылки
    while True:
        for ingredient in soup.find_all('li', ('class', 'col-xs-6 col-sm-4 col-md-3 col-lg-3')):
            try:
                link = ingredient.find('a').get('href')
            except:
                link = None
            if (link):
                books_links.append(urllib.parse.urljoin(url, link))
        # ищем следущие страницы
        next = soup.find('li', ('class', 'next'))
        try:
            next_page = urllib.parse.urljoin(url, next.find('a').get('href'))
        except:
            next_page = None
        if next_page:
            # собираем ссылки со следующич страниц
            get_books_links(next_page, books_links)
        break


# Функция собирает данные о книгах по ссылкам
def get_books_data(book_links):
    data = []
    index = 1
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}
    for link in books_links:
        response = requests.get(link, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        book = {}
        book['index'] = index
        index += 1
        # Ищем имя
        try:
            name = soup.find('div', ('class', 'col-sm-6 product_main')).find('h1').text
        except:
            name = ''
        book['name'] = name
        # Ищем цену
        try:
            price = float(soup.find('div', ('class', 'col-sm-6 product_main')).find('p', ('class', 'price_color')).text[1:])
        except:
            price = ''
        book['price'] = price
        # Ищем остаток
        try:
            stock = soup.find('div', ('class', 'col-sm-6 product_main')).find('p', (
                'class', 'instock availability')).text.strip()
            in_stock = int(re.sub('[^0-9]', '', stock))
        except:
            in_stock = ''
        book['in_stock'] = in_stock
        # Ищем категорию
        try:
            category = soup.find_all('li')[2].text.strip()
        except:
            category = ''
        book['category'] = category
        print(book) #для визуализации процесса оставила
        data.append(book)
    return data


# Функция сохранения данных в json
def save_to_json(data, path: Path):
    with open(path, 'w') as file:
        json.dump(data, file, indent=4)


if __name__ == "__main__":
    books_links = []
    get_books_links("http://books.toscrape.com/", books_links)
    save_to_json(books_links, Path('books_links.json'))
    data = get_books_data(books_links)
    save_to_json(data, Path('books_data.json'))

