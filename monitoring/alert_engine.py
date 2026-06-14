import time


# =========================
# MEMORY ANALYTICS
# =========================
class MemoryAnalytics:
    def __init__(self, memory):
        self.memory = memory

    def summary(self):
        total = len(self.memory.history)

        wins = len([
            t for t in self.memory.history
            if t.get("pnl", 0) > 0
        ])

        losses = total - wins

        win_rate = (wins / total) if total > 0 else 0

        return {
            "total_trades": total,
            "wins": wins,
            "losses": losses,
            "win_rate": round(win_rate, 3)
        }


# =========================
# ALERT ENGINE
# =========================
class AlertEngine:
    def __init__(self, memory, telegram=None):
        self.analytics = MemoryAnalytics(memory)
        self.telegram = telegram

    def check_health(self):
        stats = self.analytics.summary()

        alerts = []

        # ❗ low performance alert
        if stats["win_rate"] < 0.4 and stats["total_trades"] > 10:
            alerts.append("LOW_WIN_RATE")

        # ❗ no trades alert
        if stats["total_trades"] == 0:
            alerts.append("NO_TRADES_EXECUTED")

        # ❗ unstable system
        if stats["losses"] > stats["wins"] * 2:
            alerts.append("HIGH_RISK_DRAWDOWN")

        return stats, alerts

    def notify(self):
        stats, alerts = self.check_health()

        if not alerts:
            return {"status": "OK", "stats": stats}

        message = f"🚨 FSE ALERT\nStats: {stats}\nIssues: {alerts}"

        print(message)

        if self.telegram:
            try:
                self.telegram.send_message(message)
            except:
                pass

        return {
            "status": "ALERT",
            "stats": stats,
            "alerts": alerts
        }
