from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

class ModelFactory:
    @staticmethod
    def get(name):
        if name == "logistic":
            return LogisticRegression()
        elif name == "rf":
            return RandomForestClassifier()
        else:
            raise ValueError("Unknown model")
