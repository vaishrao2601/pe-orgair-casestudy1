# src/pe_orgair/db/snowflake.py
# (Yes the filename says snowflake — we’re keeping it so your existing import works.)

import os
from typing import Any, Dict, List, Optional
import psycopg
import psycopg.rows


class _DB:
    def _conn(self):
        url = os.getenv("DATABASE_URL")
        if not url:
            raise RuntimeError("DATABASE_URL not set in environment/.env")
        return psycopg.connect(url, row_factory=psycopg.rows.dict_row)

    def fetch_one(self, query: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        with self._conn() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params or {})
                return cur.fetchone()

    def fetch_all(self, query: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        with self._conn() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params or {})
                return cur.fetchall()


db = _DB()