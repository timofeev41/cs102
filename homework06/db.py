from typing import Dict, List, Any
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from parser import get_news

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


def add_news(news: List[Dict[str, str]]) -> None:
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


Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    news_list = get_news(n_pages=34)
    add_news(news_list)
