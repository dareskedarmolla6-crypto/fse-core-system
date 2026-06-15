
# fse/monitoring/performance_monitor.py
import logging

logger = logging.getLogger(__name__)

# =========================
# RELIABILITY ORCHESTRATOR
# =========================
class ReliabilityOrchestrator:
    """ሲስተሙ ከገበያ ጋር ተመሳስሎ እንዲቀጥል የሚያደርግ (Self-Healing) ክፍል (መርህ #6)።"""
    
    def __init__(self, store, gateway):
        self.store = store
        self.gateway = gateway

    def rebuild_state(self):
        """የጠፉ ወይም የተዛቡ ትዕዛዞችን ማስተካከል (Reconciliation)።"""
        for trade in self.store.get_active_trades():
            order = self.gateway.query_order(trade["symbol"], trade.get("order_id"))
            position = self.gateway.query_position(trade["symbol"])
            drift = self._detect_drift(trade, order, position)

            if drift:
                self._repair(trade, drift)

    def _detect_drift(self, trade, order, position):
        if order and order.get("status") == "FILLED" and trade.get("status") != "FILLED":
            return "STATE_DRIFT"
        if not order:
            return "ORPHAN_ORDER"
        if position and float(position.get("positionAmt", 0)) != 0 and not order:
            return "ORPHAN_POSITION"
        return None

    def _repair(self, trade, drift):
        attempts = trade.get("repair_attempts", 0)
        if attempts >= 3:
            self.store.move_to_dlq(trade)
            logger.critical(f"❌ DLQ MOVED: {trade.get('order_id')} after 3 failed repairs.")
            return
        
        trade["repair_attempts"] = attempts + 1
        logger.info(f"🛠 REPAIR ATTEMPT {attempts + 1}: {drift} for {trade.get('order_id')}")

# =========================
# RISK ENGINE (SCORING)
# =========================
class RiskAIEngine:
    """የገበያ መዋዠቅን መሰረት አድርጎ የሪስክ ደረጃን የሚመድብ።"""
    
    def evaluate(self, market, exposure):
        volatility = market.get("volatility", 0)
        score = (volatility * 2) + exposure
        
        if score > 1.5: return "HIGH_RISK"
        if score > 0.8: return "MEDIUM_RISK"
        return "LOW_RISK"

# =========================
# POSITION SIZING
# =========================
class SmartRiskManager:
    """በሪስክ ደረጃ መሰረት የካፒታል ምደባ የሚያደርግ (መርህ #7)።"""
    
    def calculate(self, balance, risk_level):
        mapping = {
            "HIGH_RISK": 0.005,   # 0.5%
            "MEDIUM_RISK": 0.01,  # 1%
            "LOW_RISK": 0.02      # 2%
        }
        return balance * mapping.get(risk_level, 0.01)
