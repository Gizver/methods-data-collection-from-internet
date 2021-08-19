# 1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
# сохранить JSON-вывод в файле *.json.

import requests
import json

url = 'https://api.github.com/users/Gizver/repos'
header = {'USER-AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.135 YaBrowser/21.6.2.855 Yowser/2.5 Safari/537.36'}

response = requests.get(url, headers=header).json()

data = []

for item in response:
    data.append(item['name'])

with open('data.json', 'w') as outfile:
    json.dump(data, outfile)


