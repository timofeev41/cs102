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
        points = subtext[pos].select(".score")[0].getText()
        news_list.append({"title": title, "link": href, "points": points})
    return news_list


def extract_next_page(parser: BeautifulSoup) -> str:
    """ Extract next page URL """
    link = parser.select(".morelink")[0]["href"]
    return link[link.index("?") :]


def get_news(url: str = "https://news.ycombinator.com/newest", n_pages: int = 1) -> News:
    """ Collect news from a given web page """
    news: News = []
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
