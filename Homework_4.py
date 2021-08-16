import requests
from lxml import html
import re
import datetime
from pymongo import MongoClient

# Написать приложение, которое собирает основные новости с сайтов mail.ru, lenta.ru, yandex-новости.
# Для парсинга использовать XPath. Структура данных должна содержать:
# название источника;
# наименование новости;
# ссылку на новость;
# дата публикации.

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 YaBrowser/20.8.3.115 Yowser/2.5 Safari/537.36'}

# news.mail.ru
def mail_news_parcer():
    url = 'https://news.mail.ru/'
    xpath_news_text = '//div[7]/div[2]/div[1]/div/div[2]/ul/li/a/text()'
    response = requests.get(url, headers=header)
    root = html.fromstring(response.text)
    text = root.xpath(xpath_news_text)
    text = [i.replace('\xa0', ' ').rstrip() for i in text]

    xpath_news_link = '//div[7]/div[2]/div[1]/div/div[2]/ul/li/a/@href'
    link = root.xpath(xpath_news_link)

    xpath_news_name = '/html/body/div[7]/div[2]/div[1]/div/div/div/div/div/div[1]/div[1]/span[2]/span/a/span/text()'
    xpath_news_date = '//div/div/div/div[1]/div[1]/span[1]/span/span/@datetime'
    date_list = []
    name_list = []
    for i in link:
        response = requests.get(i, headers=header)
        root = html.fromstring(response.text)
        date = root.xpath(xpath_news_date)
        name = root.xpath(xpath_news_name)
        date_list.extend(date)
        name_list.extend(name)

    date_list = [str(d) for d in date_list]
    formated_date = []
    for l in date_list:
        date_list = datetime.datetime.strptime(l, '%Y-%m-%dT%H:%M:%S+03:00').strftime('%H:%M, %d-%m-%Y')
        formated_date.append(date_list)

    keys = ('title', 'date', 'sourse', 'link')
    result = []
    for item in list(zip(text, formated_date, name_list, link)):
        dictionary = {}
        for key, value in zip(keys, item):
            dictionary[key] = value
        result.append(dictionary)

    return result


def lenta_news_parcer():
    url = 'https://lenta.ru/'
    xpath_news_text = '//*[@id="root"]/section[2]/div/div/div[1]/section[1]/div[1]/div[1]/h2/a/text() | \
        //*[@id="root"]/section[2]/div/div/div[1]/section[1]/div[1]/div/a/text() | \
        //*[@id="root"]/section[2]/div/div/div[1]/section[1]/div[2]/div/a[not(contains(text(),"Больше новостей"))]/text()'

    response = requests.get(url, headers=header)
    root = html.fromstring(response.text)

    # Описание статьи
    text = root.xpath(xpath_news_text)
    text = [i.replace('\xa0', ' ').rstrip() for i in text]

    xpath_news_link = '//*[@id="root"]/section[2]/div/div/div[1]/section[1]/div[1]/div/*/@href | \
      //*[@id="root"]/section[2]/div/div/div[1]/section[1]/div[2]/div/a[not(contains(text(),"Больше новостей"))]/@href'
    link = root.xpath(xpath_news_link)
    link = [(url + i) for i in link]

    # Дата
    xpath_time = '//*[@id="root"]/section[2]/div/div/div[1]/section[1]/div[1]/div[1]/h2/a/time/@datetime | \
                //*[@id="root"]/section[2]/div/div/div[1]/section[1]/div[1]/div/a/time/@datetime | \
                //*[@id="root"]/section[2]/div/div/div[1]/section[1]/div[2]/div/a/time/@datetime'

    date_time = root.xpath(xpath_time)
    date_time = [str(d) for d in date_time]  # Дата в str для datetime.datetime.strptime

    # Приводим дату к единому образцу для всех сайтов
    month_list = {'января': '01', 'февраля': '02', 'марта': '03', 'апреля': '04', 'мая': '05', 'июня': '06',
                  'июля': '07', 'августа': '08', 'сентября': '09', 'октября': '10', 'ноября': '11', 'декабря': '12'}

    numeric_date = []
    for date in date_time:
        date = date.split()
        numeric_date.append(date)

    string_numeric_date = []
    for i in numeric_date:
        i[2] = month_list[i[2]]
        string_numeric_date.append(' '.join(i))

    final_date = []
    for date in string_numeric_date:
        date_time_obj = datetime.datetime.strptime(date, '%H:%M, %d %m %Y').strftime('%H:%M, %d-%m-%Y')
        final_date.append(date_time_obj)

    # Имя ресурса
    name = []
    for i in link:
        i = re.search(r'//(.+?)/', i)
        name.append(i[0].replace('/', ''))

    # Оформляем в словарь
    keys = ('title', 'date', 'sourse', 'link')
    result = []
    for item in list(zip(text, final_date, name, link)):
        dictionary = {}
        for key, value in zip(keys, item):
            dictionary[key] = value
        result.append(dictionary)
    return result


def yandex_parcer():
    from datetime import datetime
    url = 'https://yandex.ru/news/'
    xpath_news_text = '//*[@id="neo-page"]/div/div[2]/div/div[1]/div[1]/div[1]/article/div[2]/a/h2/text() | \
                      //*[@id="neo-page"]/div/div[2]/div/div[1]/div[1]/div/article/div/div/a/h2[@class="mg-card__title"]/text()'

    response = requests.get(url, headers=header)
    root = html.fromstring(response.text)
    text = root.xpath(xpath_news_text)
    text = [i.replace('\xa0', ' ').rstrip() for i in text]

    xpath_news_link = '//*[@id="neo-page"]/div/div[2]/div/div[1]/div/div/article/div/a/@href | \
       //*[@id="neo-page"]/div/div[2]/div/div[1]/div[1]/div/article/div/div/a/@href'
    link = root.xpath(xpath_news_link)

    xpath_news_name = '//*[@id="neo-page"]/div/div[2]/div/div[1]/div[1]/div[1]/article/div[2]/div[2]/div[1]/div/span[1]/a/text() | \
                        //div[1]/div/article/div[3]/div[1]/div/span[1]/a/text()'

    name = root.xpath(xpath_news_name)

    xtime_news_date = '//*[@id="neo-page"]/div/div[2]/div/div[1]/div[1]/div[1]/article/div[2]/div[2]/div[1]/div/span[2]/text() | \
                       //*[@id="neo-page"]/div/div[2]/div/div[1]/div[1]/div/article/div/div/div/span/text()'

    date = root.xpath(xtime_news_date)
    date = [str(d) for d in date]

    now = datetime.now()
    full_date = []
    for i in date:
        full_date.append(i + f', {now.strftime("%Y-%m-%d")}')

    # Оформляем в словарь
    keys = ('title', 'date', 'sourse', 'link')
    result = []
    for item in list(zip(text, full_date, name, link)):
        dictionary = {}
        for key, value in zip(keys, item):
            dictionary[key] = value
        result.append(dictionary)

    return result

full_data = mail_news_parcer() + lenta_news_parcer() + yandex_parcer()
# print(full_data)

MONGO_URI = 'mongodb://localhost:27017/'
MONGO_DATABASE = 'world_news'
client = MongoClient(MONGO_URI)
mongo_base = client[MONGO_DATABASE]

collection = mongo_base['news']

for el in full_data:
    collection.update_one({'link': el['link']}, {'$set': el}, upsert=True)
