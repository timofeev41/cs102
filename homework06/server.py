from bottle import SimpleTemplate, route, run, template, redirect, request
from sqlalchemy.orm import query_expression


from db import News, session

# from bayes import NaiveBayesClassifier


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template("templates/news_template", rows=rows)


@route("/add_label/")
def add_label():
    req = request.query_string
    try:
        label, id = req.split("&")
    except ValueError:
        return template("templates/exception", exception="Expected 2 arguments")
    print(f"{label} {id}")
    # 1. Получить значения параметров label и id из GET-запроса
    # 2. Получить запись из БД с соответствующим id (такая запись только одна!)
    # 3. Изменить значение метки записи на значение label
    # 4. Сохранить результат в БД
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
