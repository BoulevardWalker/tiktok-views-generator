"""Entry point: parse args, wire pipeline, run."""
from __future__ import annotations

import argparse
import asyncio
import logging
import sys

from tiktok_views_generator.config.loader import load_config
from tiktok_views_generator.drivers import DRIVERS
from tiktok_views_generator.handlers import HANDLERS
from tiktok_views_generator.pipeline import Pipeline
from tiktok_views_generator.processors import PROCESSORS


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="tiktok-views", description="TikTok Views Generator")
    p.add_argument("source", nargs="?", help="URL, file path, or CSV of TikTok video URLs")
    p.add_argument("--config", default=None, help="path to YAML config")
    p.add_argument("--handler", default=None, help="ingest handler (cli, csv, paste)")
    p.add_argument("--driver", default=None, help="output driver (stdout, jsonl, sqlite, gui)")
    p.add_argument("--concurrency", type=int, default=None)
    p.add_argument("--views", type=int, default=None, help="views per video target")
    p.add_argument("--dry-run", action="store_true")
    return p


async def _run(args: argparse.Namespace) -> int:
    cfg = load_config(args.config)

    if args.concurrency:
        cfg["runtime"]["concurrency"] = args.concurrency
    if args.driver:
        cfg["driver"]["name"] = args.driver

    handler_name = args.handler or cfg["ingest"]["handler"]
    if handler_name not in HANDLERS:
        print(f"unknown handler: {handler_name}", file=sys.stderr)
        return 2

    driver_name = cfg["driver"]["name"]
    if driver_name not in DRIVERS:
        print(f"unknown driver: {driver_name}", file=sys.stderr)
        return 2

    handler = HANDLERS[handler_name]()
    driver = DRIVERS[driver_name](**cfg["driver"].get("options", {}))
    pipeline = Pipeline(cfg=cfg, handler=handler, driver=driver, processors=PROCESSORS)

    if args.dry_run:
        async for job in handler.ingest(args.source or ""):
            print(f"[dry-run] {job.url}")
        return 0

    stats = await pipeline.run(args.source or "")
    logging.getLogger("ttvg").info(
        "done: submitted=%d ok=%d fail=%d", stats.submitted, stats.ok, stats.failed
    )
    return 0 if stats.failed == 0 else 1


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    cfg = load_config(args.config)
    logging.basicConfig(
        level=cfg.get("logging", {}).get("level", "INFO"),
        format="%(asctime)s %(levelname)s %(name)s :: %(message)s",
    )
    try:
        return asyncio.run(_run(args))
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    raise SystemExit(main())