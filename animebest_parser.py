import requests
from bs4 import BeautifulSoup
import csv

URL = 'https://animebestnew.org/'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 '
                  'YaBrowser/20.4.1.225 Yowser/2.5 Yptp/1.23 Safari/537.36',
    'accept': '*/*'}
FILE = 'anime.csv'

def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='shortstory')
    anime = []
    for el in items:
        anime.append({
            'title': el.find('h2').get_text(),
            'categories': el.find('div', class_='animbest-cat radius-2').get_text().replace('\n', '').replace(
                'Категории: ', ''),
            'description': el.find('div', class_='finfo-text').get_text(strip=True).replace('\n', '').replace(
                'Описание:', ''),
            'link': el.find('a').get('href')
        })
    return anime


def safe_parser(file, path):
    with open(path, 'w', newline='') as item:
        writer = csv.writer(item, delimiter=';')
        writer.writerow(['Название', 'Категории', 'Описание', 'Ссылка'])
        for i in file:
            writer.writerow([i['title'], i['categories'], i['description'], i['link']])


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        anime = []
        page = int(input('Введите нужное количество страниц:'))
        for item in range(1, page + 1):
            print(f'Парсинг страницы {item} из {page} ...')
            html = get_html(URL, params={'page': item})
            anime.extend(get_content(html.text))
        safe_parser(anime, FILE)
        print('Парсинг завершён!')
    else:
        print('Error')


parse()
