"""Mint or reuse a session for the job."""
from __future__ import annotations

from typing import Any

from tiktok_views_generator.models.job import ViewJob
from tiktok_views_generator.processors.base import BaseProcessor


class MintSession(BaseProcessor):
    name = "mint_session"

    async def run(self, job: ViewJob, ctx: Any) -> ViewJob:
        session = await ctx.session_store.acquire(job.video_id)
        job.session_id = session.id
        job.headers = dict(session.headers)
        return job