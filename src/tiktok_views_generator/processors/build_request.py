"""Build the final HTTP request envelope for the view delivery."""
from __future__ import annotations

from typing import Any

from tiktok_views_generator.models.job import ViewJob
from tiktok_views_generator.processors.base import BaseProcessor


class BuildRequest(BaseProcessor):
    name = "build_request"

    async def run(self, job: ViewJob, ctx: Any) -> ViewJob:
        watch = ctx.cfg["runtime"]["watch_seconds"]
        job.request = {
            "method": "POST",
            "url": f"https://www.tiktok.com/api/item/detail/?itemId={job.video_id}",
            "headers": job.headers,
            "proxy": job.proxy,
            "timeout": ctx.cfg["runtime"]["request_timeout"],
            "meta": {"watch_seconds": watch, "session_id": job.session_id},
        }
        return job