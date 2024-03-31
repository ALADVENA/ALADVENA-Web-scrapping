import requests
from bs4 import BeautifulSoup
import fake_headers
import json

def gen_headers():
    headers_gen = fake_headers.Headers(os="win", browser="chrome")
    return headers_gen.generate()


main_response = requests.get('https://spb.hh.ru/search/vacancy?text=python+django+flask&area=1&area=2',
                             headers=gen_headers())
main_html_data = main_response.text
main_soup = BeautifulSoup(main_html_data, "lxml")

vacancy_list_tag = main_soup.find('div', id='a11y-main-content')
parsed_data = []

for vacancy in vacancy_list_tag.find_all('div', class_='serp-item'):
    url_tag = vacancy.find('a', class_='bloko-link')
    title_tag = url_tag.find('span', class_='serp-item__title')
    salary_tag = vacancy.find('span', class_='bloko-header-section-2')
    company_name_tag = vacancy.find('a', class_='bloko-link bloko-link_kind-tertiary')
    city_tag = vacancy.find('div', {'data-qa': 'vacancy-serp__vacancy-address'})

    header = title_tag.text.strip()
    link = url_tag['href']
    company_name = company_name_tag.text.replace('\xa0', ' ')
    location = city_tag.text.split(', ')[0]
    if salary_tag == None:
        salary = 'ЗП не указана'
    else:
        salary = salary_tag.text.replace('\u202f', ' ')

    parsed_data.append({
        'Название вакансии': header,
        'Ссылка на вакансию': link,
        'Работодатель': company_name,
        'Город': location,
        'ЗП': salary
    })
with open('hh_data.json', 'w', encoding='utf-8') as f:
    json.dump(parsed_data, f, ensure_ascii=False, indent=2)