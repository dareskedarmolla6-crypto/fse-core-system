
# fse/execution/trade_router.py
import logging

logger = logging.getLogger(__name__)

# =========================================================
# SMART TRADE ROUTER (SMART EXECUTION ENTRY)
# =========================================================
class TradeRouter:
    """ምርጥ የዋጋ ምንጭ መርጦ ትዕዛዝ የሚልክ ክፍል (መርህ #6)።"""
    
    def __init__(self, exchanges):
        self.exchanges = exchanges  # { 'BINANCE': connector, 'BYBIT': connector }

    def execute_best(self, signal):
        target = self._select_best_exchange(signal)
        if target:
            return target.place_order(symbol=signal["symbol"], side=signal["side"], qty=signal["qty"])
        return None

    def _select_best_exchange(self, signal):
        # ለወደፊት ፈሳሽነትን (Liquidity) እና ክፍያን (Fees) ግምት ውስጥ የሚያስገባ logic ይጨመርበታል
        return self.exchanges.get("BINANCE")

# =========================================================
# EXECUTION CONTROL ENGINE
# =========================================================
class ExecutionControlEngine:
    """የውሳኔ አሰጣጥን ወደ ትዕዛዝ አይነት የሚቀይር።"""
    
    def execute_trade(self, decision):
        mapping = {
            "BUY": "OPEN_LONG", "STRONG_BUY": "OPEN_LONG",
            "SELL": "OPEN_SHORT", "STRONG_SELL": "OPEN_SHORT"
        }
        return mapping.get(decision, "NO_ACTION")

# =========================================================
# TAKE PROFIT ENGINE
# =========================================================
class TakeProfitEngine:
    """የትርፍ መቆለፊያ ስልት (Risk-Adjusted TP)።"""
    
    def manage_profit(self, position):
        profit = position.get("profit", 0)
        capital = position.get("capital", 1)
        
        if profit >= (0.25 * capital):
            return "LOCK_PROFIT"
        elif profit >= (0.10 * capital):
            return "PARTIAL_TP"
        return "HOLD"

# =========================================================
# MULTI-EXCHANGE ROUTER
# =========================================================
class MultiExchangeRouter:
    """በተለያዩ ልውውጦች መካከል ምርጥ ዋጋ መፈለጊያ።"""
    
    def __init__(self, exchanges):
        self.exchanges = exchanges

    def best_price(self, symbol):
        best_price = float('inf')
        best_exchange = None

        for name, ex in self.exchanges.items():
            try:
                price = float(ex.get_price(symbol))
                if price < best_price:
                    best_price = price
                    best_exchange = name
            except Exception as e:
                logger.error(f"❌ Error getting price from {name}: {e}")
        
        return best_exchange, best_price

    def place_order(self, symbol, side, qty):
        ex_name, price = self.best_price(symbol)
        if ex_name:
            logger.info(f"🚀 Routing order to {ex_name} at {price}")
            return self.exchanges[ex_name].place_order({
                "symbol": symbol, "side": side, "qty": qty, "price": price
            })
        return None

# =========================================================
# UNIFIED MARKET CONTROLLER
# =========================================================
class UnifiedMarketController:
    """የተዋሃደ የገበያ መቆጣጠሪያ።"""
    
    def __init__(self, router):
        self.router = router

    def route(self, symbol, side, qty):
        return self.router.place_order(symbol, side, qty)
