#2. Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа).
# Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.

#Будем получать информацию с last.fm

import requests, json

def lastfm_get(payload):

    headers = {'user-agent': 'Boris Mukhin'}
    url = 'https://ws.audioscrobbler.com/2.0/'

    payload['api_key'] = 'a0460860e28c2efaa078e8a8f6182801'
    payload['format'] = 'json'

    response = requests.get(url, headers=headers, params=payload)
    return response


#Используем метод artist.getTopTags, для получения топа тегов исполнителя
r = lastfm_get({
    'method': 'artist.getTopTags',
    'artist':  'Slayer'
})

#Получим топ 6 тегов для группы 'Slayer'
tags = [t['name'] for t in r.json()['toptags']['tag'][:6]]
print(tags)

with open('slayer_tags.json', 'w') as outfile:
    json.dump(tags, outfile)