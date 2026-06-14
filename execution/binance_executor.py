# fse/execution/binance_executor.py

import time
import uuid
import hashlib


# =========================
# IDEMPOTENCY KEY
# =========================
def generate_idempotency_key(symbol, side, qty, strategy_id, bucket):
    raw = f"{symbol}:{side}:{qty}:{strategy_id}:{bucket}"
    return hashlib.sha256(raw.encode()).hexdigest()


# =========================
# BINANCE EXECUTOR CORE
# =========================
class BinanceExecutor:
    def __init__(self, client):
        self.client = client

    # -------------------------
    # LONG POSITION
    # -------------------------
    def open_long(self, symbol, quantity, leverage=20):
        try:
            self.client.futures_change_leverage(
                symbol=symbol,
                leverage=min(leverage, 20)
            )

            order = self.client.futures_create_order(
                symbol=symbol,
                side="BUY",
                type="MARKET",
                quantity=quantity
            )

            print(f"📈 LONG OPENED: {symbol} | Qty: {quantity}")
            return order

        except Exception as e:
            print(f"❌ LONG ERROR: {e}")
            return {"status": "ERROR", "message": str(e)}

    # -------------------------
    # SHORT POSITION
    # -------------------------
    def open_short(self, symbol, quantity, leverage=20):
        try:
            self.client.futures_change_leverage(
                symbol=symbol,
                leverage=min(leverage, 20)
            )

            order = self.client.futures_create_order(
                symbol=symbol,
                side="SELL",
                type="MARKET",
                quantity=quantity
            )

            print(f"📉 SHORT OPENED: {symbol} | Qty: {quantity}")
            return order

        except Exception as e:
            print(f"❌ SHORT ERROR: {e}")
            return {"status": "ERROR", "message": str(e)}

    # -------------------------
    # CLOSE POSITION
    # -------------------------
    def close_position(self, symbol):
        try:
            positions = self.client.futures_position_information(symbol=symbol)

            if not positions:
                return {"status": "NO_POSITION"}

            pos = positions[0]
            qty = abs(float(pos["positionAmt"]))

            if qty == 0:
                return {"status": "ALREADY_FLAT"}

            side = "SELL" if float(pos["positionAmt"]) > 0 else "BUY"

            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type="MARKET",
                quantity=qty
            )

            print(f"🔴 POSITION CLOSED: {symbol}")
            return order

        except Exception as e:
            print(f"❌ CLOSE ERROR: {e}")
            return {"status": "ERROR", "message": str(e)}


# =========================
# EXECUTION ROUTER (MAIN BRAIN)
# =========================
class BinanceExecutionRouter:
    def __init__(self, executor):
        self.executor = executor

    def execute(self, signal):
        symbol = signal["symbol"]
        side = signal["side"]
        qty = signal["qty"]

        if side == "LONG":
            return self.executor.open_long(symbol, qty)

        if side == "SHORT":
            return self.executor.open_short(symbol, qty)

        if side == "CLOSE":
            return self.executor.close_position(symbol)

        if side == "HEDGE":
            long_leg = self.executor.open_long(symbol, qty / 2)
            short_leg = self.executor.open_short(symbol, qty / 2)

            return {
                "symbol": symbol,
                "long": long_leg,
                "short": short_leg,
                "status": "HEDGE_ACTIVE"
            }

        return {"status": "NO_ACTION", "reason": "Unknown signal"}
