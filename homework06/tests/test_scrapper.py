import re

import pytest
import requests
from bs4 import BeautifulSoup
from hackernews.utils.scrapper import *


@pytest.fixture
def page():
    return """<tr class="athing" id="26596092">
        <td class="title"><a href="https://lwn.net/Articles/850218/" class="storylink">First one</a>
        </td></tr> <tr><td class="subtext">
        <span class="score" id="score_26596092">1 point</span>
        <a href="user?id=me" class="hnuser">me</a></td></tr>
        <tr class="athing" id="26596092">
        <td class="title"><a href="https://lwn.net/Articles/850218/" class="storylink">Second</a>
        </td></tr> <tr><td class="subtext">
        <span class="score" id="score_26596092">1 point</span>
        <a href="user?id=me" class="hnuser">me</a></td></tr>
        <tr class="athing" id="26596092">
        <td class="title"><a href="https://lwn.net/Articles/850218/" class="storylink">Last</a>
        </td></tr> <tr><td class="subtext">
        <span class="score" id="score_26596092">1 point</span>
        <a href="user?id=me" class="hnuser">me</a></td></tr>
        <a href="?nextpagelink" class="morelink" rel="next">More</a>
        """


@pytest.fixture()
def fake_page():
    return """<a>There is nothing here, actually</a>"""


@pytest.fixture()
def soup(page):
    return BeautifulSoup(page, "html.parser")


def test_get_soup_works():
    url = "https://google.com"
    soup_actual = get_soup(url)

    assert type(soup_actual) == BeautifulSoup


def test_extract_news_count(soup) -> None:
    """Test to check if "extract_news" func returns exact count of news"""
    result = extract_news(parser=soup)
    print(result)
    assert len(result) == 3


def test_extract_news_wrong_page(fake_page) -> None:
    """Test to check if "extract_news" func returns [] when you parse news from wrong ycombinator page"""
    tmp_soup = BeautifulSoup(fake_page, "html.parser")
    result = extract_news(parser=tmp_soup)
    assert result == []


def test_extract_new_page(soup) -> None:
    """Test to check if "extract_new_page" func returns correct next page link"""
    result = extract_next_page(parser=soup)
    assert result == "?nextpagelink"


def test_extract_new_page_no_button(fake_page) -> None:
    """Test to check if "extract_new_page" func returns correct next page link"""
    with pytest.raises(Exception):
        result = extract_next_page(parser=BeautifulSoup(fake_page, "html.parser"))



def test_get_news_works_properly(soup) -> None:
    """Test to check if "extract_new_page" works properly"""
    result = get_news(soup, n_pages=0)
    assert result == []

    result = get_news(soup, n_pages=1)
    assert len(result) == 3
    assert result[0]["title"] == "First one"
