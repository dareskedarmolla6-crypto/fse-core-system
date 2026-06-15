
# fse/monitoring/system_health.py
import time
import psutil
import threading
import logging

logger = logging.getLogger(__name__)

# =========================
# SYSTEM HEALTH MONITOR
# =========================
class SystemHealthMonitor:
    """የቦቱን የስርዓት ሀብት አጠቃቀም (CPU, RAM, Latency) የሚከታተል (መርህ #6)።"""
    
    def __init__(self, cpu_limit=80, memory_limit=80):
        self.cpu_limit = cpu_limit
        self.memory_limit = memory_limit
        self.errors = 0
        self.trades = 0
        self.start_time = time.time()
        self.latency_log = []
        self.running = False

    def record_trade(self): self.trades += 1
    def record_error(self): self.errors += 1

    def record_latency(self, latency_ms):
        self.latency_log.append(latency_ms)
        if len(self.latency_log) > 100: self.latency_log.pop(0)

    def system_status(self):
        """የስርዓቱን ሁኔታ እና የጤንነት ደረጃ (Health Status) የሚመልስ።"""
        cpu = psutil.cpu_percent(interval=None)
        mem = psutil.virtual_memory().percent
        avg_latency = sum(self.latency_log) / len(self.latency_log) if self.latency_log else 0
        
        status = "HEALTHY"
        if cpu > self.cpu_limit: status = "CPU_HIGH"
        elif mem > self.memory_limit: status = "MEMORY_HIGH"
        elif self.errors > 10: status = "ERROR_OVERLOAD"
        elif avg_latency > 1000: status = "HIGH_LATENCY"

        return {
            "status": status, "cpu": cpu, "memory": mem,
            "errors": self.errors, "trades": self.trades,
            "avg_latency_ms": round(avg_latency, 2),
            "uptime_sec": round(time.time() - self.start_time, 2)
        }

    def start_background_monitor(self, interval=5):
        """በጀርባ (Background Thread) ሁኔታን የሚከታተል ተግባር።"""
        self.running = True
        def loop():
            while self.running:
                status = self.system_status()
                logger.info(f"📊 SYSTEM HEALTH: {status}")
                time.sleep(interval)

        thread = threading.Thread(target=loop, daemon=True)
        thread.start()

    def stop(self):
        self.running = False
