
# fse/utils/time_utils.py
import time
from datetime import datetime, timezone

# =========================
# TIME HELPERS (CORE)
# =========================

def now_unix() -> int:
    """የአሁኑን ሰዓት በUnix ሴኮንድ መመለሻ።"""
    return int(time.time())

def now_ms() -> int:
    """የአሁኑን ሰዓት በMilliseconds መመለሻ (ለAPI ጥሪዎች አስፈላጊ)።"""
    return int(time.time() * 1000)

def utc_now() -> datetime:
    """UTC ሰዓት መመለሻ።"""
    return datetime.now(timezone.utc)

# =========================
# SCHEDULING & COOLDOWN
# =========================

def next_interval(interval_sec: int, offset: int = 0) -> float:
    """መርህ #6: የተስተካከለ የጊዜ ክፍተት (Aligned Interval) ማስያ።"""
    return ((time.time() // interval_sec) + 1) * interval_sec + offset

class Cooldown:
    """መርህ #9/10: በተደጋጋሚ ጥሪዎችን ለመከላከል (Rate Limiting)።"""
    def __init__(self):
        self._last_call = {}

    def allow(self, key: str, cooldown_sec: int) -> bool:
        now = time.time()
        if now - self._last_call.get(key, 0) >= cooldown_sec:
            self._last_call[key] = now
            return True
        return False

def in_time_window(start_hour: int, end_hour: int) -> bool:
    """መርህ #6: የንግድ ስራ የሚካሄድበትን ሰዓት ማረጋገጫ።"""
    return start_hour <= utc_now().hour <= end_hour
