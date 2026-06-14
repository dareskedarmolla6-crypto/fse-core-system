import json
import time


class InMemoryStore:
    """
    Simple storage layer for FSE bot:
    - system status
    - trades
    - positions
    """

    def __init__(self):
        self.data = {
            "system_status": "RUNNING",
            "trades": [],
            "positions": [],
            "logs": []
        }

    # =========================
    # SYSTEM STATUS
    # =========================
    def set_status(self, status: str):
        self.data["system_status"] = status

    def get(self, key):
        return self.data.get(key)

    # =========================
    # TRADE STORAGE
    # =========================
    def save_trade(self, trade: dict):
        trade["ts"] = int(time.time())
        self.data["trades"].append(trade)

    def get_trades(self):
        return self.data["trades"]

    # =========================
    # POSITION STORAGE
    # =========================
    def save_position(self, position: dict):
        position["ts"] = int(time.time())
        self.data["positions"].append(position)

    def get_positions(self):
        return self.data["positions"]

    # =========================
    # LOGS
    # =========================
    def log(self, message: str):
        self.data["logs"].append({
            "message": message,
            "ts": int(time.time())
        })

    def get_logs(self):
        return self.data["logs"]

    # =========================
    # ACTIVE TRADES (for reliability engine)
    # =========================
    def get_active_trades(self):
        return [
            t for t in self.data["trades"]
            if t.get("status") != "CLOSED"
        ]

    # =========================
    # OPTIONAL: SAVE TO FILE
    # =========================
    def save_to_file(self, path="fse_storage.json"):
        with open(path, "w") as f:
            json.dump(self.data, f, indent=4)

    def load_from_file(self, path="fse_storage.json"):
        try:
            with open(path, "r") as f:
                self.data = json.load(f)
        except FileNotFoundError:
            pass
# Safety improvement: prevent corrupted JSON overwrite (backup fallback)
def safe_save_to_file(self, path="fse_storage.json"):
    backup_path = path + ".backup"
    try:
        self.save_to_file(path)
    except Exception:
        self.save_to_file(backup_path)
