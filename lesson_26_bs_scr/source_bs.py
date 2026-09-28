from bs4 import BeautifulSoup

import requests
import os

from dotenv import load_dotenv

load_dotenv()

base_url = "http://127.0.0.1:8000"

def get_web_data(url_enpoint="", userdata:dict={}, headers={}):
    url = f"{base_url}" # /{url_enpoint}
    response = requests.get(url, params=userdata, headers=headers)
    return response

html = get_web_data().content
print(html)

soup = BeautifulSoup(
    html,
    "html.parser"
)
print(soup)

title = soup.find("h1")

print(title)
print(title.text)

texts = soup.find_all("p")
print(texts)
for t in texts:
    print(t.text)

price = soup.find(
    class_="price"
)

print(price.text)

links = soup.find_all("a")
for l in links:
    print(l["href"])

fb_link = soup.find(
    class_="ananas"
)

print(fb_link["href"])
print(fb_link.text)

titles = soup.select(
    ".product>.title"
)
prices = soup.select(
    ".product>.price"
)

products = dict(zip(
    [t.text.strip() for t in titles],
    [float(t.text.strip()) for t in prices]
))
print(products)

# for t in titles:
#     print(t.text.strip())
# for t in prices:
#     print(t.text.strip())

class Product:

    def __init__(self, name, price):
        self.name = name
        self.price = float(price)

    @property
    def price_with_tax(self):
        return round(
            self.price * 1.2, 2
        )
"""
[
    ("Laptop", 1200.0),
    ("Phone", 800.0),
]
"""
products_items = list(map(lambda item: Product(item[0], item[1]), products.items()))
for p in products_items:
    print(p.name, p.price, p.price_with_tax)