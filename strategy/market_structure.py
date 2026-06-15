
# fse/strategy/market_structure.py
import logging

logger = logging.getLogger(__name__)

# =========================
# MARKET STRUCTURE COMPONENTS
# =========================
class SwingDetector:
    """የዋጋ መወጣጫ እና መውረጃ ነጥቦችን (HH/LL) ለይቶ የሚያወጣ።"""
    def __init__(self, window=3):
        self.window = window

    def detect_swings(self, candles):
        if len(candles) < self.window * 2: return []
        swings = []
        for i in range(self.window, len(candles) - self.window):
            if all(candles[i].high > candles[i-j].high for j in range(1, self.window+1)) and \
               all(candles[i].high > candles[i+j].high for j in range(1, self.window+1)):
                swings.append({"type": "HIGH", "price": candles[i].high, "time": candles[i].open_time, "label": "HH"})
            elif all(candles[i].low < candles[i-j].low for j in range(1, self.window+1)) and \
                 all(candles[i].low < candles[i+j].low for j in range(1, self.window+1)):
                swings.append({"type": "LOW", "price": candles[i].low, "time": candles[i].open_time, "label": "LL"})
        return swings

class BOSDetector:
    """የገበያ አዝማሚያ መቀየርን (Break of Structure) መከታተያ።"""
    def __init__(self):
        self.last_swing = None

    def check_bos(self, current_swing):
        if self.last_swing is None:
            self.last_swing = current_swing
            return None
        if current_swing["label"] == "HH" == self.last_swing["label"] and current_swing["price"] > self.last_swing["price"]:
            self.last_swing = current_swing
            return "BULLISH_BOS"
        if current_swing["label"] == "LL" == self.last_swing["label"] and current_swing["price"] < self.last_swing["price"]:
            self.last_swing = current_swing
            return "BEARISH_BOS"
        self.last_swing = current_swing
        return None

class FVGDetector:
    """የገበያ አለመመጣጠንን (Fair Value Gap) መለየት።"""
    def detect_fvg(self, c1, c2, c3, min_size_mult=1.2):
        if not (c1 and c2 and c3): return None
        body_size = abs(c2.high - c2.low)
        if c3.low > c1.high and (c3.low - c1.high) > body_size * min_size_mult:
            return {"type": "BULLISH_FVG", "top": c3.low, "bottom": c1.high}
        if c1.low > c3.high and (c1.low - c3.high) > body_size * min_size_mult:
            return {"type": "BEARISH_FVG", "top": c1.low, "bottom": c3.high}
        return None

# =========================
# MARKET STRUCTURE ENGINE
# =========================
class MarketStructureEngine:
    """የመዋቅር መለኪያ ዋና ክፍል (መርህ #3)።"""
    def __init__(self):
        self.swing = SwingDetector()
        self.bos = BOSDetector()
        self.fvg = FVGDetector()

    def evaluate(self, candles):
        """የገበያ መዋቅርን በመገምገም ሲግናል ማውጣት።"""
        if len(candles) < 5: return "NO_TRADE"
        swings = self.swing.detect_swings(candles)
        if not swings: return "NO_TRADE"

        last_swing = swings[-1]
        bos_signal = self.bos.check_bos(last_swing)
        if bos_signal: return bos_signal

        if len(candles) >= 3:
            fvg = self.fvg.detect_fvg(candles[-3], candles[-2], candles[-1])
            if fvg: return fvg["type"]

        return "NO_TRADE"
