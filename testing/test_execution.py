
# fse/tests/test_execution.py
import unittest
from risk.risk_manager import RiskEngine, PositionSizer

# =========================
# MOCK EXECUTION ENGINE
# =========================
class MockExecution:
    """የንግድ አፈጻጸምን የሚመስል (Mock) ሞጁል ለሙከራ።"""
    def __init__(self):
        self.trades = []

    def execute_trade(self, symbol, side, size):
        trade = {"symbol": symbol, "side": side, "size": size, "status": "EXECUTED"}
        self.trades.append(trade)
        return trade

# =========================
# TEST SUITE
# =========================
class TestExecutionFlow(unittest.TestCase):
    """የንግድ አፈጻጸም ፍሰትን የሚያረጋግጡ የሙከራ ትዕዛዞች።"""

    def setUp(self):
        self.executor = MockExecution()
        self.risk = RiskEngine(max_risk=0.02)
        self.sizer = PositionSizer(max_risk=0.02)
        self.balance = 1000.0

    def test_full_trade_flow(self):
        """ሲግናል -> ሪስክ ፍተሻ -> አፈጻጸም ያለውን ሂደት ማረጋገጥ።"""
        signal = "LONG"
        confidence = 80
        
        # 1. ሪስክ ፍተሻ
        size = self.sizer.calculate(self.balance, confidence)
        approved, _ = self.risk.validate_new_position(signal, self.balance, size, [])
        
        # 2. አፈጻጸም
        if approved:
            trade = self.executor.execute_trade("DOGEUSDT", signal, size)
            
            # 3. ማረጋገጫ (Assertions)
            self.assertEqual(trade["side"], "LONG")
            self.assertEqual(trade["symbol"], "DOGEUSDT")
            self.assertEqual(trade["size"], 16.0) # 1000 * 0.02 * 0.8
            self.assertEqual(trade["status"], "EXECUTED")

    def test_rejection_on_excessive_size(self):
        """ከፍተኛ መጠን ያለው ንግድ መታገዱን ማረጋገጥ።"""
        size = 500.0 # 50% risk (በጣም ከፍተኛ)
        approved, reason = self.risk.validate_new_position("LONG", self.balance, size, [])
        self.assertFalse(approved)
        self.assertEqual(reason, "RISK_TOO_HIGH")

if __name__ == "__main__":
    unittest.main()
