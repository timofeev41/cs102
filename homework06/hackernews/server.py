import typing as tp

from bottle import route, run, template, redirect, request

from hackernews.database.db import News, get_session, engine, update_label, load_fresh_news


# from bayes import NaiveBayesClassifier

@tp.no_type_check
@route("/")
def main_page():
    return template("templates/main_menu")


@tp.no_type_check
@route("/news")
def news_list():
    s = get_session(engine)
    rows = s.query(News).filter(News.label == None).all()
    return template("templates/news_template", rows=rows, more_button=True, label=True)


@tp.no_type_check
@route("/news_labeled")
def news_list_labeled():
    s = get_session(engine)
    rows = []
    for i in ("good", "maybe", "never"):
        rows.extend(s.query(News).filter(News.label == i).all())
    return template("templates/news_template", rows=rows, more_button=False, label=False)


@tp.no_type_check
@route("/add_label/")
def add_label():
    s = get_session(engine)
    req = request.query_string
    try:
        label, id = req.split("&")
    except ValueError:
        return template("templates/exception", exception="Expected 2 arguments. Label and ID.")
    label = label[label.index("=") + 1:]
    id = id[id.index("=") + 1:]
    update_label(session=s, id=id, label=label)
    redirect("/news")


@tp.no_type_check
@route("/update_news")
def update_news() -> None:
    s = get_session(engine)
    load_fresh_news(session=s)
    redirect("/news")


@tp.no_type_check
@route("/classify")
def classify_news() -> None:
    pass


if __name__ == "__main__":
    run(host="localhost", port=8080)
