import uuid
import time


# =========================
# POSITION MODEL
# =========================
class HedgePosition:
    def __init__(self, symbol, side, qty, entry_price):
        self.id = str(uuid.uuid4())
        self.symbol = symbol
        self.side = side  # BUY / SELL
        self.qty = qty
        self.entry_price = entry_price
        self.created_at = time.time()

        self.status = "OPEN"
        self.realized_pnl = 0
        self.unrealized_pnl = 0


# =========================
# HEDGE BOOK (STATE)
# =========================
class HedgeBook:
    def __init__(self):
        self.long_positions = {}
        self.short_positions = {}

    def add(self, position: HedgePosition):
        if position.side == "BUY":
            self.long_positions[position.id] = position
        else:
            self.short_positions[position.id] = position

    def get_symbol_positions(self, symbol):
        longs = [p for p in self.long_positions.values() if p.symbol == symbol]
        shorts = [p for p in self.short_positions.values() if p.symbol == symbol]
        return longs, shorts


# =========================
# HEDGE CONTROLLER
# =========================
class HedgeController:
    def __init__(self, book: HedgeBook):
        self.book = book

    def open_long(self, symbol, qty, price):
        pos = HedgePosition(symbol, "BUY", qty, price)
        self.book.add(pos)
        return pos

    def open_short(self, symbol, qty, price):
        pos = HedgePosition(symbol, "SELL", qty, price)
        self.book.add(pos)
        return pos


# =========================
# EXPOSURE ENGINE
# =========================
class ExposureEngine:
    def calculate(self, book: HedgeBook):
        long_qty = sum(p.qty for p in book.long_positions.values())
        short_qty = sum(p.qty for p in book.short_positions.values())

        return {
            "long_exposure": long_qty,
            "short_exposure": short_qty,
            "net_exposure": long_qty - short_qty
        }


# =========================
# RISK GUARD FOR HEDGE
# =========================
class HedgeRiskEngine:
    def __init__(self, max_net_exposure=100):
        self.max_net_exposure = max_net_exposure

    def validate(self, book: HedgeBook):
        exposure = ExposureEngine().calculate(book)

        if abs(exposure["net_exposure"]) > self.max_net_exposure:
            return False, "EXPOSURE_LIMIT"

        return True, "OK"


# =========================
# EXIT ENGINE
# =========================
class HedgeExitEngine:
    def close_position(self, position: HedgePosition, exit_price):
        if position.status != "OPEN":
            return 0

        if position.side == "BUY":
            pnl = (exit_price - position.entry_price) * position.qty
        else:
            pnl = (position.entry_price - exit_price) * position.qty

        position.realized_pnl = pnl
        position.status = "CLOSED"
        return pnl


# =========================
# MAIN MANAGER
# =========================
class HedgeModeManager:
    def __init__(self):
        self.book = HedgeBook()
        self.controller = HedgeController(self.book)
        self.risk = HedgeRiskEngine()
        self.exit_engine = HedgeExitEngine()

    def status(self):
        return {
            "longs": len(self.book.long_positions),
            "shorts": len(self.book.short_positions)
        }

    def is_hedged(self, symbol):
        longs, shorts = self.book.get_symbol_positions(symbol)
        return len(longs) > 0 and len(shorts) > 0
