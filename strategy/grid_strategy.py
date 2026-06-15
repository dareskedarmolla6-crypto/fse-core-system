# fse/strategy/grid_strategy.py
import logging

logger = logging.getLogger(__name__)

# =========================
# GRID TRADING STRATEGY
# =========================
class GridStrategy:
    """የገበያ ዋጋዎችን በረድፍ (Grid) በመከፋፈል ንግድ የሚያካሂድ (መርህ #3)።"""

    def __init__(self, levels=5):
        self.levels = int(levels)

    def generate_levels(self, base_price, step_pct=0.5):
        """የዋጋ ደረጃዎችን (Price Levels) መፍጠር።"""
        levels = []
        base = float(base_price)
        step = float(step_pct) / 100.0

        for i in range(1, self.levels + 1):
            lower = base * (1.0 - (step * i))
            upper = base * (1.0 + (step * i))
            levels.append({"buy": round(lower, 4), "sell": round(upper, 4)})

        return levels

    def execute(self, executor, symbol, base_size, base_price):
        """የGrid ትዕዛዞችን ማስፈጸም (Execution Orchestration)።"""
        levels = self.generate_levels(base_price)
        orders = []
        step_size = float(base_size) / self.levels

        for level in levels:
            # የBUY ትዕዛዞችን በዝቅተኛ የዋጋ ደረጃዎች ማስቀመጥ
            buy_order = executor.open_long(symbol, step_size)
            orders.append({"type": "BUY", "price": level["buy"], "order": buy_order})
        
        logger.info(f"🕸 Grid Strategy: {len(orders)} orders placed for {symbol}.")
        
        return {
            "strategy": "GRID",
            "symbol": symbol,
            "orders": orders,
            "status": "GRID_PLACED"
        }

