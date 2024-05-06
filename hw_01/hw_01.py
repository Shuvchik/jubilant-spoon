import json
import requests
import pandas as pd

# Ваши учетные данные API
client_id = "__"
client_secret = "__"

# Конечная точка API
endpoint = "https://api.foursquare.com/v3/places/search"

# Определение параметров для запроса API
category = input("Введите категорию поиска: ")
params = {
    "client_id": client_id,
    "client_secret": client_secret,
    "query": category
}

headers = {
"Accept": "application/json",
"Authorization": "fsq3V3AFHzvqod5PVkb9j5ptfec29VfLTGG2XbHrQEGC8bI="
}

# Отправка запроса API и получение ответа
response = requests.get(endpoint, params=params, headers=headers)

if response.status_code==200:
    data = json.loads(response.text)
    venues = data["results"]
    df = pd.DataFrame(columns=['id', 'name', 'adress', 'latitude', 'longitude'])
    for venue in venues:
        id = venue.get('categories')[0].get('id', 'не указано')
        address = venue.get('location', {}).get('formatted_address', 'не указанo')
        latitude = venue.get('geocodes', {}).get('main', {}).get('latitude', 'не указано')
        longitude = venue.get('geocodes', {}).get('main', {}).get('longitude', 'не указано')
        df.loc[len(df)]=[id, venue['name'], address, latitude, longitude]

df.to_csv(r'C:\GB\DataEngineer\Data_collection\HW\1\result.csv', encoding='utf-8')
print(df.head(5))