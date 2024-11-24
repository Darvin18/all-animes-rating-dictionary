import requests
from bs4 import BeautifulSoup
import json
import time, random
from headers import headers


best_anime_dict = {}

main_url = "https://animego.org/anime"

def main(main_url):

    s = requests.Session()
    s.headers.update(headers)

    for i in range(1, 136):

        main_url = f"{main_url}?sort=a.createdAt&direction=desc&type=animes&page={i}"

        response = s.get(main_url)
        bs = BeautifulSoup(response.text, "lxml")

        list_anime = bs.find_all("div", class_="col-12")[0:-1]

        for anime in list_anime:
            name = anime.find("div", class_="h5 font-weight-normal mb-1").find("a").text
            try:
                rating = anime.find("div", class_="p-rate-flag__text").text
                edited_rating = float(rating.replace(",", "."))
            except AttributeError:
                edited_rating = 0.0
            best_anime_dict[name] = edited_rating

        time.sleep(random.choice([2,3,4]))


main(main_url)

sorted_anime_dict = dict(sorted(best_anime_dict.items(), key=lambda x: x[1], reverse=True))

with open("best_animes.txt", "w", encoding="utf-8") as best_anime_file:
    best_anime_file.write(json.dumps(sorted_anime_dict, indent=4, ensure_ascii=False))
