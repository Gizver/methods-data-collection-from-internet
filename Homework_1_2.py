#2. Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа).
# Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.

#Будем получать информацию с last.fm

import requests, json

def lastfm_get(payload):

    headers = {'USER-AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.135 YaBrowser/21.6.2.855 Yowser/2.5 Safari/537.36'}
    url = 'https://ws.audioscrobbler.com/2.0/'

    payload['api_key'] = 'a0460860e28c2efaa078e8a8f6182801'
    payload['format'] = 'json'

    response = requests.get(url, headers=headers, params=payload)
    return response


#Используем метод artist.getTopTags, для получения топа тегов исполнителя
top_teg = lastfm_get({
    'method': 'artist.getTopTags',
    'artist':  'Slayer'
})

#Получим топ 6 тегов для группы 'Slayer'
tags = [t['name'] for t in top_teg.json()['toptags']['tag'][:6]]
print(tags)

with open('slayer_tags.json', 'w') as outfile:
    json.dump(tags, outfile)
