
import os
import json
import logging
from dataclasses import dataclass
from typing import Optional

# Logger setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# =========================
# ENV LOADER CORE
# =========================
class EnvManager:
    def __init__(self, env_file: Optional[str] = ".env"):
        self.env_file = env_file
        self._load_env_file()

    def _load_env_file(self):
        if self.env_file and os.path.exists(self.env_file):
            with open(self.env_file, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"): continue
                    if "=" in line:
                        key, value = line.split("=", 1)
                        os.environ.setdefault(key.strip(), value.strip())

    def get(self, key: str, default=None): return os.getenv(key, default)

    def require(self, key: str):
        value = os.getenv(key)
        if value is None:
            raise EnvironmentError(f"❌ Missing required env variable: {key}")
        return value

    def get_bool(self, key: str, default=False):
        return os.getenv(key, str(default)).lower() in ["1", "true", "yes", "y"]

    def get_int(self, key: str, default=0):
        try: return int(os.getenv(key, default))
        except ValueError: return default

    def get_float(self, key: str, default=0.0):
        try: return float(os.getenv(key, default))
        except ValueError: return default

# =========================
# CONFIG MODEL (FSE CORE SETTINGS)
# =========================
@dataclass
class FSEConfig:
    binance_api_key: str
    binance_api_secret: str
    max_leverage: int = 5
    max_risk_per_trade: float = 0.02
    symbol: str = "BTCUSDT" # Default placeholder
    scan_interval: int = 3
    environment: str = "production"
    debug_mode: bool = False
    telegram_token: str = ""
    telegram_chat_id: str = ""

# =========================
# CONFIG BUILDER
# =========================
class ConfigLoader:
    def __init__(self, env: EnvManager):
        self.env = env

    def load(self) -> FSEConfig:
        return FSEConfig(
            binance_api_key=self.env.require("BINANCE_API_KEY"),
            binance_api_secret=self.env.require("BINANCE_API_SECRET"),
            max_leverage=self.env.get_int("MAX_LEVERAGE", 5),
            max_risk_per_trade=self.env.get_float("MAX_RISK_PER_TRADE", 0.02),
            symbol=self.env.get("TRADE_SYMBOL", "BTCUSDT"),
            scan_interval=self.env.get_int("SCAN_INTERVAL", 3),
            environment=self.env.get("ENV", "production"),
            debug_mode=self.env.get_bool("DEBUG", False),
            telegram_token=self.env.get("TELEGRAM_TOKEN", ""),
            telegram_chat_id=self.env.get("TELEGRAM_CHAT_ID", "")
        )

# =========================
# GLOBAL INITIALIZATION
# =========================
env_manager = EnvManager()
config = ConfigLoader(env_manager).load()

def validate_runtime_env():
    """Ensure required credentials exist."""
    env_manager.require("BINANCE_API_KEY")
    env_manager.require("BINANCE_API_SECRET")
    logger.info("✅ Runtime environment validated.")

def print_config():
    """Safe print (hides secrets)."""
    cfg_dict = config.__dict__.copy()
    cfg_dict['binance_api_key'] = '***'
    cfg_dict['binance_api_secret'] = '***'
    logger.info(f"===== FSE CONFIG =====\n{json.dumps(cfg_dict, indent=4)}")
