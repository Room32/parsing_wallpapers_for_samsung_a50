import random
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time
import os

if not os.path.exists('content'):
    os.makedirs('content')

if os.path.exists('links.txt'):
    os.remove('links.txt')

ua = UserAgent()
headers = {
    'user-agent': ua.random
}


def find_links():
    page = 1
    while page < 19:
        url = f'https://www.setaswall.com/samsung-galaxy-a50-wallpapers/{page}/'
        try:
            response = requests.get(url=url, headers=headers, timeout=10).text
        except Exception as ex:
            print(f'There is error: {ex}')
            return

        soup = BeautifulSoup(response, 'lxml')
        pictures_list = soup.find_all('div', class_='gallery-icon portrait')

        for pic in pictures_list:
            pic_link = pic.find_next('a').get('href')
            with open('links.txt', 'a', encoding='utf-8') as file:
                file.write(pic_link + '\n')
        print(f'COMPLETE - {page}/18')
        page += 1
        time.sleep(random.randint(1, 3))


def download_every_picture():
    count = 1
    with open('links.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for i in lines:
            new_i = i.strip()

            try:
                response_2 = requests.get(url=new_i, headers=headers, timeout=10).text
            except Exception as ex:
                print(f'Some error: {ex}')
                continue

            soup_2 = BeautifulSoup(response_2, 'lxml')
            picture_full_size_link = soup_2.find('a', class_='download').get('href')

            try:
                picture = requests.get(picture_full_size_link, headers=headers, timeout=10).content
            except Exception as ex:
                print(f'Some error: {ex}')
                continue

            with open(f'content/image{count}.jpg', 'wb') as file:
                file.write(picture)

            print(f'DOWNLOADED {count}/{len(lines)}')
            count += 1
            time.sleep(random.randint(1, 3))


def main():
    find_links()
    download_every_picture()


if __name__ == '__main__':
    main()