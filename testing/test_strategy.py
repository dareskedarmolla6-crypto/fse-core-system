
# fse/tests/test_strategy.py
import unittest
from strategy.strategy_router import StrategyRouter

# =========================
# TEST SUITE
# =========================
class TestStrategyRouter(unittest.TestCase):
    """የስልት መራጭ ማዕከልን (StrategyRouter) ትክክለኛነት የሚያረጋግጡ የሙከራ ትዕዛዞች።"""

    def setUp(self):
        self.router = StrategyRouter()

    def test_grid_strategy_selection(self):
        """ከፍተኛ ቮላቲሊቲ ሲኖር GRID ስልት መመረጡን ማረጋገጥ።"""
        market_data = {"volatility": 0.8, "trend": "NEUTRAL"}
        strategy = self.router.select_strategy(market_data)
        self.assertEqual(strategy, "GRID")

    def test_mean_reversion_selection(self):
        """ዝቅተኛ ቮላቲሊቲ ሲኖር MEAN_REVERSION ስልት መመረጡን ማረጋገጥ።"""
        market_data = {"volatility": 0.2, "trend": "NEUTRAL"}
        strategy = self.router.select_strategy(market_data)
        self.assertEqual(strategy, "MEAN_REVERSION")

    def test_momentum_strategy_selection(self):
        """አዝማሚያ (Trend) ወደ ላይ ሲሆን MOMENTUM ስልት መመረጡን ማረጋገጥ።"""
        market_data = {"volatility": 0.5, "trend": "UP"}
        strategy = self.router.select_strategy(market_data)
        self.assertEqual(strategy, "MOMENTUM")

    def test_default_alpha_selection(self):
        """ምንም ግልጽ ሁኔታ በሌለበት ጊዜ ALPHA ስልት መመረጡን ማረጋገጥ።"""
        market_data = {"volatility": 0.5, "trend": "DOWN"}
        strategy = self.router.select_strategy(market_data)
        self.assertEqual(strategy, "ALPHA")

if __name__ == "__main__":
    unittest.main()
