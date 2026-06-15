
# fse/portfolio/pnl_calculator.py
import logging

logger = logging.getLogger(__name__)

# =========================
# TRADE MEMORY (LEARNING ENGINE)
# =========================
class TradeMemory:
    """ያለፉትን የንግድ ልውውጦች ታሪክ እና የስኬት ምጣኔ የሚያከማች ክፍል (መርህ #1)።"""
    
    def __init__(self):
        self.history = []
        self.pattern_success = {}

    def record_trade(self, signal, pnl, regime):
        """ንግድን መመዝገብ እና የስኬት ምጣኔን ማዘመን።"""
        side = signal.get("side", "UNKNOWN")
        key = f"{side}_{regime}"

        self.history.append({
            "symbol": signal.get("symbol"),
            "side": side,
            "pnl": float(pnl),
            "regime": regime,
            "key": key
        })

        if key not in self.pattern_success:
            self.pattern_success[key] = {"wins": 0, "losses": 0}

        if pnl > 0:
            self.pattern_success[key]["wins"] += 1
        else:
            self.pattern_success[key]["losses"] += 1
        
        logger.info(f"🧠 Memory Updated: {key} | Wins: {self.pattern_success[key]['wins']} | Losses: {self.pattern_success[key]['losses']}")

# =========================
# MEMORY SIGNAL BOOSTER
# =========================
class MemorySignalBooster:
    """ባለፈው ልምድ መሰረት ሲግናሎችን የሚያሻሽል (Alpha Optimization)።"""
    
    def __init__(self, memory: TradeMemory):
        self.memory = memory

    def enhance(self, signal):
        """የሲግናልን ጥራት በ Memory Score ማሻሻል።"""
        regime = signal.get("regime", "UNKNOWN")
        key = f"{signal.get('side', 'UNKNOWN')}_{regime}"
        
        stats = self.memory.pattern_success.get(key)

        # ስታቲስቲክስ ከሌለ ገለልተኛ ውጤት መስጠት
        if not stats:
            score = 0.5
        else:
            total = stats["wins"] + stats["losses"]
            score = stats["wins"] / total if total > 0 else 0.5

        signal["memory_score"] = round(score, 3)
        
        # የሲግናልን አጠቃላይ ጥራት በታሪክ መሰረት ማሳደግ
        current_score = signal.get("score", 0)
        signal["score"] = current_score + int(score * 10)

        logger.info(f"🚀 Signal Enhanced: {signal.get('symbol')} | Memory Score: {signal['memory_score']}")
        return signal
