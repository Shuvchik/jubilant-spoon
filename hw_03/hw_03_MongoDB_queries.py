from pymongo import MongoClient
import json

# Подключение к серверу MongoDB
client = MongoClient('mongodb://localhost:27017/')

# Выбор базы данных и коллекции
db = client["books"]
collection = db["books_data"]

# вывод первой записи в коллекции
first_book = collection.find()[0]
print(f"Первая запись: {first_book}")

# Получение количества документов в коллекции с помощью функции count_documents()
count_documents = collection.count_documents({})
print(f"Количество записей в базе данных: {count_documents}")

# - Отфильтруйте документы по критерию "category", равному ""Mystery""
count_mystery = collection.count_documents(filter={"category": "Mystery"})
print(f"Количество книг в категории 'Mystery': {count_mystery}")

# - Используйте проекцию для отображения только полей 'name' и 'price' для документов с 'category' равным "Business".
# Отсортируйте их по цене по возрастанию
print("Книги в категории бизнесс:")
business_books = collection.find(projection={"_id": 0,'name': 1, 'price': 1}, filter={"category": "Business"})
print(*sorted(business_books, key = lambda x: x["price"]),sep='\n')

# - Используйте операторы $lte и $gt для подсчета количества документов с "price" меньше или равно 50 и больше 50,
# соответственно.
cheaper_50 = collection.count_documents(filter={"price" :{"$lte" : 50}})
print(f"Количество книг дешевле или равно по стоимости 50: {cheaper_50}")
expensive_50 = collection.count_documents(filter={"price" :{"$gt" : 50}})
print(f"Количество книг длороже 50: {expensive_50}")

# - Используйте оператор $regex для подсчета количества документов, содержащих слово "women" в поле "name",
# игнорируя регистр.
count_women = collection.count_documents(filter={'name':{'$regex' : 'women', '$options': 'i'}})
print(f"Количество книг, содержащих слово 'women': {count_women}")

# - Используйте оператор $in для подсчета количества документов, в которых "category" либо "Sequential Art", либо "Music".
art_music_category = collection.count_documents(filter={"category" :{"$in" : ["Sequential Art", "Music"]}})
print(f"Количество книг в категориях Sequential_Art и Music: {art_music_category}")

# - Используйте оператор $all для подсчета количества документов, в которых "category" и "Sequential Art", и "Music",
art_music= collection.count_documents(filter={'name': {'$all' : ["Sequential Art", "Music"]}})
print(f"Количество книг в категориях Sequential_Art и Music: {art_music}")

# - Используйте оператор $ne для подсчета количества документов, у которых "in_stock" не равно 5.

ne_5 = collection.count_documents(filter={'in_stock':{'$ne' : 5}})
print(f"Количество книг, которых в стоке не 5 шт  равно: {ne_5}")