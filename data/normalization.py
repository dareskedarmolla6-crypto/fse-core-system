
# fse/data/normalization.py
import math
import logging

logger = logging.getLogger(__name__)

class DataNormalizer:
    """የገበያ መረጃዎችን ለቦቱ ስልተ-ቀመር የሚያዘጋጅ (መርህ #3 & #4)።"""

    def __init__(self):
        self.min_max_cache = {}

    def safe_float(self, value):
        """የተሳሳተ መረጃ (None/String) ሲመጣ ስህተት እንዳይፈጠር መከላከል (Safety Guard)።"""
        try:
            return float(value)
        except (TypeError, ValueError):
            return 0.0

    def min_max(self, value, min_val, max_val):
        value = self.safe_float(value)
        if max_val == min_val:
            return 0.0
        return (value - min_val) / (max_val - min_val)

    def z_score(self, value, mean, std):
        value = self.safe_float(value)
        if std == 0:
            return 0.0
        return (value - mean) / std

    def normalize_price_change(self, price_change):
        """ዋጋን በ -1 እና 1 መካከል ማመጣጠን።"""
        price_change = self.safe_float(price_change)
        return max(-1.0, min(1.0, price_change / 10.0))

    def normalize_volume(self, volume, max_volume=1000):
        """ቮሊዩምን መደበኛ ማድረግ (ከፍተኛው 1.0)።"""
        volume = self.safe_float(volume)
        return min(volume / max_volume, 1.0)

    def volatility_score(self, price_changes):
        """የገበያ መዋዠቅን ማስላት (Standard Deviation)።"""
        if not price_changes or len(price_changes) == 0:
            return 0.0
        
        data = [self.safe_float(x) for x in price_changes]
        avg = sum(data) / len(data)
        variance = sum((x - avg) ** 2 for x in data) / len(data)
        return math.sqrt(variance) / 10.0 

    def build_features(self, market_data):
        """ለአልጎሪዝም የሚያስፈልጉ መለኪያዎችን ማዘጋጀት።"""
        try:
            return {
                "price_change_norm": self.normalize_price_change(
                    market_data.get("price_change", 0)
                ),
                "volume_norm": self.normalize_volume(
                    market_data.get("volume", 0)
                ),
                "volatility": self.volatility_score(
                    market_data.get("history", [])
                )
            }
        except Exception as e:
            logger.error(f"❌ Feature build error: {e}")
            return {"price_change_norm": 0, "volume_norm": 0, "volatility": 0}
