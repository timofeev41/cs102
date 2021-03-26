from collections import defaultdict, Counter
from math import log
import typing as tp

from hackernews.utils.textutils import prepare_data

Vocabulary = tp.Dict[str, tp.Union[str, int]]
Predictions = tp.Iterable[tp.Dict[str, float]]
Freq = tp.Optional[Vocabulary]
Labels = tp.Iterable[str]
Words = tp.Iterable[str]


class NaiveBayesClassifier:
    def __init__(self, alpha: float = 1) -> None:
        self.alpha = alpha
        self._words_freq: Freq = None
        self._class_freq: Freq = None
        self._d: int = 0

    @staticmethod
    def make_words_freq_list(X: Words, y: Labels) -> defaultdict:
        vocab_freq = defaultdict(lambda: defaultdict(lambda: 0))
        for x_i, y_i in zip(X, y):
            words_list = x_i.split()
            for word in words_list:
                vocab_freq[y_i][word] += 1
        return vocab_freq

    @staticmethod
    def make_classes_freq_list(y: Labels) -> defaultdict:
        classes_freq = defaultdict(lambda: 0)
        count, classes = len(y), set(y)
        for y_i in y:
            classes_freq[y_i] += 1
        for c in classes:
            classes_freq[c] /= count
        return classes_freq

    @staticmethod
    def count_entries(vocab_freq: Freq) -> int:
        words = set()
        for label in vocab_freq:
            words |= set(vocab_freq[label])
            # print(words)
        return len(words)

    def fit(self, X: Words, y: Labels) -> None:
        """ Fit Naive Bayes classifier according to X, y. """
        X = prepare_data(X)
        self._words_freq = self.make_words_freq_list(X, y)
        self._class_freq = self.make_classes_freq_list(y)
        self._d = self.count_entries(self._words_freq)

    def predict(self, title: str) -> str:
        """ Perform classification on an array of test vectors title. """
        scores = defaultdict(lambda: 0)
        titles = prepare_data(title.split())
        classes = self._class_freq.keys()
        for c in classes:
            scores[c] += log(self._class_freq[c])
            for word in titles:
                scores[c] += log(self._words_freq[c][word] + self.alpha) / (
                        len(self._words_freq[c].values()) + self.alpha * self._d)
            scores[c] = round(scores[c], 2)
        min_val, prediction = max(scores.values()), str
        for c, v in scores.items():
            if v == min_val:
                prediction = c
                break
        return prediction

    def score(self, X_test: Words, y_test: Labels):
        """ Returns the mean accuracy on the given test data and labels. """
        cnt_ok, cnt_all = 0, len(X_test)
        for x, y in zip(X_test, y_test):
            classified = self.predict(x)
            if classified == y:
                cnt_ok += 1
        print(f"{cnt_all} {cnt_ok}")
        return cnt_ok / float(cnt_all)


if __name__ == "__main__":
    import csv

    x = NaiveBayesClassifier()
    with open("spam_collection.csv") as f:
        data = list(csv.reader(f, delimiter="\t"))
    print(f"data = {len(data)}")
    y, X = zip(*data)
    X_train, y_train, X_test, y_test = X[:3900], y[:3900], X[3900:], y[3900:]
    x.fit(X_train, y_train)
    print(x.score(X_test, y_test))
