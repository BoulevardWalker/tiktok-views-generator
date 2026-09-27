"""CLI ingest — one URL, whitespace-separated URLs, or newline-separated."""
from __future__ import annotations

from typing import AsyncIterator

from tiktok_views_generator.handlers.base import BaseIngestHandler
from tiktok_views_generator.models.job import ViewJob
from tiktok_views_generator.utils.url import normalize_tiktok_url


class CliHandler(BaseIngestHandler):
    name = "cli"

    async def ingest(self, source: str) -> AsyncIterator[ViewJob]:
        for token in source.replace(",", " ").split():
            url = normalize_tiktok_url(token)
            if url is None:
                continue
            yield ViewJob(url=url, source=self.name)