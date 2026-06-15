
# fse/strategy/mean_reversion.py
import logging

logger = logging.getLogger(__name__)

# =========================
# REVERSAL CONFIRMATION
# =========================
class ReversalConfirmationEngine:
    """የገበያ ለውጥን (Reversal) በሶስት መለኪያዎች የሚያረጋግጥ ክፍል (መርህ #3)።"""

    def confirm_reversal(self, trend: bool, volume: bool, momentum: bool) -> bool:
        """Trend, Volume እና Momentum ሲገጣጠሙ ብቻ Reversal ማረጋገጥ።"""
        is_valid = all([trend, volume, momentum])
        if is_valid:
            logger.info("🔄 Mean Reversion: Reversal confirmed.")
        return is_valid

# =========================
# SMART HEDGE CONTROLLER
# =========================
class SmartHedgeController:
    """በReversal ጊዜ የሄጅንግ ፖዚሽኖችን (Hedge Positions) የሚያስተዳድር።"""

    def manage_position(self, long_position: dict, short_position: dict, reversal_confirmed: bool):
        """ትርፋማ ያልሆነውን ጎን በመዝጋት አደጋን መቀነስ።"""
        
        if not reversal_confirmed:
            return "KEEP_BOTH"

        long_profit = float(long_position.get("profit", 0.0))
        short_profit = float(short_position.get("profit", 0.0))

        # የሄጅንግ ስልት: ትርፋማውን ይዞ ትርፋማ ያልሆነውን መዝጋት
        if long_profit > short_profit:
            logger.info("📉 Closing weaker short position.")
            return "CLOSE_SHORT"
        else:
            logger.info("📈 Closing weaker long position.")
            return "CLOSE_LONG"
