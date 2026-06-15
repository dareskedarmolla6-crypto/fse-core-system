# =====================================================
# FSE GLOBAL CONSTANTS (CORE SYSTEM CONFIG)
# =====================================================

# System Settings
BOT_NAME = "FSE"
BOT_VERSION = "2.0.0" # አዘምነነዋል
SCAN_INTERVAL_SECONDS = 180   # 3 ደቂቃ (መርህ #6)

# Market Requirements
MIN_CONFIDENCE = 15
MIN_VOLATILITY_PERCENT = 15 # መርህ #4

# Confidence → Leverage Mapping (መርህ #8)
# (Min_Conf, Max_Conf): Leverage
LEVERAGE_LEVELS = {
    (15, 25): 5,
    (26, 35): 8,
    (36, 55): 10,
    (56, 75): 15,
    (76, 85): 20,
    (86, 100): 30
}
MAX_LEVERAGE = 35 # የቦትህን ከፍተኛ አቅም መሰረት ያደረገ

# Trading Modes
LONG, SHORT, HEDGE, GRID = "LONG", "SHORT", "HEDGE", "GRID"
NO_TRADE = "NO_TRADE"

# Risk Management
STOP_LOSS_ENABLED = True
TRAILING_STOP_ENABLED = True
TRAILING_ACTIVATION_PERCENT = 0.05
TRAILING_DISTANCE_PERCENT = 0.02
PARTIAL_TAKE_PROFIT_ENABLED = True
PARTIAL_TP_PERCENT = 0.10 # መርህ #5 (Grid System/Partial Selling)
PROFIT_LOCK_ENABLED = True
PROFIT_LOCK_PERCENT = 0.25

# Market/Exchange Support (መርህ #10)
CRYPTO_EXCHANGES = ["BINANCE", "BYBIT", "OKX", "KUCOIN", "GATE_IO", "MEXC", "BITGET"]
FOREX_BROKERS = ["MT5", "OANDA", "IC_MARKETS", "PEPPERSTONE", "EXNESS"]

# System States
SYSTEM_RUNNING, SYSTEM_STOPPED, SYSTEM_EMERGENCY = "RUNNING", "STOPPED", "EMERGENCY"

# Order States
ORDER_CREATED, ORDER_OPEN, ORDER_FILLED, ORDER_CLOSED, ORDER_FAILED = \
    "CREATED", "OPEN", "FILLED", "CLOSED", "FAILED"

# Default Symbol
DEFAULT_SYMBOL = "BTCUSDT" # DOGEUSDT ተለዋዋጭ ስለሆነ BTCUSDT ለጅምር ይሻላል
