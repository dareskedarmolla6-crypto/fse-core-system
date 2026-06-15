# fse/dashboard/api_server.py
import logging

logger = logging.getLogger(__name__)

class DashboardController:
    """
    Dashboard Controller: ለቦት አፈጻጸም እና ለሪፖርት ማቅረቢያ ማዕከል (መርህ #1)
    """

    def __init__(self, status_engine, history_engine, profit_engine, dashboard_ui):
        self.status = status_engine
        self.history = history_engine
        self.profit = profit_engine
        self.dashboard = dashboard_ui

    def update(self, telegram_status, start_balance, current_balance, open_positions):
        """የቦቱን አጠቃላይ ሁኔታ እና የትርፍ/ኪሳራ ሪፖርት ማዘመን።"""
        
        # Current system status
        system_status = self.status.get_status(
            current_balance,
            open_positions
        )

        # Calculate PnL (መርህ #7)
        profit_report = self.profit.calculate_profit(
            start_balance,
            current_balance
        )

        # Get trade history
        trade_history = self.history.get_trades()

        # Update dashboard display
        try:
            self.dashboard.show(
                telegram_status,
                system_status,
                profit_report,
                trade_history
            )
            logger.info("✅ Dashboard updated successfully.")
        except Exception as e:
            logger.error(f"❌ Dashboard update failed: {e}")

        return {
            "status": system_status,
            "profit": profit_report,
            "trades": trade_history
        }
