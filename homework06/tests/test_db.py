from hackernews.database.db import *


def test_add_news() -> None:
    pass


def test_update_label() -> None:
    pass


def test_extract_all_news() -> None:
    actual = extract_all_news_from_db()
    s = session()
    expected = s.query(News).all()
    s.close()
    assert len(expected) == len(actual)


def test_load_fresh_news() -> None:
    pass
