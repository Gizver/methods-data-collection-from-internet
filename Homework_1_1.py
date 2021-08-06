#1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
# сохранить JSON-вывод в файле *.json.

import requests, json

url = 'https://api.github.com/users/Gizver/repos'

response = requests.get(url).json()

data = []

for item in response:
    data.append(item['name'])

with open('data.json', 'w') as outfile:
    json.dump(data, outfile)


