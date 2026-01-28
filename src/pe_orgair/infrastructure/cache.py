# src/pe_orgair/infrastructure/cache.py

from __future__ import annotations
from typing import Any, Dict, Optional
import time


class SimpleCache:
    def __init__(self):
        self._store: Dict[str, Any] = {}
        self._expires: Dict[str, float] = {}

    def get(self, key: str) -> Optional[Any]:
        exp = self._expires.get(key)
        if exp is not None and time.time() > exp:
            self._store.pop(key, None)
            self._expires.pop(key, None)
            return None
        return self._store.get(key)

    def set(self, key: str, value: Any, ttl: int = 0) -> None:
        self._store[key] = value
        if ttl and ttl > 0:
            self._expires[key] = time.time() + ttl
        else:
            self._expires.pop(key, None)

    def delete(self, key: str) -> None:
        self._store.pop(key, None)
        self._expires.pop(key, None)

    def invalidate_pattern(self, pattern: str) -> None:
        # pattern like "sectors:*"
        prefix = pattern.replace("*", "")
        keys = [k for k in self._store.keys() if k.startswith(prefix)]
        for k in keys:
            self.delete(k)


cache = SimpleCache()