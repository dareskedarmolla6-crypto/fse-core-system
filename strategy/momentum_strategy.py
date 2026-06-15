
# fse/strategy/momentum_strategy.py
import logging

logger = logging.getLogger(__name__)

class MomentumStrategy:
    """
    Momentum Strategy: የዋጋ አቅጣጫን (Velocity) የሚከተል (መርህ #3)።
    """

    def __init__(self, lookback_window=5):
        self.lookback_window = lookback_window
        self.prices = []

    def update(self, price):
        """የዋጋ መረጃን ማዘመን።"""
        self.prices.append(float(price))
        if len(self.prices) > self.lookback_window:
            self.prices.pop(0)

    def get_average(self):
        """አማካይ ዋጋን ማስላት።"""
        if not self.prices:
            return 0.0
        return sum(self.prices) / len(self.prices)

    def decide(self, price_now):
        """የገበያ ውሳኔ ሰጪ (Decision Engine)።"""
        price_avg = self.get_average()
        if price_avg <= 0:
            return "HOLD"

        # 1% threshold ለMomentum ማጣሪያ
        if price_now > price_avg * 1.01:
            return "LONG"
        elif price_now < price_avg * 0.99:
            return "SHORT"

        return "HOLD"

    def execute(self, market_data):
        """የስልቱ ዋና ማስፈጸሚያ።"""
        price = float(market_data.get("price", 0))
        self.update(price)
        action = self.decide(price)

        logger.info(f"⚡ Momentum Strategy: {action} | Price: {price}")

        return {
            "strategy": "MOMENTUM",
            "action": action,
            "price": price,
            "timestamp": market_data.get("timestamp")
        }
