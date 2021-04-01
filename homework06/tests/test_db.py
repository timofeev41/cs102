import pytest
from hackernews.database.db import *

FAKE_NEWS = [
    {"title": "Cats invaded Moon", "url": "example.com", "points": 12, "author": "Nikolas"},
    {
        "title": "Nikolas got 100 points for this task",
        "url": "yandex.ru",
        "points": 100,
        "author": "Dementiy",
    },
]


def db_set_up(engine):
    Base.metadata.create_all(bind=engine)


def db_tear_down(session):
    session.query(News).delete()
    session.commit()
    session.close()


@pytest.fixture
def engine():
    return create_engine("sqlite://")


@pytest.fixture
def session(engine):
    session = get_session(engine)
    db_set_up(engine)
    yield session
    db_tear_down(session)


def test_news_can_be_saved(session):
    add_news(session=session, raw_news_list=FAKE_NEWS)

    saved_item = session.query(News).get(1)
    assert saved_item.title == FAKE_NEWS[0]["title"]
    assert saved_item.author == FAKE_NEWS[0]["author"]

    saved_item = session.query(News).get(2)
    assert saved_item.title == FAKE_NEWS[1]["title"]
    assert saved_item.author == FAKE_NEWS[1]["author"]


def test_can_news_be_labeled(session):
    add_news(session=session, raw_news_list=FAKE_NEWS)

    saved_item = session.query(News).get(1)
    assert saved_item.label is None

    label = "good"
    update_label(session=session, id=1, label=label)
    saved_item = session.query(News).get(1)
    assert saved_item.label == label


def test_all_news_can_be_extracted(session):
    add_news(session=session, raw_news_list=FAKE_NEWS)
    news = extract_all_news_from_db(session=session)

    assert len(news) == len(FAKE_NEWS)


def test_fresh_news_can_be_added(session):
    """Идея такая: у нас есть 2 новости, мы проверяем, что 30 новостей выгрузятся и запишутся рядом, не повредив
    исходные данные"""
    add_news(session=session, raw_news_list=FAKE_NEWS)
    news = extract_all_news_from_db(session=session)

    load_fresh_news(session)

    all_news = extract_all_news_from_db(session=session)
    assert len(all_news) == 32
