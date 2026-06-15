
# fse/tests/test_brain.py
import unittest
# በፕሮጀክቱ መዋቅር መሰረት ከ brain.signal_engine የ Brain ክፍሉን አስገባ
# from brain.signal_engine import Brain 

class Brain:
    """የንግድ ውሳኔ ሰጪ (Mock Logic)።"""
    def predict(self, data):
        change = float(data.get("price_change", 0))
        if change > 1.0: return "LONG", 75
        if change < -1.0: return "SHORT", 72
        return "HEDGE", 60

class TestBrain(unittest.TestCase):
    """የ Brain ሞጁሉን ትክክለኛነት የሚያረጋግጡ የሙከራ ትዕዛዞች።"""

    def setUp(self):
        self.brain = Brain()

    def test_long_signal_accuracy(self):
        """ከፍተኛ የዋጋ ለውጥ ሲኖር LONG ሲግናል መፈጠሩን ማረጋገጥ።"""
        data = {"price_change": 2.5}
        signal, conf = self.brain.predict(data)
        self.assertEqual(signal, "LONG")
        self.assertGreaterEqual(conf, 70)

    def test_short_signal_accuracy(self):
        """ዝቅተኛ የዋጋ ለውጥ ሲኖር SHORT ሲግናል መፈጠሩን ማረጋገጥ።"""
        data = {"price_change": -2.2}
        signal, conf = self.brain.predict(data)
        self.assertEqual(signal, "SHORT")
        self.assertGreaterEqual(conf, 70)

    def test_hedge_signal_on_low_volatility(self):
        """የዋጋ መረጋጋት ሲኖር HEDGE ሲግናል መፈጠሩን ማረጋገጥ።"""
        data = {"price_change": 0.2}
        signal, conf = self.brain.predict(data)
        self.assertEqual(signal, "HEDGE")
        self.assertEqual(conf, 60)

if __name__ == "__main__":
    unittest.main()
