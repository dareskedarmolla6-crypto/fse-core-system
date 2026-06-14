# fse/risk/risk_manager.py

class RiskManager:
    """
    Core capital protection layer
    """
    def __init__(self, max_daily_loss=0.05, max_exposure=0.3):
        self.max_daily_loss = max_daily_loss
        self.max_exposure = max_exposure

    def check_trade(self, balance, position_size, open_positions):
        exposure = sum(open_positions) / balance if balance > 0 else 0

        if position_size / balance > 0.02:
            return "REJECT: RISK TOO HIGH"

        if exposure > self.max_exposure:
            return "REJECT: EXPOSURE LIMIT"

        return "APPROVED"

    def emergency_stop(self, drawdown):
        return drawdown >= self.max_daily_loss


class RiskAdjuster:
    """
    Dynamic risk scaling based on performance
    """
    def adjust(self, win_rate):
        if win_rate < 0.4:
            return {"risk": 0.01}
        elif win_rate < 0.6:
            return {"risk": 0.02}
        return {"risk": 0.05}


class RiskEngine:
    """
    Lightweight trade approval engine
    """
    def __init__(self, max_loss=0.05, max_leverage=5):
        self.max_loss = max_loss
        self.max_leverage = max_leverage
        self.daily_loss = 0

    def approve_trade(self, signal, confidence, leverage):
        if confidence < 60:
            return False, "LOW CONFIDENCE"

        if leverage > self.max_leverage:
            return False, "LEVERAGE TOO HIGH"

        if self.daily_loss >= self.max_loss:
            return False, "DAILY LOSS LIMIT HIT"

        if signal not in ["LONG", "SHORT", "HEDGE"]:
            return False, "INVALID SIGNAL"

        return True, "APPROVED"

    def update_loss(self, loss):
        self.daily_loss += loss


class EmergencyStopEngine:
    """
    Hard system protection layer
    """
    def check(self, drawdown):
        if drawdown >= 0.15:
            return "STOP_ALL_TRADING"
        if drawdown >= 0.10:
            return "REDUCE_RISK"
        return "OK"


class ProfitLock:
    """
    Locks profit and reduces risk dynamically
    """
    def lock(self, position, profit):
        if profit > 0.05:
            position["stop_loss"] = profit * 0.5
        return position


class RewardEngine:
    """
    RL-style reward shaping
    """
    def calculate(self, pnl, risk, drawdown):
        return pnl - (risk * 0.5) - (drawdown * 2)


class LiquidityChecker:
    def is_valid(self, market_data):
        return market_data.get("volume", 0) >= 100000


class SignalValidator:
    def validate(self, signal, market_data, higher_tf_trend):
        if market_data.get("volume", 0) < 100000:
            return False

        if signal.get("flip_count", 0) > 3:
            return False

        if higher_tf_trend and higher_tf_trend != signal["side"]:
            return False

        return True


class SignalQualityScorer:
    def score(self, signal, market_data):
        score = 0
        score += min(market_data.get("volume", 0) / 10000, 50)
        score += market_data.get("volatility", 0) * 100
        score -= market_data.get("spread", 0) * 20
        return round(score, 2)


class AdvancedSignalValidationEngine:
    def __init__(self):
        self.validator = SignalValidator()
        self.scorer = SignalQualityScorer()

    def process(self, signal, market_data, higher_tf_trend):
        return {
            "valid": self.validator.validate(signal, market_data, higher_tf_trend),
            "quality_score": self.scorer.score(signal, market_data)
        }
