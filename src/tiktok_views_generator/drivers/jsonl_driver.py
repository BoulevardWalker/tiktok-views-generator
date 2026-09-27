"""jsonl driver — append every result to a JSONL file."""
from __future__ import annotations

import json
from pathlib import Path

from tiktok_views_generator.drivers.base import BaseDriver
from tiktok_views_generator.models.result import ViewResult


class JsonlDriver(BaseDriver):
    name = "jsonl"

    def __init__(self, path: str = "out/results.jsonl") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._fh = self.path.open("a", encoding="utf-8")

    async def emit(self, result: ViewResult) -> None:
        self._fh.write(json.dumps(result.model_dump()) + "\n")
        self._fh.flush()

    async def close(self) -> None:
        self._fh.close()