from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")

import requests
from bs4 import BeautifulSoup
from datetime import date
import re
import sqlite3
from product import product

conn = sqlite3.connect("coto_products2.db")
c = conn.cursor()

c.execute("""DELETE FROM products WHERE date='{}';""".format(date.today()))


def insert_product(prod):
    with conn:
        c.execute(
            "INSERT INTO products VALUES(?,?,?,?,?,?,?)",
            (
                prod.main_category,
                prod.category,
                prod.sub_category,
                prod.sku,
                prod.name,
                prod.price,
                prod.date,
            ),
        )


def get_categories(nextPage):
    source1 = requests.get(nextPage).text
    soup = BeautifulSoup(source1, "lxml")
    div = soup.findAll("div", class_="atg_store_refinementAncestorsLinkCategory")

    categories = []
    for cada in div[1:]:
        letra = str(cada.find("a", class_="atg_store_actionDelete"))
        x = re.findall("(?<=>)(.*)(?=<)", letra)[0]
        categories.append(x)

    main_category = categories[0].strip()
    category = categories[1].strip() if len(categories) > 1 else ""
    sub_category = soup.find("title").text.strip()

    print(main_category, category, sub_category)
    return [main_category, category, sub_category]


def scrape_product(nextPage, i=1):
    categories = get_categories(nextPage)
    x = "continue"
    while x == "continue":
        source1 = requests.get(nextPage).text
        soup = BeautifulSoup(source1, "lxml")
        i += 1
        actual_page = soup.find("a", class_="disabledLink")
        try:
            prox_page = str(int(actual_page.text) + 1)
            nextPage = (
                "https://www.cotodigital3.com.ar"
                + soup.find("a", title=str("Ir a página " + prox_page)).attrs["href"]
            )
        except:
            x = "stop"
            print("no next")

        li = soup.findAll("li", class_="clearfix")
        for each in li:
            producto = each.find("div", class_="descrip_full").text.strip()
            try:
                price = (
                    each.find("span", class_="atg_store_newPrice")
                    .text.split("$")[1]
                    .strip()
                )
            except:
                price = 0
            sku = (
                each.find("div", class_="descrip_full")
                .attrs["id"]
                .split("sku")[1]
                .strip()
            )
            insert_product(
                product(
                    categories[0], categories[1], categories[2], sku, producto, price
                )
            )

    return


driver = webdriver.Chrome(ChromeDriverManager().install())
base_url = "https://www.cotodigital3.com.ar"
driver.get(base_url)
assert "Coto" in driver.title

products = {}

elem = driver.find_elements_by_xpath(
    '//div[4]/div[1]/div[2]/div/div[2]/div/ul/li[not(@id="categoriaOferta")]/div/div/div/ul/div/li/a'
)

categorias = []
categorias_url = []
for each in elem:
    categorias_url.append(base_url + each.get_attribute("pathname"))

assert "No results found." not in driver.page_source
driver.close()

for category_url in categorias_url:
    print(category_url)
    scrape_product(category_url)


conn.commit()


conn.close()
