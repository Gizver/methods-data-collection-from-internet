from pymongo import MongoClient
import json

# 1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию, записывающую собранные вакансии в созданную БД.

client = MongoClient('localhost', 27017)

db = client['vacancy']

collection = db['python']

# В data.json хранятся собранные вакансии (ДЗ №2)
with open('data.json', encoding='UTF-8') as f:
    file_data = json.load(f)

collection.insert_many(file_data)

# 2. Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой суммы.

def find_document(collection, salary, currency):

    results = collection.find({'$or': [{'Min salary': {'$gt': salary}}, {'Max salary': {'$gt': salary}}]}, {'Сurrency':currency})
    return [r for r in results]



result = find_document(collection, 90000, 'руб.')
print(result)


# 3. Написать функцию, которая будет добавлять в вашу базу данных только новые вакансии с сайта.

def new_vacancy(data):
    for el in data:
        collection.update_one({'URL': el['URL']}, {'$set': el}, upsert=True)

new_vacancy(file_data)
