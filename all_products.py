import requests
from bs4 import BeautifulSoup
import json

url = "https://parsinger.ru/html/index4_page_1.html"


def soup(url):
    response = requests.get(url=url)
    response.encoding = "utf-8"
    return BeautifulSoup(response.text, "lxml")


soup1 = soup(url)
nav_url = [link["href"] for link in soup1.find("div", class_="nav_menu").find_all("a")]
pag_url = [link["href"] for link in soup1.find("div", class_="pagen").find_all("a")]
res_json = []
for i in range(len(nav_url)):
    for j in range(len(pag_url)):
        key_list = []
        soup1 = soup(f"https://parsinger.ru/html/index{i + 1}_page_{j + 1}.html")
        key_description = [j[0] for j in
                           [i.text.split(":") for i in soup1.find_all("li")]]
        [key_list.append(i) for i in key_description]
        soup1 = soup(f"https://parsinger.ru/html/index{i + 1}_page_{j + 1}.html")
        name = [i.text.strip() for i in soup1.find_all("a", class_="name_item")]
        description = [i.text.split("\n") for i in soup1.find_all("div", class_="description")]
        price = [i.text.strip() for i in soup1.find_all("p", class_="price")]
        l = 0
        for n, d, p in zip(name, description, price):
            res_json.append({
                "Наименование": n,
                f"{key_list[l]}": d[1].split(": ")[1].strip(),
                f"{key_list[l + 1]}": d[2].split(": ")[1].strip(),
                f"{key_list[l + 2]}": d[3].split(": ")[1].strip(),
                f"{key_list[l + 3]}": d[4].split(": ")[1].strip(),
                "Цена": p
            })
            l += 4

with open("new.json", "w", encoding="utf-8") as file:
    json.dump(res_json, file, indent=4, ensure_ascii=False)