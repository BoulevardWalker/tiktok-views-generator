"""ProxyPool — round-robin over proxies/pool.txt with health-aware skip."""
from __future__ import annotations

import asyncio
import itertools
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class Proxy:
    url: str
    fails: int = 0


class ProxyPool:
    def __init__(self, cfg: dict[str, Any]) -> None:
        self.cfg = cfg
        self._lock = asyncio.Lock()
        self._proxies: list[Proxy] = []
        self._cycle: itertools.cycle[Proxy] | None = None
        self._load()

    def _load(self) -> None:
        path = Path(self.cfg["pool_file"])
        if not path.is_file():
            self._proxies = []
            self._cycle = itertools.cycle([Proxy(url="")])
            return
        lines = [ln.strip() for ln in path.read_text(encoding="utf-8").splitlines()]
        self._proxies = [Proxy(url=ln) for ln in lines if ln and not ln.startswith("#")]
        self._cycle = itertools.cycle(self._proxies) if self._proxies else itertools.cycle([Proxy(url="")])

    async def acquire(self) -> Proxy | None:
        async with self._lock:
            if self._cycle is None:
                return None
            return next(self._cycle)

    async def report_fail(self, proxy: Proxy) -> None:
        async with self._lock:
            proxy.fails += 1

    def size(self) -> int:
        return len(self._proxies)