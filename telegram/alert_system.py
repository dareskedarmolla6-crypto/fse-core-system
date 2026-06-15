# fse/telegram/alert_system.py
import requests
import logging

logger = logging.getLogger(__name__)

# =========================
# TELEGRAM NOTIFIER
# =========================
class TelegramNotifier:
    """የመልዕክት መላኪያ ክፍል (መርህ #8)።"""
    def __init__(self, token, chat_id):
        self.token = token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{self.token}/sendMessage"

    def send(self, message: str):
        """መልዕክትን ወደ ቴሌግራም መላክ (Error Handling ተካቷል)።"""
        payload = {"chat_id": self.chat_id, "text": message}
        try:
            response = requests.post(self.base_url, json=payload, timeout=10)
            response.raise_for_status()
        except Exception as e:
            logger.error(f"❌ Telegram Alert Error: {e}")

# =========================
# SIGNAL & TRADE FORMATTER
# =========================
class SignalFormatter:
    """ሲግናሎችን ለቴሌግራም በሚመች ሁኔታ ማዘጋጀት።"""
    def format(self, signal: dict):
        return (
            "🚀 SIGNAL DETECTED\n"
            f"Symbol: {signal.get('symbol', 'N/A')}\n"
            f"Side: {signal.get('side', 'N/A')}\n"
            f"Score: {signal.get('score', 0)}\n"
            f"Strategy: {signal.get('strategy_id', 'N/A')}"
        )

# =========================
# SIGNAL DISTRIBUTOR (MULTI CHANNEL)
# =========================
class SignalDistributor:
    """ሲግናሎችን በተለያዩ መስመሮች ማሰራጨት።"""
    def __init__(self, telegram, discord=None, email=None):
        self.telegram = telegram
        self.discord = discord
        self.email = email
        self.formatter = SignalFormatter()

    def broadcast(self, signal: dict):
        msg = self.formatter.format(signal)
        if self.telegram: self.telegram.send(msg)
        if self.discord: self.discord.send(msg)
        if self.email: self.email.send("Trading Signal", msg)

# =========================
# RISK & TRADE NOTIFICATIONS
# =========================
class TradeNotifier:
    def __init__(self, telegram):
        self.telegram = telegram

    def notify_trade(self, action, symbol, size):
        msg = f"📊 TRADE ALERT\nSymbol: {symbol}\nAction: {action}\nSize: {size}\nStatus: EXECUTED"
        self.telegram.send(msg)

class RiskNotifier:
    def __init__(self, telegram):
        self.telegram = telegram

    def alert(self, risk_level: str):
        if risk_level == "HIGH":
            self.telegram.send("🚨 WARNING: High Risk Exposure Detected!")
        elif risk_level == "CRITICAL":
            self.telegram.send("🛑 SYSTEM STOPPED: Emergency Exit Activated!")
