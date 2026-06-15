
import time
import psutil
import os
import logging

# Logger setup
logger = logging.getLogger(__name__)

# =========================
# PRODUCTION MONITOR
# =========================
class ProductionMonitor:
    MAX_RESTART_ATTEMPTS = 5

    def __init__(self, restart_callback=None):
        self.restart_callback = restart_callback
        self.last_heartbeat = time.time()
        self.restart_count = 0

    def track_system_health(self):
        health = {
            "cpu": psutil.cpu_percent(interval=1),
            "memory": psutil.virtual_memory().percent,
            "disk": psutil.disk_usage("/").percent,
            "uptime": time.time() - self.last_heartbeat
        }
        logger.info(f"[HEALTH] CPU:{health['cpu']}% | MEM:{health['memory']}% | DISK:{health['disk']}%")
        return health

    def monitor_bot_loop(self, last_trade_ts, timeout=60):
        """ቦቱ መቆሙን ወይም አለመቆሙን ለመቆጣጠር (60 ሰከንድ ቆይታ)።"""
        if (time.time() - last_trade_ts) > timeout:
            logger.warning("⚠️ BOT STALL DETECTED!")
            if self.restart_callback:
                self.trigger_auto_recovery()
            return False
        return True

    def trigger_auto_recovery(self):
        if self.restart_count < self.MAX_RESTART_ATTEMPTS:
            self.restart_count += 1
            logger.info(f"🔁 Auto recovery triggered (Attempt {self.restart_count})")
            try:
                # በስርዓቱ ላይ የተመሰረተ ትክክለኛ የሪስታርት ሂደት
                if self.restart_callback:
                    self.restart_callback()
            except Exception as e:
                logger.error(f"🚨 Recovery failed: {e}")
        else:
            logger.critical("🛑 MAX RESTART ATTEMPTS REACHED. MANUAL INTERVENTION REQUIRED.")

    def update_heartbeat(self):
        self.last_heartbeat = time.time()

# =========================
# CLOUD SYSTEM CORE STATE
# =========================
class F44Core:
    def __init__(self):
        self.running = False
        self.balance = 1000.0
        self.positions = {}
        self.last_risk = "LOW_RISK"
        self.last_trade_ts = time.time()

    def update_trade_time(self):
        self.last_trade_ts = time.time()

    def risk_state(self):
        return self.last_risk

    def set_risk(self, level):
        self.last_risk = level
        logger.info(f"🛡️ Risk Level Updated: {level}")
