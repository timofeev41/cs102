from typing import Dict, List, Any

from hackernews.utils.scrapper import get_news
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

Base = declarative_base()
SQLALCHEMY_DATABASE_URL = "sqlite:///news.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False)


class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    url = Column(String)
    points = Column(Integer)
    label = Column(String)


def get_session(engine) -> Session:
    SessionLocal.configure(bind=engine)
    return SessionLocal()


def add_news(session: Session, news: List[Dict[str, str]]) -> None:
    for content in news:
        thing = News(
            title=content["title"],
            author=content["author"],
            url=content["link"],
            points=content["points"],
        )
        session.add(thing)
    session.commit()


def update_label(session: Session, id: int, label: str) -> None:
    entry = session.query(News).get(int(id))
    entry.label = label
    session.commit()


def extract_all_news_from_db(session: Session):
    entries = session.query(News).all()
    return entries


def load_fresh_news(session: Session) -> None:
    fresh_news: List[Dict[str, Any]] = []
    news = get_news(n_pages=1)
    for item in news:
        ttl, auth = item["title"], item["author"]
        exists = list(session.query(News).filter(News.title == ttl, News.author == auth))
        if not exists:
            fresh_news.append(item)
        else:
            break
    if fresh_news:
        add_news(session=session, news=fresh_news)


Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    # При запуске db.py получаем 1000+ записей в базе данных
    s = get_session(engine)
    news_list = get_news(n_pages=1)
    add_news(session=s, news=news_list)
