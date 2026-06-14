import time


# =========================
# PORTFOLIO ALLOCATION ENGINE
# =========================
class AllocationEngine:
    def __init__(self, initial_balance=1000):
        self.initial_balance = initial_balance
        self.available_balance = initial_balance
        self.used_margin = 0
        self.allocations = []
        self.max_risk_per_trade = 0.1  # 10% default risk cap

    # -------------------------
    # CALCULATE POSITION SIZE
    # -------------------------
    def calculate_position_size(self, confidence, balance=None):
        balance = balance or self.available_balance

        # confidence-based scaling (0–100)
        risk_factor = confidence / 100

        position_size = balance * self.max_risk_per_trade * risk_factor

        return round(position_size, 4)

    # -------------------------
    # ALLOCATE CAPITAL
    # -------------------------
    def allocate(self, symbol, signal, confidence):
        size = self.calculate_position_size(confidence)

        allocation = {
            "time": time.time(),
            "symbol": symbol,
            "signal": signal,
            "confidence": confidence,
            "allocated_size": size
        }

        self.allocations.append(allocation)

        self.available_balance -= size
        self.used_margin += size

        return allocation

    # -------------------------
    # RELEASE CAPITAL (ON CLOSE)
    # -------------------------
    def release(self, size):
        self.available_balance += size
        self.used_margin -= size

        if self.used_margin < 0:
            self.used_margin = 0

    # -------------------------
    # PORTFOLIO STATUS
    # -------------------------
    def status(self):
        return {
            "available_balance": round(self.available_balance, 2),
            "used_margin": round(self.used_margin, 2),
            "total_allocations": len(self.allocations)
        }

    # -------------------------
    # RISK CHECK BEFORE TRADE
    # -------------------------
    def can_allocate(self, confidence):
        projected_size = self.calculate_position_size(confidence)

        return projected_size <= self.available_balance

    # -------------------------
    # RESET (BACKTEST MODE)
    # -------------------------
    def reset(self):
        self.available_balance = self.initial_balance
        self.used_margin = 0
        self.allocations.clear()
