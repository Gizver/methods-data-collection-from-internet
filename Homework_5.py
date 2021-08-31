# Написать программу, которая собирает «Новинки» с сайта техники mvideo и складывает данные в БД.

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from pymongo import MongoClient
import time

client = MongoClient('localhost', 27017)
db = client['mvideo']
collection = db['new']

chrome_options = Options()
chrome_options.add_argument('start-maximized')

driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=chrome_options)
driver.get('https://www.mvideo.ru/')

new_block = driver.find_element_by_xpath("//h2[contains(text(), 'Новинки')]/../../following-sibling::div")
actions = ActionChains(driver)
actions.move_to_element(new_block).perform()

time.sleep(0.5)
next_btn = new_block.find_element_by_xpath(".//a[contains(@class, 'next-btn')]")
cls_next_btn = next_btn.get_attribute('class')

#Прокручиваем весь блок новинок, чтобы информация о них появилась в коде страницы
while cls_next_btn == 'next-btn c-btn c-btn_scroll-horizontal c-btn_icon i-icon-fl-arrow-right':
    time.sleep(0.5)
    next_btn = new_block.find_element_by_xpath(".//a[contains(@class, 'next-btn')]")
    cls_next_btn = next_btn.get_attribute('class')
    time.sleep(0.5)
    next_btn.click()


names_items = new_block.find_elements_by_xpath(".//h3[contains(@class, 'fl-product-tile-title')]")
links_items = new_block.find_elements_by_xpath(".//a[contains(@class, 'fl-product-tile-title__link')]")

names = []
links = []
# Собираем названия новинок
for i in names_items:
    name = i.get_attribute('title')
    names.append(name)
# Собираем ссылки на страницы новинок
for i in links_items:
    link = i.get_attribute('href')
    links.append(link)

# Оформляем в словарь
keys = ('name', 'link')
result = []
for item in list(zip(names, links)):
    dictionary = {}
    for key, value in zip(keys, item):
        dictionary[key] = value
    result.append(dictionary)

# Заносим в монго с проверкой на дубли
for el in result:
    collection.update_one({'link': el['link']}, {'$set': el}, upsert=True)



