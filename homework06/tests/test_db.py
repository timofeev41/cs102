import pytest
from hackernews.database.db import *


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


def test_extract_all_news() -> None:
    actual = extract_all_news_from_db()
    s = session()
    expected = s.query(News).all()
    s.close()
    assert len(expected) == len(actual)


def test_load_fresh_news() -> None:
    pass
