import logging


# =========================
# RELIABILITY ORCHESTRATOR
# =========================
class ReliabilityOrchestrator:
    def __init__(self, store, gateway):
        self.store = store
        self.gateway = gateway

    def rebuild_state(self):
        active_trades = self.store.get_active_trades()

        for trade in active_trades:
            symbol = trade["symbol"]

            order = self.gateway.query_order(symbol, trade.get("order_id"))
            position = self.gateway.query_position(symbol)

            drift = self._detect_drift(trade, order, position)

            if drift:
                self._repair(trade, drift)

    def _detect_drift(self, trade, order, position):
        # order exists but trade not updated
        if order and order.get("status") == "FILLED" and trade.get("status") != "FILLED":
            return "STATE_DRIFT"

        # order missing
        if not order:
            return "ORPHAN_ORDER"

        # position exists but no order tracked
        if position and float(position.get("positionAmt", 0)) != 0 and not order:
            return "ORPHAN_POSITION"

        return None

    def _repair(self, trade, drift):
        attempts = trade.get("repair_attempts", 0)

        if attempts >= 3:
            self.store.move_to_dlq(trade)
            logging.warning(f"DLQ MOVED: {trade.get('order_id')}")
            return

        trade["repair_attempts"] = attempts + 1

        logging.info(
            f"REPAIR ATTEMPT {attempts + 1}: {drift} -> {trade.get('order_id')}"
        )

        # placeholder for future auto-recovery logic
        # e.g. resync order, cancel orphan position, etc.


# =========================
# RISK ENGINE (SCORING)
# =========================
class RiskAIEngine:
    def evaluate(self, market, exposure):
        volatility = market.get("volatility", 0)

        score = volatility * 2 + exposure

        if score > 1.5:
            return "HIGH_RISK"
        elif score > 0.8:
            return "MEDIUM_RISK"
        else:
            return "LOW_RISK"


# =========================
# POSITION SIZING
# =========================
class SmartRiskManager:
    def calculate(self, balance, risk_level):
        if risk_level == "HIGH_RISK":
            return balance * 0.005  # 0.5%
        elif risk_level == "MEDIUM_RISK":
            return balance * 0.01   # 1%
        else:
            return balance * 0.02   # 2%
