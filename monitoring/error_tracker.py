
# fse/monitoring/error_tracker.py
import logging
import time
import traceback

logger = logging.getLogger(__name__)

# =========================
# ERROR TRACKER / LOGGER
# =========================
class ErrorTracker:
    """ስህተቶችን በቅጽበት የሚይዝ እና ሪፖርት የሚያደርግ (መርህ #11)።"""
    
    def __init__(self, store=None, alert_system=None):
        self.store = store
        self.alert_system = alert_system
        self.error_buffer = []

    def capture(self, error, context=None):
        error_data = {
            "timestamp": time.time(),
            "error": str(error),
            "context": context or {},
            "trace": traceback.format_exc()
        }

        self.error_buffer.append(error_data)
        logger.error(f"🚨 [FSE ERROR] {error_data['error']} | Context: {context}")

        if self.store:
            self.store.save_error(error_data)

        if self.alert_system:
            try:
                self.alert_system.send_message(f"🚨 FSE ALERT: {error_data['error']}")
            except Exception as e:
                logger.error(f"❌ Alert system failure: {e}")

    def get_recent_errors(self, limit=20):
        return self.error_buffer[-limit:]

    def clear(self):
        self.error_buffer = []

# =========================
# SYSTEM HEALTH TRACKER
# =========================
class SystemHealthTracker:
    """የቦቱን የስራ ብቃት እና ጤንነት የሚከታተል ክፍል (መርህ #6)።"""
    
    def __init__(self):
        self.start_time = time.time()
        self.error_count = 0
        self.last_heartbeat = time.time()

    def heartbeat(self):
        self.last_heartbeat = time.time()

    def record_error(self):
        self.error_count += 1

    def status(self):
        uptime = time.time() - self.start_time
        if self.error_count > 10:
            state = "UNSTABLE"
        elif uptime < 60:
            state = "WARMING_UP"
        else:
            state = "STABLE"

        return {
            "state": state,
            "uptime_seconds": round(uptime, 2),
            "total_errors": self.error_count,
            "last_heartbeat": self.last_heartbeat
        }

# =========================
# SAFE EXECUTION WRAPPER
# =========================
class SafeExecutor:
    """ማንኛውንም ተግባር በደህና መንገድ የሚያስኬድ (Fail-safe mechanism)።"""
    
    def __init__(self, error_tracker):
        self.tracker = error_tracker

    def run(self, fn, *args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            self.tracker.capture(e, context={"function": fn.__name__})
            return None
