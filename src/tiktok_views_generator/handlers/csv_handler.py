"""CSV ingest — reads a file, expects URL in column 0 or a header named 'url'."""
from __future__ import annotations

import csv
from pathlib import Path
from typing import AsyncIterator

from tiktok_views_generator.handlers.base import BaseIngestHandler
from tiktok_views_generator.models.job import ViewJob
from tiktok_views_generator.utils.url import normalize_tiktok_url


class CsvHandler(BaseIngestHandler):
    name = "csv"

    async def ingest(self, source: str) -> AsyncIterator[ViewJob]:
        path = Path(source)
        if not path.is_file():
            raise FileNotFoundError(f"csv source not found: {source}")
        with path.open("r", encoding="utf-8", newline="") as fh:
            reader = csv.reader(fh)
            header = next(reader, None)
            url_idx = 0
            if header and "url" in [c.strip().lower() for c in header]:
                url_idx = [c.strip().lower() for c in header].index("url")
            for row in reader:
                if not row or url_idx >= len(row):
                    continue
                url = normalize_tiktok_url(row[url_idx])
                if url is None:
                    continue
                yield ViewJob(url=url, source=self.name)