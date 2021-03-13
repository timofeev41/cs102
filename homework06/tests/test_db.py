from database import db

Base = db.declarative_base()
engine = db.create_engine("sqlite:///test.db")
session = db.sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)


def test_add_news():
    news = [{"title": "Test", "author": "Nikolay", "url": "https://example.com", "points": 10}]
    db.add_news(news=news)
