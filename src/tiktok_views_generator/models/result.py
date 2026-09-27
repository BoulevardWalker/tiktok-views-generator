"""ViewResult — terminal state of a ViewJob, handed to drivers."""
from __future__ import annotations

import time

from pydantic import BaseModel, Field

from tiktok_views_generator.models.job import ViewJob


class ViewResult(BaseModel):
    url: str
    video_id: str | None = None
    session_id: str | None = None
    status: str
    error: str | None = None
    ts: float = Field(default_factory=time.time)

    @classmethod
    def from_job(cls, job: ViewJob, status: str, error: str | None = None) -> "ViewResult":
        return cls(
            url=job.url,
            video_id=job.video_id,
            session_id=job.session_id,
            status=status,
            error=error,
        )