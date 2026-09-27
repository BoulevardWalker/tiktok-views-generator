"""Paste ingest — pulls from a clipboard file written by the GUI."""
from __future__ import annotations

import os
from pathlib import Path
from typing import AsyncIterator

from tiktok_views_generator.handlers.base import BaseIngestHandler
from tiktok_views_generator.models.job import ViewJob
from tiktok_views_generator.utils.url import normalize_tiktok_url


class PasteHandler(BaseIngestHandler):
    name = "paste"

    def __init__(self, clipboard_file: str | None = None) -> None:
        self.clipboard_file = Path(
            clipboard_file or os.getenv("TTVG_CLIPBOARD_FILE", "sessions/clipboard.txt")
        )

    async def ingest(self, source: str) -> AsyncIterator[ViewJob]:
        text = self.clipboard_file.read_text(encoding="utf-8") if self.clipboard_file.is_file() else source
        for token in text.split():
            url = normalize_tiktok_url(token)
            if url is None:
                continue
            yield ViewJob(url=url, source=self.name)