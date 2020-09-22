from bs4 import BeautifulSoup
from urllib.parse import urljoin
from selenium import webdriver
import requests
import html.parser
 
# Сайт с которого берем Анимешки
HOST = "https://yummyanime.club"
# User-Agent, без него на сайт не пустят
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
page_number = 0
 
 
def get_content(pages_content):
    anime_links = []
    for anime in pages_content:
        anime_links.append(anime.get('href'))
    return anime_links
 
 
# Бежим по всем страницам
while page_number < 2:
 
    url_page = HOST + "/catalog?page=" + str(page_number)
    response_main_page = requests.get(url_page, headers=HEADERS)
    soup_min_page = BeautifulSoup(response_main_page.content, "html.parser")
	 
    selector_content = ".anime-column .image-block"
    pages_content = soup_min_page.select(selector_content)
    anime_links = get_content(pages_content)
    count = 0
    for link in anime_links:

        response_anime_page = requests.get(HOST + link, headers=HEADERS)
        soup_anime_page = BeautifulSoup(response_anime_page.content, "html.parser")
 
        selector_name = "div.anime-column-info a"
        selector_age = "span.year-block"
        selector_age_rating = "ul.content-main-info li" #<li><span>Возрастной рейтинг:</span> PG-13 (от 13 лет)</li>
        select_name = soup_anime_page.select(selector_name)
        select_age = soup_anime_page.select(selector_age)
        selector_age_rating = soup_anime_page.select(selector_age_rating)
        print(selector_age_rating.text)
        count += 1
 
    page_number += 1