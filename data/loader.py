
# fse/data/loader.py
import random
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# =========================
# CANDLE MODEL
# =========================
class Candle:
    """የገበያ መረጃን በአንድ ሻማ (Candle) መልክ የሚያዋቅር ክፍል (መርህ #3)።"""
    
    def __init__(self, open_, high, low, close, volume):
        self.open = float(open_)
        self.high = float(high)
        self.low = float(low)
        self.close = float(close)
        self.volume = float(volume)
        self.timestamp = datetime.utcnow()

# =========================
# MARKET DATA LOADER (SIMULATED)
# =========================
class MarketDataLoader:
    """የገበያ ዋጋዎችን እና ሻማዎችን የሚያመነጭ (ሲሙሌሽን)።"""
    
    def __init__(self):
        self.last_price = 100.0

    def fetch_price(self, symbol):
        """የገበያ ዋጋን ማስመሰል።"""
        change = random.uniform(-2, 2)
        self.last_price = max(0.01, self.last_price + change)
        return round(self.last_price, 4)

    def generate_candle(self, symbol):
        """የገበያ ሻማ መረጃን ማመንጨት።"""
        try:
            open_price = self.fetch_price(symbol)
            high = open_price + random.uniform(0, 2)
            low = open_price - random.uniform(0, 2)
            close = self.fetch_price(symbol)
            volume = random.uniform(10, 1000)
            return Candle(open_price, high, low, close, volume)
        except Exception as e:
            logger.error(f"❌ Error generating candle for {symbol}: {e}")
            return None

# =========================
# STREAM LOADER
# =========================
class MarketStream:
    """የገበያ መረጃን በየጊዜው የሚያስተላልፍ (Streaming) ክፍል (መርህ #6)።"""
    
    def __init__(self, symbol="DOGEUSDT"):
        self.symbol = symbol
        self.loader = MarketDataLoader()
        self.active = False

    def stream(self):
        """የገበያ መረጃን የሚያስተላልፍ Generator።"""
        self.active = True
        logger.info(f"📡 Starting market stream for {self.symbol}...")
        try:
            while self.active:
                candle = self.loader.generate_candle(self.symbol)
                if candle:
                    yield candle
        except Exception as e:
            logger.error(f"❌ Stream error: {e}")
            self.active = False
