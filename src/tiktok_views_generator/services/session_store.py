"""SessionStore — mint/reuse pseudo-sessions with headers and TTL."""
from __future__ import annotations

import json
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from fake_useragent import UserAgent


@dataclass
class Session:
    id: str
    headers: dict[str, str]
    created: float = field(default_factory=time.time)
    uses: int = 0


class SessionStore:
    def __init__(self, cfg: dict[str, Any]) -> None:
        self.cfg = cfg
        self.dir = Path(cfg["dir"])
        self.dir.mkdir(parents=True, exist_ok=True)
        self.ttl = cfg["ttl_seconds"]
        self.per_session = cfg.get("requests_per_session", 25)
        try:
            self._ua = UserAgent()
        except Exception:  # noqa: BLE001 — offline fallback
            self._ua = None
        self._pool: list[Session] = []

    def _fresh(self) -> Session:
        sid = uuid.uuid4().hex[:16]
        ua = self._ua.random if self._ua else "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        headers = {
            "User-Agent": ua,
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://www.tiktok.com/",
            "X-TTVG-Session": sid,
        }
        return Session(id=sid, headers=headers)

    async def acquire(self, video_id: str) -> Session:
        now = time.time()
        for s in self._pool:
            if s.uses < self.per_session and (now - s.created) < self.ttl:
                s.uses += 1
                return s
        s = self._fresh()
        s.uses = 1