# Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы) с сайтов Superjob и HH.
# Приложение должно анализировать несколько страниц сайта (также вводим через input или аргументы). Получившийся список должен содержать в себе минимум:
# Наименование вакансии.
# Предлагаемую зарплату (отдельно минимальную и максимальную).
# Ссылку на саму вакансию.
# Сайт, откуда собрана вакансия



from bs4 import BeautifulSoup
import lxml
import pandas as pd
import requests
from fake_headers import Headers
import re


headers = Headers(headers=True).generate()

def hh_parser(vacancy='analitik', pages=3):
    data = []
    for i in range(pages):
        url = 'https://spb.hh.ru/vacancies/{}?page={}'.format(vacancy, i)
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        vacancy_data = soup.findAll('div', class_='vacancy-serp-item')


        for i in vacancy_data:
            name = i.find('a', class_='bloko-link').text
            link = i.find('a', class_='bloko-link')['href']

            salary = i.find('div', class_='vacancy-serp-item__sidebar').text
            if not salary:
                min = None
                max = None
            else:
                salary = re.split(r'\s|-', salary)
                if salary[0] == 'от':
                    min = salary[1] + salary[2]
                    max = None
                elif salary[0] == 'до':
                    min = None
                    max = salary[1] + salary[2]
                else:
                    min = salary[0] + salary[1]
                    max = salary[3] + salary[4]

            data.append({
                'Vacancy name ': name,
                'Min salary': min,
                'Max salary': max,
                'URL': link
            })
    return data



def s_job_parser(vacancy='analitik', pages=2):
    data = []
    for i in range(pages):
        url = 'https://spb.superjob.ru/vakansii/{}.html?page={}'.format(vacancy, pages)
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        vacancy_data = soup.find_all('div', {'class': 'f-test-vacancy-item'})


        for i in vacancy_data:
            name = i.find('a').text
            link = 'https://spb.superjob.ru' + i.find('a')['href']

            salary = i.find('span', class_='_1h3Zg _2Wp8I _2rfUm _2hCDz _2ZsgW').text


            if salary == 'По договорённости':
                min = max = None
            else:
                salary = re.split(r'\s|-', salary)
                if salary[0] == 'от':
                    min = salary[1] + salary[2]
                    max = None
                elif salary[0] == 'до':
                    min = None
                    max = salary[1] + salary[2]
                elif '-' not in salary:
                    min = max = salary[0] + salary[1]
                else:
                    min = salary[0] + salary[1]
                    max = salary[3] + salary[4]

            data.append({
                    'Vacancy name ': name,
                    'Min salary': min,
                    'Max salary': max,
                    'URL': link
                })
        return data


hh_s_job_data = hh_parser() + s_job_parser()
df = pd.DataFrame(hh_s_job_data)
print(df)
