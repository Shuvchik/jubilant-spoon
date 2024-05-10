# Загрузите данные который вы получили на предыдущем уроке путем скрейпинга сайта с помощью
# Buautiful Soup в MongoDB и создайте базу данных и коллекции для их хранения.

from pymongo import MongoClient
import json
# Подключение к серверу MongoDB
client = MongoClient('mongodb://localhost:27017/')

# Выбор базы данных и коллекции
db = client["books"]
collection = db["books_data"]
# Чтение файла JSON
with open("books_data.json", "r") as file:
    data = json.load(file)

# Функция разделения данных на более мелкие фрагменты (здесь на особо нужно, написала для практики)
def get_chunks(data, chunk_size):
    for i in range(0, len(data), chunk_size):
        yield data[i:i+chunk_size]

# Вставка фрагментов в коллекцию MongoDB
for chunk in get_chunks(data, chunk_size=50):
    collection.insert_many(chunk)

print("Данные успешно вставлены.")