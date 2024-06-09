"""
Выберите веб-сайт, который содержит информацию, представляющую интерес для извлечения данных. Это может быть новостной сайт,
платформа для электронной коммерции или любой другой сайт, который позволяет осуществлять скрейпинг (убедитесь в соблюдении
условий обслуживания сайта).
Используя Selenium, напишите сценарий для автоматизации процесса перехода на нужную страницу сайта.
Определите элементы HTML, содержащие информацию, которую вы хотите извлечь (например, заголовки статей, названия продуктов,
цены и т.д.).
Используйте BeautifulSoup для парсинга содержимого HTML и извлечения нужной информации из идентифицированных элементов.
Обработайте любые ошибки или исключения, которые могут возникнуть в процессе скрейпинга.
Протестируйте свой скрипт на различных сценариях, чтобы убедиться, что он точно извлекает нужные данные.
"""
from selenium import webdriver  # класс управления браузером
from selenium.webdriver.chrome.options import Options  # Настройки
from selenium.webdriver.common.by import By  # селекторы
from selenium.webdriver.support.ui import WebDriverWait  # класс для ожидания
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import csv

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
url = 'https://yandex.ru/video/'

# задаем опции для вебдрайвера
chrom_option = Options()
chrom_option.add_argument(f'user_agent = {user_agent}')
# создаем вебдрайвер с указанными опциями
driver = webdriver.Chrome(options=chrom_option)
# обрабатываем ошибки
try:
    # запускаем драйвер
    driver.get(url)
    # ждем пока прогрузится тело страницы
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

    # высота экрана в пикселях, если скролить во вмеря исполнения, будет больше
    size_length = driver.execute_script("return document.documentElement.scrollHeight")

    # скролинг вниз, ограничила размер страницы 50000 пикселями, иначе очень долго работает программа)
    while size_length < 50000:
        # говорим драйверу выполнить скрипт: скроль
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(2)
        # запоминаем новый размер страницы
        new_size_length = driver.execute_script("return document.documentElement.scrollHeight")
        # заменяем старый размер страницы на новый
        size_length = new_size_length
        print(size_length)
        # ищем кнопку 'еще видео'
        next_button = driver.find_element(By.XPATH, '//div[@class="NextPageButton-SpinnerContainer"]')
        # Проверка наличия следующей кнопки
        if not next_button:
            break
        # если нашли, нажимаем
        next_button.click()
        time.sleep(1)
    print(size_length)  # оставила для визуализации процесса

    #ищем элементы с видео
    videos = driver.find_elements(By.XPATH, '//div[@class="VideoSnippet-Content"]')
    #сюда будем записывать данные
    video_data=[]
    # счетчик записей
    count =1
    for video in videos:
        #находим название видео
        video_title = video.text.split('\n')[0]
        #находим дату публикации
        video_date = video.text.split('\n')[video.text.split('\n').index('дата публикации')+1]
        #находим ссылку на видео
        video_url=video.find_element(By.XPATH, './/a').get_attribute('href')
        #добавляем в список словарей
        video_data.append({'id': count,
                           'title' : video_title if video_title else 'not found',
                           'publication_date' : video_date if video_date else 'not found',
                           'url': video_url if video_url else 'not found' })
        count+=1

    #сохраняем в json
    with open('video_data.json', 'w', encoding='UTF-8') as file:
        json.dump(video_data, file, ensure_ascii=False, indent=4)

    #сохраняем в scv
    with open('video_data.csv', 'w', encoding='UTF-8') as file:
        writer = csv.DictWriter(file, fieldnames=list(video_data[0].keys()))
        writer.writeheader()
        writer.writerows(video_data)

except Exception:
    print("Ошибка.")
finally:
    driver.quit()
