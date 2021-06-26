import os
import asyncio
from arsenic import get_session, keys, browsers, services
import pandas as pd
from requests_html import HTML
import itertools
import re
import time
import pathlib

import logging
import structlog

# ocultar logs


def set_arsenic_log_level(level=logging.WARNING):
    # crear logger
    logger = logging.getLogger('arsenic')

    def logger_factory():
        return logger

    structlog.configure(logger_factory=logger_factory)
    logger.setLevel(level)


async def extract_id_slug(url_path):
    regex = r"^[^\s]+/(?P<id>\d+)-(?P<slug>[\w_-]+)$"
    group = re.match(regex, url_path)
    if not group:
        return None, None
    return group['id'], group['slug']


async def get_links(html_str):
    html_r = HTML(html=html_str)
    fabric_links = [x for x in list(
        html_r.links) if x.startswith('/es/telas/')]

    datas = []
    for path in fabric_links:
        id_, slug_ = await extract_id_slug(path)
        data = {
            "id": id_,
            "slug": slug_,
            "path": path,
            "scrapped": 0
        }
        datas.append(data)
    return datas


async def scraper(url):
    service = services.Chromedriver()
    browser = browsers.Chrome()
    browser.capabilities = {"goog:chromeOptions": {
        "args": ["--headless", "--no-gpu", "--disable-web-security", "--disable-site-isolation-trials"]}}
    # sesion asincrona
    async with get_session(service, browser) as session:
        await session.get(url)
        body = await session.get_page_source()
        return body


async def store_links_as_df_pickle(datas=[], name='links.pkl'):
    df = pd.DataFrame(datas)
    df.set_index('id', drop=True, inplace=True)
    df.to_pickle(name)
    return df


async def run(url):
    body_content = await scraper(url)
    links = await get_links(body_content)
    df = await store_links_as_df_pickle(links)
    return df

if __name__ == "__main__":
    url = 'https://www.spoonflower.com/es/mercado?on=fabric'
    set_arsenic_log_level()
    df = asyncio.run(run(url))
    print(df.head())
