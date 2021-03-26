from hackernews.utils.textutils import clean, prepare_data


def test_clean():
    data = "Test!"
    actual_result = clean(data)
    expected_result = "test"

    assert actual_result == expected_result

    data = "H2@%e21.y!"
    actual_result = clean(data)
    expected_result = "hey"

    assert actual_result == expected_result

    data = ""
    actual_result = clean(data)
    expected_result = ""

    assert actual_result == expected_result

    data = "already clean"
    actual_result = clean(data)
    expected_result = "already clean"

    assert actual_result == expected_result


def test_prepare_data():
    data = ["Python 3 framework to build website (2020)", "Simple framework!"]
    actual_result = prepare_data(data)
    expected_result = ["python  framework to build website ", "simple framework"]

    assert actual_result == expected_result

    data = ""
    actual_result = prepare_data(data)
    expected_result = []

    assert actual_result == expected_result
