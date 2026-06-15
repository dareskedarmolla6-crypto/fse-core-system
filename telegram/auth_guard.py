
# fse/telegram/auth_guard.py
import logging
from fse.config.env_config import EnvConfig

logger = logging.getLogger(__name__)

class AuthGuard:
    """የቴሌግራም ተጠቃሚዎችን የማረጋገጥ እና የመዳረሻ መብት አስተዳዳሪ (መርህ #11)።"""
    
    def __init__(self):
        self.authorized_users = self._normalize_users()

    def _normalize_users(self):
        """የተፈቀደላቸውን ተጠቃሚዎች ዝርዝር ማዘጋጀት።"""
        auth = getattr(EnvConfig, 'AUTHORIZED_USER', [])
        if isinstance(auth, list):
            return set(str(user_id) for user_id in auth)
        return {str(auth)}

    def is_authorized(self, user_id: int | str) -> bool:
        """ተጠቃሚው መዳረሻ እንዳለው ያረጋግጣል።"""
        authorized = str(user_id) in self.authorized_users
        if not authorized:
            logger.warning(f"🚫 Unauthorized access attempt by: {user_id}")
        return authorized

    def require_auth(self, user_id: int | str):
        """መዳረሻ ለሌለው ተጠቃሚ ጥብቅ ክልከላ ማድረግ።"""
        if not self.is_authorized(user_id):
            logger.error(f"🔒 Access DENIED for: {user_id}")
            raise PermissionError("❌ Unauthorized user access blocked.")
