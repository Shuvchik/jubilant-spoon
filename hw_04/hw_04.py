# https://drive.google.com/drive/folders/1wsHF1tHjkPTPsThcVqnLjsVoEc9JYj45?usp=drive_link
# Урок 4. Парсинг HTML. XPath
# Выберите веб-сайт с табличными данными, который вас интересует.
# Напишите код Python, использующий библиотеку requests для отправки HTTP GET-запроса на сайт и получения HTML-содержимого страницы.
# Выполните парсинг содержимого HTML с помощью библиотеки lxml, чтобы извлечь данные из таблицы.
# Сохраните извлеченные данные в CSV-файл с помощью модуля csv.
#
# Ваш код должен включать следующее:
#
# Строку агента пользователя в заголовке HTTP-запроса, чтобы имитировать веб-браузер и избежать блокировки сервером.
# Выражения XPath для выбора элементов данных таблицы и извлечения их содержимого.
# Обработка ошибок для случаев, когда данные не имеют ожидаемого формата.
# Комментарии для объяснения цели и логики кода.
#
# Примечание: Пожалуйста, не забывайте соблюдать этические и юридические нормы при веб-скреппинге.

from lxml import html
import requests
import pandas as pd

#Функция для обработки исключений
def exception_handling (row, path):
    try:
        result = row.xpath(path)[0].strip()
    except:
        result = "не определено"
        #у них написано N/A,  я специально поменяла на не определено, что бы было видно, что исключения ловятся
    return result

#Функция сканирования таблицы
def scrapy_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}
    response = requests.get(url, headers=headers)
    tree = html.fromstring(response.content)

    titles = list(map(str.strip, tree.xpath('.//thead/tr/th/text()')))
    table_rows = tree.xpath('//*[@id="list-res-table"]/div[1]/table/tbody/tr')
    # print(table_rows[0])
    data = []
    for row in table_rows:
        data.append({
            titles[0]: exception_handling(row, ".//td[1]/a/text()"),
            titles[1]: exception_handling(row, ".//td[2]/text()"),
            titles[2]: exception_handling(row, ".//td[3]/fin-streamer/text()"),
            titles[3]: exception_handling(row, ".//td[4]/fin-streamer/text()"),
            titles[4]: exception_handling(row, ".//td[5]/fin-streamer/span/text()"),
            titles[5]: exception_handling(row, ".//td[6]/fin-streamer/span/text()"),
            titles[6]: exception_handling(row, ".//td[7]/fin-streamer/text()"),
            titles[7]: exception_handling(row, ".//td[8]/fin-streamer/text()"),
        })
        # time.sleep(2)
    return data

#Функция сохранения данных в csv
def save_to_csv(data):
    df = pd.DataFrame(data)
    df.to_csv('trending_tickers.csv', index=False)

#Главная функция
def main():
    url = 'https://finance.yahoo.com/trending-tickers/'
    data = scrapy_data(url)
    save_to_csv(data)
    print(*data, sep='\n')


if __name__ == '__main__':
    main()
