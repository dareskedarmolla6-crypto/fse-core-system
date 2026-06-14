from strategy.alpha_strategy import AlphaStrategy
from strategy.grid_strategy import GridStrategy
from strategy.momentum_strategy import MomentumStrategy
from strategy.mean_reversion import MeanReversion


# =========================
# STRATEGY ROUTER (CORE)
# =========================
class StrategyRouter:
    def __init__(self):
        self.strategies = {
            "ALPHA": AlphaStrategy(),
            "GRID": GridStrategy(),
            "MOMENTUM": MomentumStrategy(),
            "MEAN_REVERSION": MeanReversion()
        }

    def select_strategy(self, market_data):
        """
        Simple selector (later AI can replace this)
        """
        volatility = market_data.get("volatility", 0.5)

        if volatility > 0.7:
            return "GRID"
        elif volatility < 0.3:
            return "MEAN_REVERSION"
        elif market_data.get("trend") == "UP":
            return "MOMENTUM"
        else:
            return "ALPHA"

    def route(self, market_data):
        strategy_name = self.select_strategy(market_data)

        strategy = self.strategies.get(strategy_name)
        if not strategy:
            return None

        return {
            "strategy": strategy_name,
            "result": strategy.execute(market_data)
        }
