
# ==========================================================
# FSE BRAIN PREDICTOR MODULE (CLEAN)
# ==========================================================

import numpy as np
from sklearn.linear_model import LogisticRegression
from collections import defaultdict


# ==========================================================
# BASIC RULE-BASED BRAIN (FAST LAYER)
# ==========================================================

class Brain:
    def predict(self, data):
        price = data.get("price_change", 0)

        if price > 1:
            return "LONG", 80
        elif price < -1:
            return "SHORT", 80
        return "HEDGE", 60


# ==========================================================
# ML-BASED AI BRAIN (LEARNING LAYER)
# ==========================================================

class AIBrain:
    def __init__(self):
        self.model = LogisticRegression()
        self.trained = False

    def train(self):
        X = np.random.uniform(-3, 3, (1000, 2))
        y = np.where(
            X[:, 0] > 1,
            1,
            np.where(X[:, 0] < -1, -1, 0)
        )

        self.model.fit(X, y)
        self.trained = True

    def predict(self, data):
        if not self.trained:
            self.train()

        X = [[data.get("price_change", 0), data.get("volume", 0)]]

        pred = self.model.predict(X)[0]
        prob = np.max(self.model.predict_proba(X))

        mapping = {
            1: "LONG",
            -1: "SHORT",
            0: "HEDGE"
        }

        return mapping[pred], round(prob * 100, 2)


# ==========================================================
# MARKET SENTIMENT PREDICTOR
# ==========================================================

class Predictor:
    def analyze_market(self, data):
        # simplified regime classifier
        confidence = 0.90

        if confidence >= 0.85:
            return "TREND"

        return "HEDGE"


# ==========================================================
# FSE CORE DECISION GATE
# ==========================================================

class FSECore:
    def __init__(self, brain, risk):
        self.brain = brain
        self.risk = risk

    def decide(self, market, balance, position_size, open_positions, drawdown):

        if self.risk.emergency_stop(drawdown):
            return "SYSTEM_STOP"

        analysis = self.brain.analyze(market)

        if self.risk.check_trade(balance, position_size, open_positions) != "APPROVED":
            return "TRADE_BLOCKED"

        if analysis["confidence"] < 0.4:
            return "HEDGE"

        if analysis.get("trend") == "UP":
            return "LONG"

        if analysis.get("trend") == "DOWN":
            return "SHORT"

        return "GRID"


# ==========================================================
# SIGNAL CONSENSUS SYSTEM
# ==========================================================

class SignalVoteEngine:
    def vote(self, signals):
        votes = defaultdict(lambda: {"buy": 0, "sell": 0})

        for s in signals:
            key = s["symbol"]

            if s["side"] == "BUY":
                votes[key]["buy"] += s.get("score", 10)

            elif s["side"] == "SELL":
                votes[key]["sell"] += s.get("score", 10)

        return votes


class ConsensusBuilder:
    def build(self, votes):
        consensus = []

        for symbol, v in votes.items():
            buy, sell = v["buy"], v["sell"]
            total = buy + sell

            if total == 0:
                continue

            bias = (buy - sell) / total

            if bias > 0.3:
                consensus.append({
                    "symbol": symbol,
                    "side": "BUY",
                    "strength": round(bias, 2)
                })

            elif bias < -0.3:
                consensus.append({
                    "symbol": symbol,
                    "side": "SELL",
                    "strength": round(abs(bias), 2)
                })

        return consensus


class SmartConsensusEngine:
    def __init__(self):
        self.vote_engine = SignalVoteEngine()
        self.builder = ConsensusBuilder()

    def process(self, signals):
        votes = self.vote_engine.vote(signals)
        return self.builder.build(votes)


# ==========================================================
# POLICY NETWORK (RL CORE)
# ==========================================================

class PolicyNetwork:
    def __init__(self, state_size=5):
        self.weights = np.random.randn(state_size)
        self.lr = 0.01

    def act(self, state):
        score = np.dot(self.weights, state)

        if score > 0.5:
            return "LONG"
        elif score < -0.5:
            return "SHORT"

        return "HOLD"

    def learn(self, state, reward):
        self.weights += self.lr * reward * np.array(state)


# ==========================================================
# END OF PREDICTOR MODULE
# ==========================================================
