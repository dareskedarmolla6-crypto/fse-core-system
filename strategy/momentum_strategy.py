import time


class MomentumStrategy:
    """
    Momentum Strategy:
    - Follows price direction (velocity)
    - Uses current price vs average price
    """

    def __init__(self, lookback_window=5):
        self.lookback_window = lookback_window
        self.prices = []

    # =========================
    # PRICE FEED UPDATE
    # =========================
    def update(self, price):
        self.prices.append(price)

        if len(self.prices) > self.lookback_window:
            self.prices.pop(0)

    # =========================
    # AVERAGE PRICE
    # =========================
    def get_average(self):
        if not self.prices:
            return 0
        return sum(self.prices) / len(self.prices)

    # =========================
    # DECISION ENGINE
    # =========================
    def decide(self, price_now):
        price_avg = self.get_average()

        if price_avg == 0:
            return "HOLD"

        if price_now > price_avg * 1.01:
            return "LONG"

        elif price_now < price_avg * 0.99:
            return "SHORT"

        return "HOLD"

    # =========================
    # OPTIONAL EXECUTE WRAPPER
    # =========================
    def execute(self, market_data):
        price = market_data.get("price", 0)

        self.update(price)
        decision = self.decide(price)

        print(f"⚡ Momentum Decision: {decision} | Price: {price}")

        return {
            "strategy": "MOMENTUM",
            "action": decision,
            "price": price
        }ረ
