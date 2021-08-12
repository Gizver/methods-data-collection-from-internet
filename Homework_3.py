from pymongo import MongoClient
import json

# 1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию, записывающую собранные вакансии в созданную БД.

client = MongoClient('localhost', 27017)

db = client['vacancy']

collection = db['analitik']

# В data.json хранятся собранные вакансии (ДЗ №2)
with open('data.json') as f:
    file_data = json.load(f)

collection.insert_many(file_data)

# 2. Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой суммы.

def find_document(collection, salary):

    results = collection.find({'$or': [{'Min salary': {'$gt': salary}}, {'Max salary': {'$gt': salary}}]})
    return [r for r in results]



result = find_document(collection, 90000)
print(result)


# 3. Написать функцию, которая будет добавлять в вашу базу данных только новые вакансии с сайта.

def new_vacancy(data):

    # Соберем список ссылок на вакансии из нашей БД
    url_list = []

    res = collection.find({})

    for r in res:
        url_list.append(r['URL'])


    # Выгрузим информацию о вакансиях из json файла
    with open('{}.json'.format(data)) as f:
        file_data = json.load(f)


    new_url = []
    for el in file_data:
        if el['URL'] not in url_list:
            new_url.append(el)

    collection.insert_many(new_url)
    print(f'Было добавлено {len(new_url)} записи')


new_vacancy('data')