from collections import defaultdict, Counter
from math import log
import typing as tp

from hackernews.utils.types import Freq, Label, Words, Labels
from hackernews.utils.textutils import prepare_data


class NaiveBayesClassifier:
    def __init__(self, alpha: float = 0.95) -> None:
        self.alpha = alpha
        self._words_freq: Freq = None
        self._class_freq: Freq = None
        self._d: int = 0

    @staticmethod
    def make_words_freq_list(X: Words, y: Labels) -> defaultdict:
        vocab_freq = defaultdict(lambda: defaultdict(int))
        for x_i, y_i in zip(X, y):
            words_list = x_i.split()
            for word in words_list:
                vocab_freq[y_i][word] += 1
        return vocab_freq

    @staticmethod
    def make_classes_freq_list(y: Labels) -> defaultdict:
        classes_freq = defaultdict(int)
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
            print(words)
        return len(words)

    def fit(self, X, y) -> None:
        """ Fit Naive Bayes classifier according to X, y. """
        X = prepare_data(X)
        self._words_freq = self.make_words_freq_list(X, y)
        self._d = self.count_entries(self._words_freq)
        self._class_freq = self.make_classes_freq_list(y)

    def predict(self, X) -> Label:
        """ Perform classification on an array of test vectors X. """
        pass

    def score(self, X_test, y_test):
        """ Returns the mean accuracy on the given test data and labels. """
        pass


def Data():
    return [
        ('I love this sandwich.', 'pos'),
        ('This is an amazing place!', 'pos'),
        ('I feel very good about these beers.', 'pos'),
        ('This is my best work.', 'pos'),
        ("What an awesome view", 'pos'),
        ('I do not like this restaurant', 'neg'),
        ('I am tired of this stuff.', 'neg'),
        ("I can't deal with this", 'neg'),
        ('He is my sworn enemy!', 'neg'),
        ('My boss is horrible.', 'neg')
    ]


if __name__ == "__main__":
    x = NaiveBayesClassifier()
    X, y = zip(*Data())
    x.fit(X, y)