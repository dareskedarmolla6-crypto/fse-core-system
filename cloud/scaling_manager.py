import time


# =========================
# BACKUP SYSTEM
# =========================
class BackupManager:
    def __init__(self, storage):
        self.storage = storage  # e.g S3, Oracle Cloud, local disk

    def perform_daily_backup(self, state):
        print("💾 Daily backup started...")
        self.storage.save("daily_backup", state)

    def perform_weekly_full_backup(self, state):
        print("☁️ Full system backup started...")
        self.storage.save("weekly_full_backup", state)

    def restore_from_disaster(self):
        print("🚨 Restoring system state...")
        return self.storage.load("weekly_full_backup")


# =========================
# CLOUD MONITOR + RESILIENCE
# =========================
class CloudMonitor:
    def __init__(self, api_client):
        self.api_client = api_client
        self.reconnect_attempts = 0

    def safe_loop(self, fetch_data, symbol):
        while True:
            try:
                data = fetch_data(symbol)
                self.reconnect_attempts = 0
                return data

            except Exception as e:
                self.reconnect_attempts += 1
                print("⚠️ API ERROR:", e)
                print("🔁 RETRYING...")

                self.recovery_system()
                time.sleep(5)

    def heartbeat(self):
        try:
            self.api_client.get_price("BTCUSDT")
            return True
        except:
            return False

    def recovery_system(self):
        if self.reconnect_attempts > 3:
            print("🚨 ALERT: SYSTEM INSTABILITY DETECTED")

        print("🔁 RECONNECTING TO MARKET DATA...")
        time.sleep(2)
