import pytest
import csv

from hackernews.news.bayes import NaiveBayesClassifier


@pytest.fixture()
def data():
    return ["First statement", "Second statement"], ["pos", "neg"]


@pytest.fixture()
def spam_data():
    with open("homework06/tests/spam_collection.csv") as f:
        data = list(csv.reader(f, delimiter="\t"))
    return data


@pytest.fixture()
def classifier():
    return NaiveBayesClassifier()


def test_alpha_has_default_value_equal_to_1():
    model = NaiveBayesClassifier()
    assert model.alpha == 1


def test_make_words_list():
    words, labels = ["a b c"], ["pos"]
    expected_result = {"pos": {"a": 1, "b": 1, "c": 1}}
    actual_result = NaiveBayesClassifier.make_words_list(words, labels)

    assert expected_result == actual_result

    words, labels = [], []
    expected_result = {}
    actual_result = NaiveBayesClassifier.make_words_list(words, labels)

    assert expected_result == actual_result

    words, labels = ["a b c", "c c c"], ["pos", "neg"]
    expected_result = {"pos": {"a": 1, "b": 1, "c": 1}, "neg": {"c": 3}}
    actual_result = NaiveBayesClassifier.make_words_list(words, labels)

    assert expected_result == actual_result


def test_make_classes_list():
    classes = ["pos", "neg", "pos", "neg"]
    expected_result = {"pos": 2 / 4, "neg": 2 / 4}
    actual_result = NaiveBayesClassifier.make_classes_list(classes)

    assert expected_result == actual_result

    classes = []
    expected_result = {}
    actual_result = NaiveBayesClassifier.make_classes_list(classes)

    assert expected_result == actual_result


def test_count_entries():
    data = {"pos": {"a": 1, "b": 1, "c": 1}, "neg": {"c": 3}}
    expected_result = 3
    actual_result = NaiveBayesClassifier.count_entries(data)

    assert expected_result == actual_result

    data = {"pos": {}, "neg": {}}
    expected_result = 0
    actual_result = NaiveBayesClassifier.count_entries(data)

    assert expected_result == actual_result

    data = {}
    expected_result = 0
    actual_result = NaiveBayesClassifier.count_entries(data)

    assert expected_result == actual_result


def test_fit(data, classifier):
    model = classifier
    X, y = data
    model.fit(X, y)

    assert model._d == 3
    assert model._words_count == {"pos": {"first": 1, "statement": 1}, "neg": {"second": 1, "statement": 1}}
    assert model._class_freq == {"pos": 0.5, "neg": 0.5}


def test_predict(data, classifier):
    model = classifier
    X, y = data
    model.fit(X, y)

    statement = "First"
    assert model.predict(statement) == "pos"

    statement = "Second"
    assert model.predict(statement) == "neg"


def test_score(spam_data, classifier):
    model = classifier
    y, X = zip(*spam_data)
    X_train, y_train, X_test, y_test = X[:3900], y[:3900], X[3900:], y[3900:]

    model.fit(X_train, y_train)

    score = model.score(X_test, y_test)

    assert score >= 0.8


def test_bayes_classifier(spam_data):
    model = NaiveBayesClassifier()
    y, X = zip(*spam_data)
    X_train, y_train, X_test, y_test = X[:3900], y[:3900], X[3900:], y[3900:]

    model.fit(X_train, y_train)
    assert model.predict("Hello, how are you?") == "ham"

    score = model.score(X_test, y_test)
    assert score >= 0.8