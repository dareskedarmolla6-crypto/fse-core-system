import requests


# =========================
# BASIC TELEGRAM SENDER
# =========================
class TelegramNotifier:
    def __init__(self, token, chat_id):
        self.token = token
        self.chat_id = chat_id

    def send(self, message: str):
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": message
        }

        try:
            requests.post(url, json=payload, timeout=10)
        except Exception as e:
            print("Telegram Error:", e)


# =========================
# SIGNAL FORMATTER
# =========================
class SignalFormatter:
    def format(self, signal: dict):
        return (
            "🚀 SIGNAL DETECTED\n"
            f"Symbol: {signal.get('symbol')}\n"
            f"Side: {signal.get('side')}\n"
            f"Score: {signal.get('score', 0)}\n"
            f"Strategy: {signal.get('strategy_id', 'N/A')}"
        )


# =========================
# SIGNAL DISTRIBUTOR (MULTI CHANNEL)
# =========================
class SignalDistributor:
    def __init__(self, telegram, discord=None, email=None):
        self.telegram = telegram
        self.discord = discord
        self.email = email
        self.formatter = SignalFormatter()

    def broadcast(self, signal: dict):
        msg = self.formatter.format(signal)

        if self.telegram:
            self.telegram.send(msg)

        if self.discord:
            self.discord.send(msg)

        if self.email:
            self.email.send("Trading Signal", msg)


# =========================
# TRADE NOTIFICATIONS
# =========================
class TradeNotifier:
    def __init__(self, telegram):
        self.telegram = telegram

    def notify_trade(self, action, symbol, size):
        msg = (
            "📊 TRADE ALERT\n"
            f"Symbol: {symbol}\n"
            f"Action: {action}\n"
            f"Size: {size}\n"
            "Status: EXECUTED"
        )
        self.telegram.send(msg)


# =========================
# RISK ALERTS
# =========================
class RiskNotifier:
    def __init__(self, telegram):
        self.telegram = telegram

    def alert(self, risk_level: str):
        if risk_level == "HIGH":
            self.telegram.send("🚨 WARNING: High Risk Exposure Detected!")

        elif risk_level == "CRITICAL":
            self.telegram.send("🛑 SYSTEM STOPPED: Emergency Exit Activated!")


# =========================
# OPTIONAL SIMPLE WRAPPER
# =========================
class TelegramIntegration:
    def __init__(self, telegram):
        self.telegram = telegram

    def send_signal(self, message):
        self.telegram.send(f"[SIGNAL] {message}")

    def send_trade_update(self, trade):
        self.telegram.send(f"[TRADE UPDATE] {trade}")
