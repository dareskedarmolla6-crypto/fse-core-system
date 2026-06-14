import random


# =========================
# MARKET DATA SOURCE (MOCK / REAL READY)
# =========================
class FakeMarketSource:
    def __init__(self, coins=None):
        self.coins = coins or [
            "BTCUSDT", "ETHUSDT", "SOLUSDT",
            "DOGEUSDT", "PEPEUSDT", "ARBUSDT"
        ]

    def get_all(self):
        data = {}

        for coin in self.coins:
            data[coin] = {
                "volatility": random.uniform(0.1, 2.5),
                "volume": random.uniform(1_000, 1_000_000),
                "momentum": random.uniform(-1, 1),
                "price_change": random.uniform(-5, 5)
            }

        return data


# =========================
# MARKET FEED WRAPPER
# =========================
class MarketFeed:
    def __init__(self, market_data_source):
        self.source = market_data_source

    def get_snapshot(self):
        return self.source.get_all()

    def get_symbol_data(self, symbol):
        data = self.source.get_all()
        return data.get(symbol, None)
