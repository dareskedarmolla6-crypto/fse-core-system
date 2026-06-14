# fse/risk/position_sizer.py

class PositionSizer:
    """
    Capital allocation engine for risk-controlled position sizing
    """

    def calculate_size(self, balance, risk_percentage, leverage=1, confidence=1.0):
        """
        balance: account balance
        risk_percentage: % of capital to risk (0.01 = 1%)
        leverage: trading leverage
        confidence: AI confidence multiplier (0-1)
        """

        base_risk = balance * risk_percentage
        adjusted_risk = base_risk * confidence
        position_size = adjusted_risk * leverage

        return round(position_size, 2)
