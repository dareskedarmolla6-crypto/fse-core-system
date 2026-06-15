
# fse/data/cache.py
import time
import threading
import logging

logger = logging.getLogger(__name__)

class CacheItem:
    def __init__(self, value, ttl):
        self.value = value
        self.expiry = time.time() + ttl

class CacheManager:
    """
    ለገበያ መረጃዎች እና ስልቶች ፈጣን ማህደር (High-speed Memory Cache)።
    """

    def __init__(self, default_ttl=5):
        self.store = {}
        self.default_ttl = default_ttl
        self.lock = threading.Lock()

    def set(self, key, value, ttl=None):
        """መረጃን በካሼ ውስጥ ማስቀመጥ።"""
        ttl = ttl or self.default_ttl
        with self.lock:
            self.store[key] = CacheItem(value, ttl)

    def get(self, key, default=None):
        """መረጃን ከካሼ ማምጣት እና ጊዜው ያለፈበት ከሆነ ማስወገድ።"""
        with self.lock:
            item = self.store.get(key)
            if not item:
                return default

            if time.time() > item.expiry:
                del self.store[key]
                return default
            return item.value

    def safe_get(self, key, default=None):
        """የስህተት መከላከያ (Safety Guard) ለካሼ ንባብ።"""
        try:
            return self.get(key, default)
        except Exception as e:
            logger.error(f"❌ Cache read error for {key}: {e}")
            return default

    def exists(self, key):
        """ቁልፉ በካሼ መኖሩን ማረጋገጥ።"""
        return self.get(key, None) is not None

    def delete(self, key):
        """አንድን መረጃ ከካሼ መሰረዝ።"""
        with self.lock:
            if key in self.store:
                del self.store[key]

    def clear(self):
        """መላውን ካሼ ማጽዳት።"""
        with self.lock:
            self.store.clear()
            logger.info("🧹 Cache cleared.")

    def cleanup(self):
        """ጊዜያቸው ያለፈባቸውን መረጃዎች በየጊዜው ማጽዳት።"""
        with self.lock:
            now = time.time()
            keys_to_delete = [k for k, v in self.store.items() if now > v.expiry]
            for k in keys_to_delete:
                del self.store[k]
