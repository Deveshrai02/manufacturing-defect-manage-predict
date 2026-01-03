from sklearn.metrics import accuracy_score

class Metrics:
    @staticmethod
    def accuracy(y_true, y_pred):
        """Return accuracy score between true and predicted labels.

        This is a static helper so you can call Metrics.accuracy(y_true, y_pred)
        or via an instance: Metrics().accuracy(y_true, y_pred).
        """
        return accuracy_score(y_true, y_pred)