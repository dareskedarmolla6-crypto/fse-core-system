import logging

class RiskEngine:
    """
    Core Risk Engine:
    - position risk control
    - exposure control
    - emergency stop logic
    """

    def __init__(self, max_risk=0.02, max_exposure=0.3, max_drawdown=0.25):
        self.max_risk = max_risk
        self.max_exposure = max_exposure
        self.max_drawdown = max_drawdown

    def validate_new_position(self, signal, balance, position_size, open_positions):
        # 1. risk per trade
        if position_size / balance > self.max_risk:
            return False, "RISK_TOO_HIGH"

        # 2. exposure check
        exposure = sum(open_positions) / balance if open_positions else 0
        if exposure > self.max_exposure:
            return False, "EXPOSURE_LIMIT"

        # 3. signal validation
        if signal not in ["LONG", "SHORT", "HEDGE"]:
            return False, "INVALID_SIGNAL"

        return True, "APPROVED"

    def emergency_stop(self, drawdown):
        return drawdown >= self.max_drawdown


class RiskGovernor:
    """
    System-wide protection layer (kill switch + state control)
    """

    def __init__(self, store):
        self.store = store
        self.state = {
            "daily_pnl": 0,
            "consecutive_losses": 0,
            "drawdown": 0
        }

    def update(self, pnl):
        self.state["daily_pnl"] += pnl

        if pnl < 0:
            self.state["consecutive_losses"] += 1
        else:
            self.state["consecutive_losses"] = 0

        self.store.set("risk_state", self.state)

    def approve_trade(self):
        if self.store.get("system_status") in ["STOP", "EMERGENCY"]:
            return False, "SYSTEM_HALTED"

        if self.state["consecutive_losses"] >= 5:
            self._halt("CONSECUTIVE LOSSES")
            return False, "SAFE_MODE"

        return True, "OK"

    def _halt(self, reason):
        logging.warning(f"[RISK HALT] {reason}")
        self.store.set("system_status", "STOP")


class PositionSizer:
    """
    Dynamic position sizing based on risk
    """

    def calculate(self, balance, confidence):
        risk_factor = confidence / 100
        return round(balance * self.max_risk * risk_factor, 2)


class RiskAdjuster:
    """
    Adaptive risk based on performance
    """

    def adjust(self, win_rate):
        if win_rate < 0.4:
            return {"risk": 0.01}
        elif win_rate < 0.6:
            return {"risk": 0.02}
        return {"risk": 0.05}
        def get_leverage(confidence, volatility=0.5, hedge=False):

    # no trade zone
    if confidence < 15:
        return 0

    # base mapping
    if 15 <= confidence <= 25:
        lev = 5
    elif 26 <= confidence <= 35:
        lev = 8
    elif 36 <= confidence <= 55:
        lev = 10
    elif 56 <= confidence <= 75:
        lev = 15
    elif 76 <= confidence <= 85:
        lev = 20
    else:
        lev = 30

    # volatility adjustment (IMPORTANT)
    if volatility > 0.8:
        lev *= 0.7   # reduce risk in chaos market
    elif volatility < 0.3:
        lev *= 1.2   # increase leverage in stable market

    # hedge mode safety
    if hedge:
        lev *= 0.6   # reduce leverage when hedging

    # safety cap
    return min(round(lev), 30)
