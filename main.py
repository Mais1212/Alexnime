from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
import lxml

#Сайт с которого берем книги
HOST = "https://yummyanime.club/catalog"
#User-Agent, без него на сайт не пустят
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
page_number = 0

def get_content(pages_content) :
	anime_links = []
	selector_url = ".image-block"
	for anime in pages_content:
		anime_links.append(urljoin(HOST, str(pages_content.select_one(selector_url))))
	return anime_links





#Бежим по всем страницам
while page_number < 2:
	page_number += 1 

	url_page = HOST + "?page="  + str(page_number)
	response_page = requests.get(url_page, headers=HEADERS)
	soup_page = BeautifulSoup(response_page.text, "lxml")

	selector_content = ".anime-column"
	pages_content = soup_page.select(selector_content)
	anime_links = get_content(pages_content)

	print(anime_links)