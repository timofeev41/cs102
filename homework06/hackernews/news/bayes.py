from collections import defaultdict
from math import log
import typing as tp

from hackernews.utils.textutils import prepare_data


class NaiveBayesClassifier:
    def __init__(self, alpha: float = 1) -> None:
        self.alpha = alpha
        self._words_count: tp.DefaultDict[str, tp.DefaultDict[str, tp.Union[float]]]
        self._class_freq: tp.DefaultDict[str, tp.Union[float]]
        self._class_count: tp.DefaultDict[str, int]
        self._d: int = 0

    @staticmethod
    def make_words_list(
        X: tp.List[str], y: tp.List[str]
    ) -> tp.DefaultDict[str, tp.DefaultDict[str, float]]:
        vocab_freq: tp.DefaultDict[str, tp.DefaultDict[str, float]] = defaultdict(
            lambda: defaultdict(lambda: 0)
        )
        for x_i, y_i in zip(X, y):
            words_list = x_i.split()
            for word in words_list:
                vocab_freq[y_i][word] += 1
        return vocab_freq

    @staticmethod
    def make_classes_list(y: tp.List[str]) -> tp.DefaultDict[str, float]:
        classes_freq: tp.DefaultDict[str, float] = defaultdict(lambda: 0)
        count, classes = len(y), set(y)
        for y_i in y:
            classes_freq[y_i] += 1
        for c in classes:
            classes_freq[c] /= count
        return classes_freq

    @staticmethod
    def count_entries(vocab_freq: tp.DefaultDict[str, tp.DefaultDict[str, float]]) -> int:
        if vocab_freq:
            words = set()
            for label in vocab_freq:
                words |= set(vocab_freq[label])
            return len(words)
        return 0

    @staticmethod
    def count_words(
        vocab_freq: tp.DefaultDict[str, tp.DefaultDict[str, float]]
    ) -> tp.DefaultDict[str, int]:
        cnt: tp.DefaultDict[str, int] = defaultdict(lambda: 0)
        for c in vocab_freq.keys():
            cnt[c] = sum(vocab_freq[c].values())  # type:ignore
        return cnt

    def fit(self, X: tp.List[str], y: tp.List[str]) -> None:
        """ Fit Naive Bayes classifier according to X, y. """
        X = prepare_data(X)
        self._words_count = self.make_words_list(X, y)
        self._class_freq = self.make_classes_list(y)
        self._class_count = self.count_words(self._words_count)
        self._d = self.count_entries(self._words_count)

    def predict(self, title: str) -> str:
        """ Perform classification on an array of test vectors title. """
        scores: tp.DefaultDict[str, float] = defaultdict(lambda: 0)
        titles = prepare_data(title.split())
        classes = self._class_freq.keys()
        for c in classes:
            scores[c] -= log(self._class_freq[c])
            for word in titles:
                scores[c] -= log(
                    (self._words_count[c][word] + self.alpha)
                    / (self._class_count[c] + self.alpha * self._d)
                )
            scores[c] = round(scores[c], 2)
        predicted_label, _ = min(scores.items(), key=lambda item: item[1])
        return predicted_label

    def score(self, X_test: tp.List[str], y_test: tp.List[str]) -> float:
        """ Returns the mean accuracy on the given test data and labels. """
        cnt_ok, cnt_all = 0, len(X_test)
        for x, y in zip(X_test, y_test):
            classified = self.predict(x)
            if classified == y:
                cnt_ok += 1
        return cnt_ok / float(cnt_all)
