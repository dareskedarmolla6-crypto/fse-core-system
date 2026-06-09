class RiskManager:
    def __init__(self, balance, risk_percentage=0.02):
        self.balance = balance
        self.risk_percentage = risk_percentage

    def calculate_position_size(self, stop_loss_distance):
        """
        Calculates the amount to risk based on account balance and stop loss distance.
        """
        risk_amount = self.balance * self.risk_percentage
        position_size = risk_amount / stop_loss_distance
        return position_size

    def check_risk_limit(self, trade_value):
        """
        Ensures the trade does not exceed the allowed risk limit.
        """
        return trade_value <= (self.balance * 0.10) # Example: Max 10% per trade
