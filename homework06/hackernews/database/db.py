import typing as tp
from sqlalchemy.future import Engine

from hackernews.utils.scrapper import get_news, get_soup
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, Query

Base = declarative_base()
SQLALCHEMY_DATABASE_URL = "sqlite:///news.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False)


class News(Base):  # type: ignore
    __tablename__ = "news"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    url = Column(String)
    points = Column(Integer)
    label = Column(String)
    prediction = Column(String)


RawNewsList = tp.List[tp.Dict[str, tp.Union[int, str]]]
NewsList = tp.List[News]


@tp.no_type_check
def get_session(engine: Engine) -> Session:
    SessionLocal.configure(bind=engine)
    return SessionLocal()


def add_news(session: Session, raw_news_list: RawNewsList) -> None:
    # for content in news:
    #     article = News(
    #         title=content["title"],
    #         author=content["author"],
    #         url=content["link"],
    #         points=content["points"],
    #     )
    #     session.add(article)
    news = [News(**news_data) for news_data in raw_news_list]
    session.add_all(news)
    session.commit()


def update_label(session: Session, id: int, label: str) -> None:
    entry = session.query(News).get(id)
    if entry is not None:
        entry.label = label
        session.commit()


def extract_all_news_from_db(session: Session) -> NewsList:
    entries = session.query(News).all()
    return entries  # type: ignore


def load_fresh_news(session: Session, url: str = "https://news.ycombinator.com/newest") -> None:
    soup = get_soup(url=url)
    fresh_news: RawNewsList = []
    news = get_news(parser=soup, n_pages=1)
    for item in news:
        title, author = item["title"], item["author"]
        exists = list(session.query(News).filter(News.title == title, News.author == author))
        if not exists:
            fresh_news.append(item)
    if fresh_news:
        add_news(session=session, raw_news_list=fresh_news)


Base.metadata.create_all(bind=engine)
