# Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы) с сайтов Superjob и HH.
# Приложение должно анализировать несколько страниц сайта (также вводим через input или аргументы). Получившийся список должен содержать в себе минимум:
# Наименование вакансии.
# Предлагаемую зарплату (отдельно минимальную и максимальную).
# Ссылку на саму вакансию.
# Сайт, откуда собрана вакансия



from bs4 import BeautifulSoup as bs
import requests
import re
from pprint import pprint
import json

my_header = {'USER-AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.135 YaBrowser/21.6.2.855 Yowser/2.5 Safari/537.36'}


vacancy = 'python'

params = {
        'text': vacancy,
        'search_field': 'name'
    }

url = 'https://hh.ru/search/vacancy'
response = requests.get(url, params=params, headers=my_header)
soup = bs(response.text, 'html.parser')

#сделаем вариант со сбором инфы с первой по последнюю страницу

next_page_blok = soup.find('div', {'data-qa': 'pager-block'}) #находим блок с кнопками перехода на следующие страницы

#подтверждаем его существование
if next_page_blok:
    last_page_number = int(next_page_blok.find_all('a', {'class':'bloko-button', 'data-qa': 'pager-page'})[-1].getText())  #находим последнюю возможную страницу

else:
    last_page_number = 1 # если такого блока нет, то страница всего одна
data = []
#перебираем страницы и собираем их код
for page in range(0, last_page_number):

    params['page'] = page
    response = requests.get(url, params, headers=my_header)


    soup_page = bs(response.text, 'html.parser')
    vacancy_data = soup_page.findAll('div', class_='vacancy-serp-item')



    for i in vacancy_data:
        name = i.find('a', class_='bloko-link').text
        link = i.find('a', class_='bloko-link')['href']

        #создаем словарь с зарплатами обрабатывая варианты с отсутствием какой-либо инфы
        salary = i.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
        if not salary:
            min = None
            max = None
            money_name = None
        else:
            salary = salary.text
            salary = re.split(r'\s|-', salary)
#так как split разделил зарплаты по пробелу, то чтобы не возиться с регулярками стал проверять некоторые элементы списка на то, число они или нет
            if salary[0] == 'от':
                if salary[2].isnumeric():
                    min = int(salary[1] + salary[2])
                else:
                    min = int(salary[1])

                max = None

            elif salary[0] == 'до':
                min = None

                if salary[2].isnumeric():
                    max = int(salary[1] + salary[2])
                else:
                    max = int(salary[1])

            else:
                if salary[1].isnumeric():
                    min = int(salary[0] + salary[1])
                else:
                    min = int(salary[0])
                if salary[4] .isnumeric():
                    max = int(salary[3] + salary[4])
                else:
                    max = int(salary[3])


            money_name = salary[-1]


        data.append({
            'Vacancy name ': name,
            'Min salary': min,
            'Max salary': max,
            'Сurrency': money_name,
            'URL': link
        })

pprint(data)
print(f'С {last_page_number} страниц было собрано {len(data)} вакансий')

with open('hh_vacansy.json', 'w', encoding='UTF-8') as outfile:
    json.dump(data, outfile, ensure_ascii=False, separators=(',', ': '))
