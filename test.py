import requests
from bs4 import BeautifulSoup
 
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
page = requests.get("https://yummyanime.club/catalog/item/hak-vernuvshijsya", headers=HEADERS)
text = page.content
soup = BeautifulSoup(text, "html.parser")
find_title = soup.find("div", {"class": "content-page anime-page"})
title = find_title.find("h1")
print(title.text.split()[0])
 
info_item = soup.find("ul", {"class": "content-main-info"}).find_all("li")
 
page.close()
 
item_views = info_item[0].text.replace("\n", "")
item_status = info_item[1].text.replace("\n", "")
item_year = info_item[2].text.replace("\n", "")
item_season = info_item[3].text.replace("\n", "")
item_age = info_item[4].text.replace("\n", "")
genre = soup.find("ul", {"class": "content-main-info"}).find("li", {"class": "categories-list"}).find_all("li")
genres = []
for g in genre:
    genres.append(g.text.replace("\n", ""))
item_genres = ', '.join(genres)
print(item_views)
print(item_status)
print(item_year)
print(item_season)
print(item_age)
print(info_item[5].text.replace("\n", "").split(":")[0] + ": " + str(item_genres))


#print("================Common print=====================")
#for i in range(len(info_item)):
#    print(i)
#    print(info_item[i].text.replace("\n", ""))