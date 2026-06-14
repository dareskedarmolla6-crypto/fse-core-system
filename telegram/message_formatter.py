# fse/telegram/message_formatter.py


class SignalFormatter:
    """
    Formats trading signals into Telegram-ready messages.
    """

    def format(self, signal: dict) -> str:
        symbol = signal.get("symbol", "UNKNOWN")
        side = signal.get("side", "UNKNOWN")
        score = signal.get("score", signal.get("strength", 0))
        strategy = signal.get("strategy_id", "N/A")

        return (
            "🚀 SIGNAL DETECTED\n"
            f"Symbol   : {symbol}\n"
            f"Side     : {side}\n"
            f"Score    : {score}\n"
            f"Strategy : {strategy}"
        )
