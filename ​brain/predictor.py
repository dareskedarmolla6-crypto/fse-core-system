import numpy as np
from sklearn.linear_model import LogisticRegression

class AIBrain:
    def __init__(self):
        self.model = LogisticRegression()
        self.trained = False

    def train(self):
        X, y = [], []

        for _ in range(1000):
            price_change = np.random.uniform(-3, 3)
            volume = np.random.uniform(0, 100)

            X.append([price_change, volume])

            if price_change > 1 and volume > 50:
                y.append(1)
            elif price_change < -1 and volume > 50:
                y.append(-1)
            else:
                y.append(0)

        self.model.fit(X, y)
        self.trained = True

    def predict(self, data):
        if not self.trained:
            self.train()

        X = [[data["price_change"], data["volume"]]]
        pred = self.model.predict(X)[0]
        prob = max(self.model.predict_proba(X)[0])

        if pred == 1:
            return "LONG", round(prob * 100, 2)
        elif pred == -1:
            return "SHORT", round(prob * 100, 2)
        return "HEDGE", round(prob * 100, 2)
