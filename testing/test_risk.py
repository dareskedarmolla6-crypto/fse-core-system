import unittest


# =========================
# SIMPLE RISK ENGINE (for testing)
# =========================
class RiskAI:
    def approve_trade(self, signal, confidence, leverage=3):
        if confidence < 55:
            return False, "LOW CONFIDENCE"
        if leverage > 20:
            return False, "LEVERAGE TOO HIGH"
        return True, "OK"

    def position_size(self, balance, confidence):
        return balance * (confidence / 1000)


# =========================
# TEST CASES
# =========================
class TestRiskAI(unittest.TestCase):

    def setUp(self):
        self.risk = RiskAI()

    # -------- approval tests --------
    def test_low_confidence_rejected(self):
        approved, reason = self.risk.approve_trade("LONG", 40)
        self.assertFalse(approved)
        self.assertEqual(reason, "LOW CONFIDENCE")

    def test_high_confidence_approved(self):
        approved, reason = self.risk.approve_trade("LONG", 80)
        self.assertTrue(approved)
        self.assertEqual(reason, "OK")

    def test_high_leverage_rejected(self):
        approved, reason = self.risk.approve_trade("LONG", 80, leverage=30)
        self.assertFalse(approved)
        self.assertEqual(reason, "LEVERAGE TOO HIGH")

    # -------- position sizing --------
    def test_position_size_calculation(self):
        size = self.risk.position_size(1000, 80)
        self.assertAlmostEqual(size, 80.0)

    def test_position_size_zero_confidence(self):
        size = self.risk.position_size(1000, 0)
        self.assertEqual(size, 0)


# =========================
# RUN TESTS
# =========================
if __name__ == "__main__":
    unittest.main()
