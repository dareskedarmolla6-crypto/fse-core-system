# fse/execution/mean_reversion.py

import time
import uuid
import hashlib


# =========================
# ID EMPOTENCY KEY
# =========================
def generate_idempotency_key(symbol, side, qty, strategy_id, bucket):
    raw = f"{symbol}:{side}:{qty}:{strategy_id}:{bucket}"
    return hashlib.sha256(raw.encode()).hexdigest()


# =========================
# EXECUTION COORDINATOR
# =========================
class ExecutionCoordinator:
    def __init__(self, risk_engine, gateway, store, verifier, lock_mgr):
        self.risk = risk_engine
        self.gateway = gateway
        self.store = store
        self.verifier = verifier
        self.lock = lock_mgr

    def execute_signal(self, signal):
        if self.store.get("system_status") in ["STOP", "EMERGENCY"]:
            raise Exception("SYSTEM HALTED")

        with self.lock.acquire(signal["portfolio_id"]):
            if not self.risk.validate_new_position(signal):
                return None

            trade_id = f"BOT_{uuid.uuid4().hex[:16]}"
            trade = self._create_trade(trade_id, signal)
            self.store.save(trade)

            key = generate_idempotency_key(
                signal["symbol"],
                signal["side"],
                signal["qty"],
                signal["strategy_id"],
                int(time.time() // 60)
            )

            resp = self.gateway.place_order(signal, idempotency_key=key)

            return self.verifier.verify_order(
                trade_id,
                signal["symbol"],
                resp["orderId"]
            )

    def _create_trade(self, trade_id, signal):
        return {
            "trade_id": trade_id,
            "symbol": signal["symbol"],
            "side": signal["side"],
            "status": "CREATED",
            "ts": int(time.time()),
            "retries": 0
        }


# =========================
# EXECUTION ENGINE (PAPER / LOG)
# =========================
class ExecutionEngine:
    def __init__(self, client):
        self.client = client

    def open_long(self, symbol, qty):
        print(f"📈 LONG OPENED: {symbol} | Qty: {qty}")

    def open_short(self, symbol, qty):
        print(f"📉 SHORT OPENED: {symbol} | Qty: {qty}")


# =========================
# HEDGE ENGINE
# =========================
class HedgeEngine:
    def open_hedge(self, executor, symbol, qty):
        print("⚖️ HEDGE MODE ACTIVE")

        long_trade = executor.open_long(symbol, qty)
        short_trade = executor.open_short(symbol, qty)

        return {
            "symbol": symbol,
            "long": long_trade,
            "short": short_trade,
            "status": "HEDGE_ACTIVE"
        }


# =========================
# STRATEGY (SIGNAL DECISION)
# =========================
class Strategy:
    def build(self, signal, confidence):
        if confidence < 60:
            return "FULL_HEDGE"
        return f"{signal}_ONLY"


# =========================
# MEAN REVERSION STRATEGY
# =========================
class MeanReversion:
    def __init__(self):
        self.name = "MEAN_REVERSION_STRATEGY"

    def execute(self, market_data):
        print(f"🔄 Running {self.name}...")

        # TODO: add real mean reversion logic
        return {
            "action": "ANALYZE_REVERSION",
            "status": "ACTIVE",
            "data": market_data
        }


# =========================
# ORDER ROUTER
# =========================
class OrderManager:
    def __init__(self, execution_engine, hedge_engine):
        self.execution = execution_engine
        self.hedge = hedge_engine

    def execute(self, signal):
        symbol = signal["symbol"]
        side = signal["side"]
        qty = signal["qty"]

        if side == "LONG":
            return self.execution.open_long(symbol, qty)

        if side == "SHORT":
            return self.execution.open_short(symbol, qty)

        if side == "HEDGE":
            return self.hedge.open_hedge(self.execution, symbol, qty)

        return {"status": "NO_ACTION"}
