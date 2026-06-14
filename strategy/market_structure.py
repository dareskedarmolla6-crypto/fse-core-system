class SwingDetector:
    def __init__(self, window=3):
        self.window = window

    def detect_swings(self, candles):
        if len(candles) < self.window * 2:
            return []

        swings = []

        for i in range(self.window, len(candles) - self.window):

            if all(candles[i].high > candles[i - j].high for j in range(1, self.window + 1)) and \
               all(candles[i].high > candles[i + j].high for j in range(1, self.window + 1)):

                swings.append({
                    "type": "HIGH",
                    "price": candles[i].high,
                    "time": candles[i].open_time,
                    "label": "HH"
                })

            elif all(candles[i].low < candles[i - j].low for j in range(1, self.window + 1)) and \
                 all(candles[i].low < candles[i + j].low for j in range(1, self.window + 1)):

                swings.append({
                    "type": "LOW",
                    "price": candles[i].low,
                    "time": candles[i].open_time,
                    "label": "LL"
                })

        return swings


class BOSDetector:
    def __init__(self):
        self.last_swing = None

    def check_bos(self, current_swing):
        if self.last_swing is None:
            self.last_swing = current_swing
            return None

        # Bullish BOS
        if current_swing["label"] == "HH" and self.last_swing["label"] == "HH" and \
           current_swing["price"] > self.last_swing["price"]:

            self.last_swing = current_swing
            return "BULLISH_BOS"

        # Bearish BOS
        if current_swing["label"] == "LL" and self.last_swing["label"] == "LL" and \
           current_swing["price"] < self.last_swing["price"]:

            self.last_swing = current_swing
            return "BEARISH_BOS"

        self.last_swing = current_swing
        return None


class LiquiditySweepDetector:
    def detect_sweep(self, current_candle, previous_swing):

        if not previous_swing:
            return None

        if previous_swing["type"] == "HIGH":
            if current_candle.high > previous_swing["price"] and current_candle.close < previous_swing["price"]:
                return "BUY_SIDE_LIQUIDITY_SWEEP"

        if previous_swing["type"] == "LOW":
            if current_candle.low < previous_swing["price"] and current_candle.close > previous_swing["price"]:
                return "SELL_SIDE_LIQUIDITY_SWEEP"

        return None


class FVGDetector:
    def detect_fvg(self, c1, c2, c3, min_size_multiplier=1.2):

        if not (c1 and c2 and c3):
            return None

        body_size = abs(c2.high - c2.low)

        if c3.low > c1.high and (c3.low - c1.high) > body_size * min_size_multiplier:
            return {
                "type": "BULLISH_FVG",
                "top": c3.low,
                "bottom": c1.high
            }

        if c1.low > c3.high and (c1.low - c3.high) > body_size * min_size_multiplier:
            return {
                "type": "BEARISH_FVG",
                "top": c1.low,
                "bottom": c3.high
            }

        return None


class MarketStructureEngine:
    def __init__(self):
        self.swing = SwingDetector()
        self.bos = BOSDetector()
        self.liquidity = LiquiditySweepDetector()
        self.fvg = FVGDetector()

    def evaluate(self, candles):
        if not candles or len(candles) < 5:
            return "NO_TRADE"

        swings = self.swing.detect_swings(candles)
        if not swings:
            return "NO_TRADE"

        last_swing = swings[-1]

        bos_signal = self.bos.check_bos(last_swing)
        if bos_signal:
            return bos_signal

        sweep_signal = self.liquidity.detect_sweep(candles[-1], last_swing)
        if sweep_signal:
            return sweep_signal

        # optional FVG check (safe, non-blocking)
        if len(candles) >= 3:
            fvg = self.fvg.detect_fvg(candles[-3], candles[-2], candles[-1])
            if fvg:
                return fvg["type"]

        return "NO_TRADE"
