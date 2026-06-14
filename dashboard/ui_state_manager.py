# fse/dashboard/ui_state_manager.py

class SystemStatus:
    def get_status(self, balance, open_positions, running=True, system_error=None):

        risk_level = self._risk_level(balance, open_positions)

        return {
            "balance": balance,
            "open_positions": len(open_positions),
            "status": "RUNNING" if running and balance > 0 else "STOPPED",
            "risk_level": risk_level,
            "system_error": system_error
        }

    def _risk_level(self, balance, open_positions):
        exposure = len(open_positions)

        if balance <= 0:
            return "CRITICAL"

        if exposure == 0:
            return "LOW"

        if exposure <= 3:
            return "MEDIUM"

        return "HIGH"


# =========================
# PROFIT TRACKER (IMPROVED)
# =========================
class ProfitTracker:
    def __init__(self):
        self.peak = None

    def calculate_profit(self, start_balance, current_balance):

        profit = current_balance - start_balance
        profit_percent = (profit / start_balance) * 100 if start_balance else 0

        # track peak (for drawdown awareness)
        if self.peak is None or current_balance > self.peak:
            self.peak = current_balance

        drawdown = self.peak - current_balance

        return {
            "profit": profit,
            "profit_percent": profit_percent,
            "drawdown": drawdown,
            "peak_balance": self.peak
        }
