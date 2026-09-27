"""Async semaphore-based rate limiter."""
from __future__ import annotations

import asyncio


class RateLimiter:
    def __init__(self, concurrency: int) -> None:
        if concurrency < 1:
            raise ValueError("concurrency must be >= 1")
        self._sem = asyncio.Semaphore(concurrency)

    async def __aenter__(self) -> "RateLimiter":
        await self._sem.acquire()
        return self

    async def __aexit__(self, *exc: object) -> None:
        self._sem.release()