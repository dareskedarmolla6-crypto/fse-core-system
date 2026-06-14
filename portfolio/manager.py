# portfolio/portfolio_manager.py

class PortfolioManager:
    def __init__(self, total_capital: float):
        self.total_capital = total_capital
        self.reserve_ratio = 0.25
        self.positions = []
        self.balance = total_capital

    # =========================
    # CAPITAL ALLOCATION
    # =========================
    def allocate_capital(self, strategies):
        """
        Allocate capital dynamically based on strategy scores.
        Higher score = more allocation.
        """
        if not strategies:
            return {}

        total_score = sum(s["score"] for s in strategies)

        allocations = {}
        available_capital = self.balance * (1 - self.reserve_ratio)

        for s in strategies:
            weight = s["score"] / total_score
            allocations[s["symbol"]] = available_capital * weight

        return allocations

    # =========================
    # EXPOSURE CONTROL
    # =========================
    def check_symbol_exposure(self, symbol, current_exposure):
        """
        Limit exposure per symbol to 20%
        """
        max_exposure = self.total_capital * 0.20

        if current_exposure >= max_exposure:
            return False, "EXPOSURE_LIMIT_REACHED"

        return True, "OK"

    # =========================
    # HEALTH SCORE
    # =========================
    def calculate_health_score(self):
        """
        Simple portfolio health score:
        - fewer positions = better
        - higher balance = better
        """
        exposure_penalty = len(self.positions) * 2
        balance_factor = (self.balance / self.total_capital) * 100

        score = balance_factor - exposure_penalty
        return max(0, min(100, score))

    # =========================
    # UPDATE AFTER TRADE
    # =========================
    def update(self, trade_result):
        """
        Update portfolio after trade execution
        """
        pnl = trade_result.get("pnl", 0)

        self.balance += pnl
        self.positions.append(trade_result)

    # =========================
    # POSITION SUMMARY
    # =========================
    def state(self):
        return {
            "balance": self.balance,
            "open_positions": len(self.positions),
            "health_score": self.calculate_health_score()
        }
