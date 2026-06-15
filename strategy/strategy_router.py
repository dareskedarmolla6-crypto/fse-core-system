


# fse/strategy/strategy_router.py
import logging
from strategy.alpha_strategy import AlphaStrategy
from strategy.grid_strategy import GridStrategy
from strategy.momentum_strategy import MomentumStrategy
from strategy.mean_reversion import MeanReversion

logger = logging.getLogger(__name__)

# =========================
# STRATEGY ROUTER (CORE)
# =========================
class StrategyRouter:
    """የገበያ ሁኔታን መሰረት በማድረግ ምርጡን ስልት የሚመርጥ ማዕከል (መርህ #3)።"""

    def __init__(self):
        self.strategies = {
            "ALPHA": AlphaStrategy(),
            "GRID": GridStrategy(),
            "MOMENTUM": MomentumStrategy(),
            "MEAN_REVERSION": MeanReversion()
        }

    def select_strategy(self, market_data):
        """የገበያ ሁኔታን (Volatility/Trend) መተንተን።"""
        volatility = float(market_data.get("volatility", 0.5))
        trend = market_data.get("trend", "NEUTRAL")

        if volatility > 0.7:
            return "GRID"
        elif volatility < 0.3:
            return "MEAN_REVERSION"
        elif trend == "UP":
            return "MOMENTUM"
        else:
            return "ALPHA"

    def route(self, market_data):
        """ስልቱን በመምረጥ ወደ ማዕከላዊ ማስፈጸሚያ መላክ።"""
        strategy_name = self.select_strategy(market_data)
        strategy = self.strategies.get(strategy_name)

        if not strategy:
            logger.error(f"❌ Strategy not found: {strategy_name}")
            return None

        result = strategy.execute(market_data)
        logger.info(f"🛣 Strategy Routed: {strategy_name} | Action: {result.get('action')}")
        
        return {
            "strategy": strategy_name,
            "result": result
        }
