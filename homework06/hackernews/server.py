import typing as tp

from bottle import route, run, template, redirect, request

from hackernews.database.db import (
    News,
    get_session,
    engine,
    update_label,
    load_fresh_news,
    extract_all_news_from_db,
)

from hackernews.news.bayes import NaiveBayesClassifier


@tp.no_type_check
@route("/")
def main_page():
    return template("templates/main_menu")


@tp.no_type_check
@route("/news")
def news_list():
    s = get_session(engine=engine)
    rows = s.query(News).filter(News.label == None).all()
    return template("templates/news_template", rows=rows, more_button=True, label=True)


@tp.no_type_check
@route("/news_labeled")
def news_list_labeled():
    s = get_session(engine=engine)
    rows = s.query(News).filter(News.label != None).order_by(News.label)
    return template("templates/news_template", rows=rows, more_button=False, label=False)


@tp.no_type_check
@route("/add_label/")
def add_label() -> None:
    s = get_session(engine=engine)
    label = request.query["label"]
    id = request.query["id"]
    update_label(session=s, id=id, label=label)
    redirect("/news")


@tp.no_type_check
@route("/update_news")
def update_news() -> None:
    s = get_session(engine)
    load_fresh_news(session=s)
    redirect("/news")


@tp.no_type_check
@route("/recommendations")
def recommendations():
    s = get_session(engine=engine)

    labeled_news = s.query(News).filter(News.label != None).all()
    unlabeled_news = s.query(News).filter(News.label == None).all()
    model = NaiveBayesClassifier()

    X: tp.List[str] = []
    y: tp.List[str] = []

    for article in labeled_news:
        X.append(article.title)
        y.append(article.label)

    model.fit(X, y)

    for article in unlabeled_news:
        prediction = model.predict(article.title)
        article.prediction = prediction

    s.commit()

    news = extract_all_news_from_db(session=s)
    return template("templates/news_template_rec", rows=news, more_button=False, label=False)


if __name__ == "__main__":
    run(host="localhost", port=8080)
