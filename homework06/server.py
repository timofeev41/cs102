from bottle import SimpleTemplate, route, run, template, redirect, request
from sqlalchemy.orm import query_expression


from db import News, session, update_label

# from bayes import NaiveBayesClassifier


@route("/")
def main_page():
    return template("templates/main_menu")


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template("templates/news_template", rows=rows, more_button=True, label=True)


@route("/news_labeled")
def news_list_labeled():
    s = session()
    rows = s.query(News).filter(News.label != None).all()
    return template("templates/news_template", rows=rows, more_button=False, label=False)


@route("/add_label/")
def add_label():
    req = request.query_string
    try:
        label, id = req.split("&")
    except ValueError:
        return template("templates/exception", exception="Expected 2 arguments. Label and ID.")
    label = label[label.index("=") + 1 :]
    id = id[id.index("=") + 1 :]
    update_label(id=id, label=label)
    redirect("/news")


@route("/update")
def update_news():
    # PUT YOUR CODE HERE
    redirect("/news")


@route("/classify")
def classify_news():
    pass


if __name__ == "__main__":
    run(host="localhost", port=8080)
