
# fse/dashboard/metrics_view.py
import time
import logging

logger = logging.getLogger(__name__)

# =========================
# TRADE HISTORY TRACKER
# =========================
class TradeHistory:
    """የንግድ ታሪክን የሚመዘግብ እና ስታቲስቲክስ የሚያወጣ ክፍል (መርህ #1)።"""
    
    def __init__(self):
        self.trades = []

    def log_trade(self, trade):
        """ንግድን መመዝገብ።"""
        trade["timestamp"] = time.time()
        self.trades.append(trade)
        logger.info(f"📝 Trade logged: {trade.get('symbol', 'Unknown')}")

    def get_trades(self):
        return self.trades

    def get_stats(self):
        """የድል መጠንን (Win Rate) ማስላት።"""
        total = len(self.trades)
        profit_trades = len([t for t in self.trades if t.get("profit", 0) > 0])
        win_rate = (profit_trades / total) * 100 if total > 0 else 0
        return {
            "total_trades": total,
            "win_rate": round(win_rate, 2)
        }

    def reset_history(self):
        """የንግድ ታሪክን ማጽዳት።"""
        self.trades = []
        logger.warning("🧹 Trade history reset.")

# =========================
# DASHBOARD VIEW
# =========================
class Dashboard:
    """ለተጠቃሚው የቦት ሁኔታን የሚያሳይ (Dashboard)።"""
    
    def show(self, tg, status, profit, trades, win_rate=None):
        """የቦቱን አጠቃላይ መረጃ በቴሌግራም መላክ።"""
        if tg is None:
            logger.warning("⚠️ Telegram client not found. Skipping notification.")
            return

        msg = (
            f"📊 **FSE DASHBOARD**\n\n"
            f"💰 Balance: {status.get('balance', 0)}\n"
            f"📦 Open Positions: {status.get('open_positions', 0)}\n"
            f"📈 Profit: {profit.get('profit', 0)}\n"
            f"📊 Total Trades: {len(trades)}\n"
        )

        if win_rate is not None:
            msg += f"🎯 Win Rate: {win_rate}%\n"

        msg += f"⚙️ Status: {status.get('status', 'UNKNOWN')}"

        try:
            tg.send(msg)
        except Exception as e:
            logger.error(f"❌ Failed to send dashboard update: {e}")
