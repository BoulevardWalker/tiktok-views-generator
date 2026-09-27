"""Pipeline: handler -> processors -> worker pool -> driver."""
from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass, field
from typing import Any

from tiktok_views_generator.drivers.base import BaseDriver
from tiktok_views_generator.handlers.base import BaseIngestHandler
from tiktok_views_generator.models.job import ViewJob
from tiktok_views_generator.models.result import ViewResult
from tiktok_views_generator.services.proxy_pool import ProxyPool
from tiktok_views_generator.services.rate_limiter import RateLimiter
from tiktok_views_generator.services.session_store import SessionStore

log = logging.getLogger(__name__)


@dataclass
class PipelineStats:
    submitted: int = 0
    ok: int = 0
    failed: int = 0
    errors: list[str] = field(default_factory=list)


class Pipeline:
    def __init__(
        self,
        cfg: dict[str, Any],
        handler: BaseIngestHandler,
        driver: BaseDriver,
        processors: list[Any],
    ) -> None:
        self.cfg = cfg
        self.handler = handler
        self.driver = driver
        self.processors = processors
        self.proxy_pool = ProxyPool(cfg["proxy"])
        self.session_store = SessionStore(cfg["session"])
        self.rate_limiter = RateLimiter(cfg["runtime"]["concurrency"])

    async def _worker(self, queue: asyncio.Queue[ViewJob | None], stats: PipelineStats) -> None:
        while True:
            job = await queue.get()
            if job is None:
                queue.task_done()
                return
            try:
                async with self.rate_limiter:
                    for proc in self.processors:
                        job = await proc.run(job, ctx=self)
                result = ViewResult.from_job(job, status="ok")
                stats.ok += 1
            except Exception as exc:  # noqa: BLE001 — worker must not die
                log.warning("job failed: %s :: %s", job.url, exc)
                result = ViewResult.from_job(job, status="fail", error=str(exc))
                stats.failed += 1
                stats.errors.append(f"{job.url}: {exc}")
            await self.driver.emit(result)
            queue.task_done()

    async def run(self, source: str) -> PipelineStats:
        stats = PipelineStats()
        queue: asyncio.Queue[ViewJob | None] = asyncio.Queue(
            maxsize=self.cfg["runtime"]["concurrency"] * 2
        )
        workers = [
            asyncio.create_task(self._worker(queue, stats))
            for _ in range(self.cfg["runtime"]["concurrency"])
        ]

        async for job in self.handler.ingest(source):
            stats.submitted += 1
            await queue.put(job)

        for _ in workers:
            await queue.put(None)
        await queue.join()
        await asyncio.gather(*workers, return_exceptions=True)
        await self.driver.close()
        return stats