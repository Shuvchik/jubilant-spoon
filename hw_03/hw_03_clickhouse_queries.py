from clickhouse_driver import Client
import pandas as pd

# Подключение к серверу ClickHouse
client = Client('localhost')

# 1. Выполнение базового запроса для получения всех записей из таблицы 'books_data'
result = client.execute('SELECT * FROM books.books_data')
df = pd.DataFrame(result, columns=['id', 'name', 'price', 'in_stock', 'category'])
# Вывод первых пяти записей DataFrame для предварительного просмотра
print(df.head(), '\n')

# 2. Фильтрация записей на основе критериев
# 2.1. Равенство: Получение записей с category, равным 'Travel'
travel = client.execute("SELECT * FROM books.books_data where category = 'Travel'")
print(f'Количество книг в категории Travel: {pd.DataFrame(travel).shape[0]}.', '\n')

# 2.2. Диапазон: Выборка записей с ценой книги между 45 и 55
LOW_PRICE = 5
HIGH_PRICE = 10
price_5_10 = client.execute(f"SELECT * FROM books.books_data where price BETWEEN {LOW_PRICE} AND {HIGH_PRICE}")
print(f'Количество книг  ценой от {LOW_PRICE} до {HIGH_PRICE} {len(price_5_10)}.')
print(*price_5_10, sep='\n')

# 3. Сортировка записей на основе одного или нескольких полей
# 3.1. Сортировка записей по цене книги в порядке убывания
sorted_books = client.execute('SELECT * FROM books.books_data ORDER BY price DESC')
df_sorted = pd.DataFrame(sorted_books, columns=df.columns)
# Вывод первых пяти записей DataFrame для предварительного просмотра
print('\n', "Пять самых дорогих книг:", '\n', df_sorted.head(), '\n')

# 3.2. Сортировка записей по току в порядке убывания и по цене в порядке возрастания
multisorted_books = client.execute(
    "SELECT id, name, price, in_stock FROM books.books_data ORDER BY in_stock DESC, price ASC")
df_multisorted = pd.DataFrame(multisorted_books, columns=['id', 'name', 'price', 'in_stock'])
print("Больше всего шт в стоке:", '\n', df_multisorted.head(7), '\n')

# 4. Агрегирование записей с помощью таких функций, как count, sum и avg.
# 4.1. Подсчет общего количества записей
count = client.execute('SELECT COUNT(*) FROM books.books_data')
print(f"В базе данных записано {count[0][0]} книг.", '\n')

# 4.2. Подсчет количества записей в каждой категории,  так же средней цены книги в категории
books_by_category = client.execute(
    """SELECT category, COUNT(*), AVG(price) 
    FROM books.books_data 
    GROUP BY category 
    ORDER BY COUNT(*) DESC""")
df_category = pd.DataFrame(books_by_category, columns=['category', 'books_count', 'avg_price'])
print("Количество книг и их средняя цена по категориям : ", '\n', df_category)
