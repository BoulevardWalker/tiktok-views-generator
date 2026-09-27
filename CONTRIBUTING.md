# Contributing to tiktok-views-generator

Thanks for wanting to push the tater. This repo is a Windows-first Python desktop tool that runs a view-delivery pipeline against TikTok video URLs. Contributions are welcome — patches, ingest handlers, driver backends, proxy loaders, docs.

## Ground rules

- Python 3.10+. Target Windows 10/11 primary, POSIX secondary.
- One PR = one concern. Don't bundle a driver rewrite with a lint sweep.
- Run `ruff check src tests` and `pytest -q` before opening the PR.
- Public surface (CLI flags, config keys, driver names) changes need a note in the PR body.

## Repo shape

We use a pipeline/worker layout:

- `src/tiktok_views_generator/handlers/` — **ingest handlers**. Take a raw input (CLI arg, CSV, pasted URL) and produce `ViewJob` objects.
- `src/tiktok_views_generator/processors/` — **job processors**. Transform a `ViewJob` (resolve video id, mint session, attach proxy, build request).
- `src/tiktok_views_generator/drivers/` — **output drivers**. Take a completed `ViewResult` and push it (stdout, JSONL, SQLite, GUI signal).
- `src/tiktok_views_generator/services/` — long-lived services (proxy pool, session store, rate limiter).
- `src/tiktok_views_generator/models/` — pydantic models. No logic beyond validation.
- `src/tiktok_views_generator/utils/` — pure helpers. No I/O in here.
- `src/tiktok_views_generator/config/` — YAML defaults + loader.

## Adding an ingest handler

1. Subclass `BaseIngestHandler` in `handlers/base.py`.
2. Implement `async def ingest(self, source: str) -> AsyncIterator[ViewJob]`.
3. Register in `handlers/__init__.py` → `HANDLERS`.
4. Add a test in `tests/test_handlers.py` with a fake source string.

## Adding a driver

Subclass `BaseDriver` in `drivers/base.py`, implement `async def emit(self, result: ViewResult) -> None` and `async def close(self) -> None`. Register in `drivers/__init__.py` → `DRIVERS`.

## Style

- Async everywhere on the hot path. No sync `requests` calls in handlers/processors/drivers.
- Logging via `logging.getLogger(__name__)`. No `print` outside `drivers/stdout_driver.py`.
- Type hints on public functions. `mypy --strict` is aspirational, not enforced.

## Legal

This is a hobbyist/educational tool. You are responsible for how you run it. Do not open issues asking the maintainers to bypass rate limits on production accounts.