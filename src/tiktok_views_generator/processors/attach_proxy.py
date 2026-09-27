"""Attach a proxy from the pool. Rotation policy lives in the pool."""
from __future__ import annotations

from typing import Any

from tiktok_views_generator.models.job import ViewJob
from tiktok_views_generator.processors.base import BaseProcessor


class AttachProxy(BaseProcessor):
    name = "attach_proxy"

    async def run(self, job: ViewJob, ctx: Any) -> ViewJob:
        proxy = await ctx.proxy_pool.acquire()
        job.proxy = proxy.url if proxy else None
        return job