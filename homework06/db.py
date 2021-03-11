from typing import Dict, List, Any
from sqlalchemy import Column, Integer, String, create_engine, update
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from scrapper import get_news

from sqlalchemy.sql import elements

Base = declarative_base()
engine = create_engine("sqlite:///news.db")
session = sessionmaker(bind=engine)


class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    url = Column(String)
    points = Column(Integer)
    label = Column(String)


def add_news(news: List[Dict[str, str]], current_session) -> None:
    s = session()
    for content in news:
        thing = News(
            title=content["title"],
            author=content["author"],
            url=content["link"],
            points=content["points"],
        )
        s.add(thing)
    s.commit()


def update_label(id: int, label: str) -> None:
    s = session()
    entry = s.query(News).get(int(id))
    entry.label = label
    s.commit()


def extract_all_news_from_db():
    s = session()
    entries = s.query(News).all()
    return entries


Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    # При запуске db.py получаем 1000+ записей в базе данных
    news_list = get_news(n_pages=34)
    add_news(news_list)
