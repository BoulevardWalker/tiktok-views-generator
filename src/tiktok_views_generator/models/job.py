"""ViewJob — a single unit of work flowing through the pipeline."""
from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class ViewJob(BaseModel):
    url: str
    source: str = "cli"
    video_id: str | None = None
    session_id: str | None = None
    headers: dict[str, str] = Field(default_factory=dict)
    proxy: str | None = None
    request: dict[str, Any] | None = None