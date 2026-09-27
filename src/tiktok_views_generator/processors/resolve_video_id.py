"""Resolve video id from a TikTok URL: /@user/video/<id>."""
from __future__ import annotations

import re
from typing import Any

from tiktok_views_generator.models.job import ViewJob
from tiktok_views_generator.processors.base import BaseProcessor

_VIDEO_ID_RE = re.compile(r"/video/(\d{15,21})")


class ResolveVideoId(BaseProcessor):
    name = "resolve_video_id"

    async def run(self, job: ViewJob, ctx: Any) -> ViewJob:
        m = _VIDEO_ID_RE.search(job.url)
        if not m:
            raise ValueError(f"no video id in {job.url}")
        job.video_id = m.group(1)
        return job