import argparse
import xlwt
import time
import requests
import html.parser
from bs4 import BeautifulSoup

HOST = "https://yummyanime.club"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5)\
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}

PROXIES = {"http": "http://10.10.1.10:3128"}

anime_data = []


def createParser():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-sp",
        "--start_page",
        type=int,
        help="Какой страницой начать?",
        default=0
    )

    parser.add_argument(
        "-ep",
        "--end_page",
        type=int,
        help="Какой страницой закончить?",
        default=15
    )
    return parser


def create_excel(path="Результат.xlsx", anime_data=[""]):
    count = 1
    book = xlwt.Workbook("utf8")

    main_font = xlwt.easyxf(
        "font: height 240,name Fixedsys,colour_index black, bold off,\
        italic off; align: wrap on, vert top, horiz left;\
        borders: top_color black, bottom_color black, right_color black,\
        left_color black, left thin, right thin, top thin, bottom thin;\
        pattern: pattern solid, fore_colour green;")

    anime_font = xlwt.easyxf(
        "font: height 240,name Comic Sans MS ,colour_index\
        black, bold off,italic off; align: wrap on, vert top, horiz left;\
        borders: top_color black, bottom_color black, right_color black,\
        left_color black, left thin, right thin, top thin, bottom thin;\
        pattern: pattern solid, fore_colour yellow; alignment: ")

    sheet = book.add_sheet("Anine")

    sheet.write(0, 0, "Название", main_font)
    sheet.write(0, 1, "Год выхода", main_font)
    sheet.write(0, 2, "Жанры", main_font)
    sheet.write(0, 3, "Возрастной рейтинг", main_font)
    sheet.write(0, 4, "Оценка пользователей", main_font)
    sheet.write(0, 5, "Озвучка", main_font)

    for anime in anime_data:
        sheet.write(count, 0, anime[0], anime_font)
        sheet.write(count, 1, anime[1], anime_font)
        sheet.write(count, 2, anime[2], anime_font)
        sheet.write(count, 3, anime[3], anime_font)
        sheet.write(count, 4, anime[4] + "⭐", anime_font)
        sheet.write(count, 5, anime[5], anime_font)
        count += 1

    sheet.row(1).height = 3000

    sheet.col(0).width = 3000

    sheet.portrait = False

    sheet.set_print_scaling(85)

    book.save(path)


def get_content(pages_content):
    anime_links = []
    for anime in pages_content:
        anime_links.append(anime.get("href"))
    return anime_links


def main():
    parser = createParser()
    namespace = parser.parse_args()

    start_page = namespace.start_page
    end_page = namespace.end_page

    for page in range(start_page, end_page):

        url_page = HOST + "/catalog?page=" + str(page)
        response_main_page = requests.get(
            url_page, headers=HEADERS, timeout=(0.1, 10), proxies=PROXIES)
        soup_min_page = BeautifulSoup(
            response_main_page.content, "html.parser"
        )

        selector_content = ".anime-column .image-block"
        pages_content = soup_min_page.select(selector_content)
        anime_links = get_content(pages_content)
        count = 0
        for link in anime_links:

            response_anime_page = requests.get(
                HOST + link, headers=HEADERS, proxies=PROXIES)
            soup_anime_page = BeautifulSoup(
                response_anime_page.content, "html.parser")

            print(link)

            selector_name = ".content div div h1"
            selector_age = ".content-main-info li:nth-child(3)"
            selector_age_rating = ".content-main-info li:nth-child(5)"
            selector_ganres = ".content-main-info .categories-list"
            selector_rating = "span.main-rating-block > span.main-rating"
            selecror_voices = "ul.animeVoices > li"

            select_name = soup_anime_page.select_one(selector_name).text
            select_age = soup_anime_page.select_one(selector_age).text
            select_age_rating = soup_anime_page.select_one(
                selector_age_rating).text
            select_ganres = soup_anime_page.select_one(selector_ganres).text
            select_rating = soup_anime_page.select_one(selector_rating).text
            try:
                select_voices = soup_anime_page.select_one(
                    selecror_voices
                ).text
            except AttributeError:
                select_voices = "Не хватает данных"

            full_select = [select_name, select_age, select_ganres,
                           select_age_rating, select_rating, select_voices]
            anime_data.append(full_select)
            count += 1

    create_excel("Результат.xlsx", anime_data)


if __name__ == "__main__":
    main()
