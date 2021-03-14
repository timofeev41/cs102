from typing import Any, Dict, List

import requests
from bs4 import BeautifulSoup

News = List[Dict[str, str]]


def extract_news(parser: BeautifulSoup) -> News:
    """ Extract news from a given web page """
    news_list: News = []
    links = parser.select(".storylink")
    subtext = parser.select(".subtext")
    for pos, item in enumerate(links):
        title = item.getText()
        href = item.get("href", None)
        if str(href).startswith("item"):
            href = "https://news.ycombinator.com/" + href
        points = int(subtext[pos].select(".score")[0].getText().split()[0])
        user = subtext[pos].select(".hnuser")[0].getText()
        if user is None:
            user = "None"
        news_list.append({"title": title, "link": href, "points": points, "author": user})
    return news_list


def extract_next_page(parser: BeautifulSoup) -> str:
    """ Extract next page URL """
    link = parser.select(".morelink")[0]["href"]
    if link is None:
        raise Exception("Parsed all news")
    return link[link.index("?") :]


def get_news(url: str = "https://news.ycombinator.com/newest", n_pages: int = 1) -> News:
    """ Collect news from a given web page """
    news: News = []
    if not url.startswith("https://news.ycombinator.com"):
        raise Exception("Script only able to scrap news from https://news.ycombinator.com")
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/newest" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news
