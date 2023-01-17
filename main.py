from bs4 import BeautifulSoup
import lxml
import requests
from fake_headers import Headers
from pprint import pprint
import os
from task_2 import logger

HH = 'https://spb.hh.ru'

KEYWORDS = ['Python', 'Django', 'Flask']
REQUEST_NUMBER = {'Moscow': 1, 'St_Peterburg': 2}
HEADERS = Headers(os='win', browser='chrome')

path = 'main_py_task_3.log'
if os.path.exists(path):
    os.remove(path)


@logger(path)
def get_url():
    req_text = f'NAME:{KEYWORDS[0]} AND DESCRIPTION:({KEYWORDS[1]} AND {KEYWORDS[2]})'
    req_area = f'&area={REQUEST_NUMBER["Moscow"]}&area={REQUEST_NUMBER["St_Peterburg"]}'
    url = f'{HH}/search/vacancy?text={req_text}{req_area}&search_field=description'
    return url


@logger(path)
def get_page(url):
    headers = HEADERS.generate()
    return requests.get(url, headers=headers)


@logger(path)
def bs_page(page):
    bs_page_soup = BeautifulSoup(page, features='lxml')
    return bs_page_soup


@logger(path)
def parsing_page(vacancy):
    link = vacancy.find("a")["href"]
    list_bloko_header_section_3 = vacancy.find_all(
        class_="bloko-header-section-3")
    salary = 'не указана'
    if len(list_bloko_header_section_3) > 1:
        salary = list_bloko_header_section_3[1].text
    company = vacancy.find(class_="bloko-link bloko-link_kind-tertiary").text
    list_bloko_text = vacancy.find_all(class_="bloko-text")
    city = list_bloko_text[1].text.split(',')[0]
    return {
        "link": link,
        "salary": salary.replace("\u202f", " "),
        "company": company.replace("\xa0", " "),
        "city": city
    }


@logger(path)
def main():

    url = get_url()
    received_page = get_page(url)
    html_text = received_page.text
    parse_page = bs_page(html_text)
    vacancies = parse_page.find_all(class_="serp-item")
    for vacancy in vacancies:
        vacancy_details = parsing_page(vacancy)
        pprint(vacancy_details)


if __name__ == "__main__":
    main()
