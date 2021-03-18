import string
from collections import defaultdict, Counter


class NaiveBayesClassifier:
    def __init__(self, alpha):
        self.alpha = alpha
        self.words = defaultdict(lambda: 0)
        self.cnt = Counter()
        self.classes = Counter()
        self.every_word_cnt = Counter()

    def fit(self, X, y):
        """ Fit Naive Bayes classifier according to X, y. """
        for cls in y:
            self.classes[cls] += 1
            for word in X:
                translator = str.maketrans("", "", string.punctuation)
                word = word.translate(translator).lower()
                self.every_word_cnt[word] += 1
                self.words[cls, word] += 1

        for cls, word in self.words:
            self.words[cls, word] /= self.classes[cls]

        for cls in self.classes:
            self.classes[cls] /= sum(self.every_word_cnt.values())

    def predict(self, X):
        """ Perform classification on an array of test vectors X. """


    def score(self, X_test, y_test):
        """ Returns the mean accuracy on the given test data and labels. """
        pass
