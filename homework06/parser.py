import requests
from bs4 import BeautifulSoup

from typing import Dict, List, Any


def extract_news(parser: BeautifulSoup) -> List[Dict[str, str]]:
    """ Extract news from a given web page """
    news_list = []
    links = parser.select('.storylink')
    subtext = parser.select('.subtext')
    for pos, item in enumerate(links):
        title = item.getText()
        href = item.get('href', None)
        points = subtext[pos].select('.score')[0].getText()
        news_list.append({'title': title, 'link': href, 'points': points})
    return news_list


def extract_next_page(parser: BeautifulSoup):
    """ Extract next page URL """
    # PUT YOUR CODE HERE
    pass


def get_news(url: str, n_pages: int = 1):
    """ Collect news from a given web page """
    news: List[Dict[str, str]] = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news