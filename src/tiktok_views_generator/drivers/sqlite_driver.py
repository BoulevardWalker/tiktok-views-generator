"""sqlite driver — durable result log."""
from __future__ import annotations

import sqlite3
from pathlib import Path

from tiktok_views_generator.drivers.base import BaseDriver
from tiktok_views_generator.models.result import ViewResult

_SCHEMA = """
CREATE TABLE IF NOT EXISTS results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT NOT NULL,
    video_id TEXT,
    session_id TEXT,
    status TEXT NOT NULL,
    error TEXT,
    ts REAL NOT NULL
);
"""


class SqliteDriver(BaseDriver):
    name = "sqlite"

    def __init__(self, path: str = "out/results.sqlite") -> None:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(str(p))
        self._conn.executescript(_SCHEMA)
        self._conn.commit()

    async def emit(self, result: ViewResult) -> None:
        self._conn.execute(
            "INSERT INTO results (url, video_id, session_id, status, error, ts) VALUES (?,?,?,?,?,?)",
            (result.url, result.video_id, result.session_id, result.status, result.error, result.ts),
        )
        self._conn.commit()

    async def close(self) -> None:
        self._conn.close()