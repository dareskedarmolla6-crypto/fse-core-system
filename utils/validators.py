import re
import logging

logger = logging.getLogger("FSE")


# =========================
# SYMBOL VALIDATION
# =========================
def validate_symbol(symbol: str) -> bool:
    """
    Ensures trading symbol format is valid (e.g. BTCUSDT)
    """
    if not isinstance(symbol, str):
        logger.error("Symbol must be a string")
        return False

    pattern = r"^[A-Z0-9]{5,15}$"
    if not re.match(pattern, symbol):
        logger.error(f"Invalid symbol format: {symbol}")
        return False

    return True


# =========================
# SIDE VALIDATION
# =========================
def validate_side(side: str) -> bool:
    """
    Validates trade direction
    """
    valid_sides = ["LONG", "SHORT", "BUY", "SELL", "HEDGE"]
    if side not in valid_sides:
        logger.error(f"Invalid side: {side}")
        return False
    return True


# =========================
# QUANTITY VALIDATION
# =========================
def validate_quantity(qty: float) -> bool:
    """
    Ensures quantity is safe and non-zero
    """
    try:
        qty = float(qty)
    except Exception:
        logger.error("Quantity must be numeric")
        return False

    if qty <= 0:
        logger.error("Quantity must be > 0")
        return False

    if qty > 1_000_000:
        logger.error("Quantity too large (risk blocked)")
        return False

    return True


# =========================
# CONFIDENCE VALIDATION
# =========================
def validate_confidence(confidence: float) -> bool:
    """
    Ensures AI confidence is within safe range
    """
    try:
        confidence = float(confidence)
    except Exception:
        logger.error("Confidence must be numeric")
        return False

    if confidence < 0 or confidence > 100:
        logger.error("Confidence must be between 0 and 100")
        return False

    return True


# =========================
# SIGNAL VALIDATION (MAIN)
# =========================
def validate_signal(signal: dict) -> bool:
    """
    Central validation before execution engine
    """
    if not isinstance(signal, dict):
        logger.error("Signal must be a dictionary")
        return False

    required_fields = ["symbol", "side", "qty"]

    for field in required_fields:
        if field not in signal:
            logger.error(f"Missing field: {field}")
            return False

    if not validate_symbol(signal["symbol"]):
        return
