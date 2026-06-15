# ==========================================================
# FSE GLOBAL SETTINGS (OPERATIONAL CONFIG)
# ==========================================================
import logging

logger = logging.getLogger(__name__)

class Settings:
    """የቦቱን የስራ መቼቶች የሚቆጣጠር ክፍል (መርህ #7 & #8)"""

    # Market Scan Interval (3 ደቂቃ - መርህ #6)
    INTERVAL = 180  

    # ከፍተኛ የአንድ ጊዜ ክፍት ቦታዎች (መርህ #9)
    MAX_OPEN_POSITIONS = 20

    # Minimum confidence (መርህ #4)
    CONFIDENCE_THRESHOLD = 15

    # Trading mode
    MODE = "ALPHA_ONLY"

    # Focus only on high volatility coins (መርህ #4)
    MIN_VOLATILITY_PERCENT = 15

    # Supported trading styles
    ENABLE_LONG = True
    ENABLE_SHORT = True
    ENABLE_HEDGE = True
    ENABLE_GRID = True

    # Leverage limits (መርህ #8)
    MIN_LEVERAGE = 5
    MAX_LEVERAGE = 35 

    # FSE confidence-based leverage map
    LEVERAGE_LEVELS = {
        (15, 25): 5,
        (26, 35): 8,
        (36, 55): 10,
        (56, 75): 15,
        (76, 85): 20,
        (86, 100): 30
    }

def validate_settings():
    """የመቼቶች መጣጣምን ማረጋገጥ።"""
    if Settings.MIN_LEVERAGE < 5 or Settings.MAX_LEVERAGE > 35:
        logger.error("🚨 Configuration Error: Leverage out of safe bounds!")
        return False
    if Settings.CONFIDENCE_THRESHOLD < 15:
        logger.warning("⚠️ Low confidence threshold detected.")
    logger.info("✅ FSE Settings validated successfully.")
    return True

# አጠቃላይ የመቼት መጫኛ አፈጻጸም
validate_settings()
