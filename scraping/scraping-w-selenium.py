import re
import requests
import pandas as pd
from requests_html import HTML

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

url = 'https://www.spoonflower.com/es/mercado?on=fabric'


def scraper(url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-web-security")
    options.add_argument("--disable-site-isolation-trials")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    return driver.page_source


def extract_id_slug(url_path):
    regex = r"^[^\s]+/(?P<id>\d+)-(?P<slug>[\w_-]+)$"
    group = re.match(regex, url_path)
    if not group:
        return None, None
    return group['id'], group['slug']


content = scraper(url)

html_r = HTML(html=content)
# print(html_r.links)
fabric_links = [x for x in list(
    html_r.links) if x.startswith('/es/telas/')]

# for link in fabric_links:
#     print(link)

datas = []
for path in fabric_links:
    id_, slug_ = extract_id_slug(path)
    # print(id_, slug_)
    data = {
        "id": id_,
        "slug": slug_,
        "path": path,
        "scrapped": 0  # True / False -> 1 / 0
    }
    datas.append(data)

df = pd.DataFrame(datas)

df.to_csv("local.csv", index=False)
