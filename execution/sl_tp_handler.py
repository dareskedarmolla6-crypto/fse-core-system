# fse/execution/sl_tp_handler.py


# =========================================================
# SMART ORDER ENHANCER
# =========================================================
class SmartOrderEnhancer:
    def enhance(self, signal, market_data):
        volatility = market_data.get("volatility", 0.5)

        # position sizing adjustment based on volatility
        signal["qty"] = max(
            0.1,
            signal.get("qty", 1) * (1 - volatility)
        )

        return signal


# =========================================================
# TRAILING STOP CONFIG
# =========================================================
class TrailingConfig:
    def __init__(self):
        # activation profit threshold (5%)
        self.activation = 0.05

        # trailing distance (2%)
        self.distance = 0.02


# =========================================================
# TRAILING STOP ENGINE
# =========================================================
class TrailingEngine:
    def __init__(self, config=None):
        self.config = config or TrailingConfig()

    def update(self, position, price):
        """
        Updates stop loss when trailing condition is met.
        Works for both LONG and SHORT positions.
        """

        # LONG POSITION
        if position.side == "BUY":
            trigger_price = position.entry_price * (1 + self.config.activation)

            if price > trigger_price:
                new_sl = price * (1 - self.config.distance)
                position.stop_loss = new_sl
                return new_sl

        # SHORT POSITION
        else:
            trigger_price = position.entry_price * (1 - self.config.activation)

            if price < trigger_price:
                new_sl = price * (1 + self.config.distance)
                position.stop_loss = new_sl
                return new_sl

        return None
