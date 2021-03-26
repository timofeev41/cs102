import pytest

from hackernews.news.bayes import NaiveBayesClassifier


def test_make_words_list():
    model = NaiveBayesClassifier()

    words, labels = ["a b c"], ["pos"]
    expected_result = {'pos': {'a': 1, 'b': 1, 'c': 1}}
    actual_result = model.make_words_list(words, labels)

    assert expected_result == actual_result

    words, labels = [], []
    expected_result = {}
    actual_result = model.make_words_list(words, labels)

    assert expected_result == actual_result

    words, labels = ["a b c", "c c c"], ["pos", "neg"]
    expected_result = {'pos': {'a': 1, 'b': 1, 'c': 1}, 'neg': {'c': 3}}
    actual_result = model.make_words_list(words, labels)

    assert expected_result == actual_result


def test_make_classes_list():
    model = NaiveBayesClassifier()

    classes = ["pos", "neg", "pos", "neg"]
    expected_result = {'pos': 2 / 4, 'neg': 2 / 4}
    actual_result = model.make_classes_list(classes)

    assert expected_result == actual_result

    classes = []
    expected_result = {}
    actual_result = model.make_classes_list(classes)

    assert expected_result == actual_result


def test_count_entries():
    model = NaiveBayesClassifier()
    data = {'pos': {'a': 1, 'b': 1, 'c': 1}, 'neg': {'c': 3}}
    expected_result = 3
    actual_result = model.count_entries(data)

    assert expected_result == actual_result

    data = {"pos": {}, "neg": {}}
    expected_result = 0
    actual_result = model.count_entries(data)

    assert expected_result == actual_result

    data = {}
    expected_result = 0
    actual_result = model.count_entries(data)

    assert expected_result == actual_result
