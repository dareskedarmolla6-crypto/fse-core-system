
# fse/monitoring/logger.py
import json
import time
import logging

logger = logging.getLogger(__name__)

# =========================
# TELEMETRY STREAM (EVENT BUFFER)
# =========================
class TelemetryStream:
    """የንግድ እና የስርዓት እንቅስቃሴዎችን በቅጽበት የሚሰበስብ (Telemetry)።"""
    
    def __init__(self, max_size=100):
        self.buffer = []
        self.max_size = max_size

    def push(self, event_type, data):
        event = {"time": time.time(), "type": event_type, "data": data}
        self.buffer.append(event)
        if len(self.buffer) > self.max_size:
            self.buffer = self.buffer[-self.max_size:]

    def flush(self):
        payload = json.dumps(self.buffer)
        self.buffer.clear()
        logger.info(f"📤 TELEMETRY FLUSHED: {payload}")
        return payload

# =========================
# TELEMETRY HOOK (EVENT CONNECTOR)
# =========================
class TelemetryHook:
    """ክስተቶችን ወደ ቴሌሜትሪ የሚገፋ (Bridge)።"""
    
    def __init__(self, stream: TelemetryStream):
        self.stream = stream

    def on_trade(self, pnl, balance):
        self.stream.push("TRADE", {"pnl": pnl, "balance": balance})

    def on_signal(self, signal):
        self.stream.push("SIGNAL", signal)

    def on_error(self, error):
        self.stream.push("ERROR", {"message": str(error)})

# =========================
# METRICS STORE (STATE TRACKER)
# =========================
class MetricsStore:
    """የንግድ ታሪክን እና የሂሳብ ቀሪ ሂሳብን (Portfolio State) የሚከታተል (መርህ #7)።"""
    
    def __init__(self):
        self.balance = 1000.0
        self.trades = []

    def log_trade(self, signal, pnl):
        self.trades.append({"signal": signal, "pnl": pnl, "timestamp": time.time()})
        self.balance += pnl
        logger.info(f"💰 TRADE LOGGED: PnL {pnl} | New Balance {self.balance}")

# =========================
# SYSTEM MONITOR (HEALTH CHECK)
# =========================
class MetricsCollection:
    """የስርዓቱን ሁኔታ አጠቃላይ መረጃ የሚሰበስብ።"""
    
    def collect(self, data):
        status = data.get("status", "UNKNOWN")
        logger.info(f"🟢 SYSTEM HEALTH STATUS: {status}")
