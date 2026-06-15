
# fse/utils/helpers.py
import time
import uuid
import hashlib
import random
import logging

logger = logging.getLogger("FSE.Helpers")

# =========================
# IDENTIFICATION & SAFETY (CORE)
# =========================

def generate_idempotency_key(symbol: str, side: str, qty: float, strategy_id: str, bucket: int = None) -> str:
    """
    መርህ #11: ተመሳሳይ ንግድ ደጋግሞ እንዳይላክ (Duplicate Trade Prevention) 
    የሚከላከል የደህንነት ቁልፍ ማመንጫ።
    """
    if bucket is None:
        bucket = int(time.time() // 60)  # 1-minute window
    
    raw = f"{symbol}:{side}:{qty}:{strategy_id}:{bucket}"
    return hashlib.sha256(raw.encode()).hexdigest()

def short_id(prefix: str = "BOT") -> str:
    """ለአጭር መታወቂያዎች ማመንጫ።"""
    return f"{prefix}_{uuid.uuid4().hex[:12]}"

# =========================
# TRADING CALCULATIONS
# =========================

def calculate_position_size(balance: float, risk_percent: float) -> float:
    """መርህ #7: ደህንነቱ የተጠበቀ የካፒታል ስሌት።"""
    return balance * (max(0, risk_percent) / 100)

def safe_qty(qty: float, min_qty: float = 0.001) -> float:
    """የንግድ መጠንን ከዝቅተኛው ገደብ ጋር ማነፃፀሪያ።"""
    return max(float(qty), min_qty)

# =========================
# MARKET UTILS
# =========================

def is_volatile(price_change: float, threshold: float = 2.0) -> bool:
    """መርህ #1: የቮላቲሊቲ ማጣሪያ።"""
    return abs(price_change) >= threshold

def direction_from_change(price_change: float) -> str:
    """የገበያ አቅጣጫ መለያ።"""
    if price_change > 0.1: return "UP"
    if price_change < -0.1: return "DOWN"
    return "FLAT"

# =========================
# TESTING UTILS
# =========================

def fake_market_data(symbol: str = "DOGEUSDT") -> dict:
    """ለሙከራ ብቻ የሚያገለግል የገበያ መረጃ ማስመሰያ።"""
    return {
        "symbol": symbol,
        "price_change": round(random.uniform(-3.0, 3.0), 2),
        "volume": round(random.uniform(10.0, 100.0), 2)
    }
