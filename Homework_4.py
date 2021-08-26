import requests
from lxml import html
from pymongo import MongoClient
from pprint import pprint

#1. Написать приложение, которое собирает основные новости с сайта на выбор lenta.ru, news.mail.ru, yandex-новости.
# Для парсинга использовать XPath. Структура данных должна содержать:
    # название источника;
    # наименование новости;
    # ссылку на новость;
    # дата публикации.
#2. Сложить собранные данные в БД

def news_mail_scraper():
    client = MongoClient('localhost', 27017)
    db = client['world_news']
    collection = db['news']

    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/91.0.4472.164 YaBrowser/21.6.4.786 Yowser/2.5 Safari/537.36'
            }
    url = 'https://news.mail.ru/'

    response = requests.get(url, headers=header)
    root = html.fromstring(response.text)
    links = root.xpath('//td[@class]/div/a/@href | //ul[@data-module="TrackBlocks"]/li[@class="list__item"]/a/@href')

    for i in links:
        dict_for_news = {}
        source_xpath = '//span[@class="note"]/a/span[@class="link__text"]/text()'
        name_xpath = '//h1[@class="hdr__inner"]/text()'
        time_xpath = '//span[@datetime]/@datetime'

        response = requests.get(i, headers=header)
        root = html.fromstring(response.text)

        source = root.xpath(source_xpath)
        name = root.xpath(name_xpath)
        date = root.xpath(time_xpath)

        dict_for_news['source'] = source[0]
        dict_for_news['name'] = name[0]
        dict_for_news['url'] = i
        dict_for_news['date'] = date[0]

        collection.update_one({'url': i}, {'$set': dict_for_news}, upsert=True)
        # pprint(dict_for_news)


news_mail_scraper()
