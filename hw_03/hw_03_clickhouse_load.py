from clickhouse_driver import Client
import json

# Подключение к серверу ClickHouse
client = Client('localhost')

# Создание базы данных (если она не существует)
client.execute('CREATE DATABASE IF NOT EXISTS books')

# Создание таблицы
client.execute('DROP TABLE IF EXISTS books.books_data')
client.execute('''
CREATE TABLE books.books_data (
id Int64,
name String,
price Double,
in_stock Int32,
category String
) ENGINE = MergeTree()
ORDER BY id
''')

print("Таблица создана успешно.")

# Считывание json
with open('books_data.json', 'r') as file:
    books = json.load(file)

# Вставка данных в таблицу

for book in books:
    # print(book['index'])  # для визуализации
    # Определение id
    id = book['index']

    client.execute('''
    INSERT INTO books.books_data(
    id, name, price, in_stock, category) VALUES''',
                   [(  id,
                       book['name'] or "",
                       book['price'] or "",
                       book['in_stock'] or "",
                       book['category'] or "")])

print("Данные введены успешно.")

# Проверка успешности вставки
print(*client.execute("SELECT * FROM books.books_data")[0])
