from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
import lxml

#Сайт с которого берем Анимешки
HOST = "https://yummyanime.club"
#User-Agent, без него на сайт не пустят
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
page_number = 0

def get_content(pages_content) :
	anime_links = []
	for anime in pages_content:
		anime_links.append(anime.get('href'))
	return anime_links


#Бежим по всем страницам
while page_number < 2: 

	url_page = HOST + "/catalog?page="  + str(page_number)
	response_main_page = requests.get(url_page, headers=HEADERS)
	soup_min_page = BeautifulSoup(response_main_page.text, "lxml")

	selector_content = ".anime-column .image-block"
	pages_content = soup_min_page.select(selector_content)
	anime_links = get_content(pages_content)

	for link in anime_links :
		response_anime_page = requests.get(HOST + link, headers=HEADERS)
		soup_anime_page = BeautifulSoup(response_main_page.text, "lxml")

		selector_name = "div.content div div h1"
		select_name = soup_anime_page.select(selector_name)
		print(select_name)
		





	page_number += 1