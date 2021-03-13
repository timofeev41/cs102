import requests
import re

from bs4 import BeautifulSoup
from utils import scrapper

page = requests.get("https://news.ycombinator.com/newest")
soup = BeautifulSoup(page.text, "html.parser")


def test_extract_news_count():
    """Test to check if "extract_news" func returns exact count of news"""
    result = scrapper.extract_news(parser=soup)
    assert len(result) == 30


def test_extract_news_wrong_page():
    """Test to check if "extract_news" func returns [] when you parse news from wrong ycombinator page"""
    tmp_page = requests.get("https://news.ycombinator.com/submit")
    tmp_soup = BeautifulSoup(tmp_page.text, "html.parser")
    result = scrapper.extract_news(parser=tmp_soup)
    assert result == []


def test_extract_new_page():
    """Test to check if "extract_new_page" func returns correct next page link using reg-ex"""
    result = scrapper.extract_next_page(parser=soup)
    assert re.match("\\?next=\\d*\\&n\\=\\d*", result).span() == (0, 19)
