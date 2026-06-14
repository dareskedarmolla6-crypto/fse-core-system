# fse/strategy/smc_strategy.py

from dataclasses import dataclass


# =========================
# CANDLE MODEL (simple)
# =========================
@dataclass
class Candle:
    open: float
    high: float
    low: float
    close: float


# =========================
# SMC STRATEGY ENGINE
# =========================
class SMCStrategy:
    """
    Smart Money Concept simplified:
    - Liquidity sweep
    - Market structure shift (BOS)
    - Premium / Discount logic
    """

    def __init__(self):
        self.last_high = None
        self.last_low = None

    # -------------------------
    # Detect market structure
    # -------------------------
    def detect_structure(self, candles):
        if len(candles) < 3:
            return "NO_DATA"

        highs = [c.high for c in candles]
        lows = [c.low for c in candles]

        current_high = max(highs)
        current_low = min(lows)

        # Initialize
        if self.last_high is None:
            self.last_high = current_high
            self.last_low = current_low
            return "INITIALIZED"

        # Break of Structure (BOS)
        if current_high > self.last_high:
            self.last_high = current_high
            return "BULLISH_BOS"

        if current_low < self.last_low:
            self.last_low = current_low
            return "BEARISH_BOS"

        return "RANGE"


    # -------------------------
    # Liquidity sweep detection
    # -------------------------
    def liquidity_sweep(self, candles):
        last = candles[-1]

        if self.last_high and last.high > self.last_high and last.close < self.last_high:
            return "SELL_SIDE_SWEEP"

        if self.last_low and last.low < self.last_low and last.close > self.last_low:
            return "BUY_SIDE_SWEEP"

        return None


    # -------------------------
    # Premium / Discount zone
    # -------------------------
    def zone(self, candles):
        high = max(c.high for c in candles)
        low = min(c.low for c in candles)

        eq = (high +
