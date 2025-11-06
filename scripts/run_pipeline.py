#!/usr/bin/env python
"""
Command-line entrypoint for the HR analytics pipeline.

Usage
-----
python scripts/run_pipeline.py --input data/raw/Human\\ Resources.csv --output data/processed/cleaned.csv
"""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

import pandas as pd

from hr_data_insights.pipeline import run_pipeline
from hr_data_insights.config import DatasetConfig, DEFAULT_CONFIG


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the HR data cleaning and analytics pipeline.",
    )
    parser.add_argument(
        "--input",
        type=Path,
        help="Path to the raw HR CSV (defaults to dataset config).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Desired output path for the cleaned CSV.",
    )
    parser.add_argument(
        "--no-metrics",
        action="store_true",
        help="Skip analytics calculations to focus purely on data cleaning.",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        help="Python log level (DEBUG, INFO, WARNING, ...).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    logging.basicConfig(
        level=getattr(logging, args.log_level.upper(), logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    )

    config = DatasetConfig() if args.input or args.output else DEFAULT_CONFIG
    result = run_pipeline(
        config=config,
        input_path=args.input,
        output_path=args.output,
        compute_metrics=not args.no_metrics,
    )

    cleaned: pd.DataFrame = result["cleaned"]
    print(f"Cleaned records: {len(cleaned):,}")
    print(f"Output written to: {result['output_path']}")
    if result["validation_messages"]:
        print("\nValidation warnings:")
        for message in result["validation_messages"]:
            print(f"- {message}")

    analytics = result.get("analytics")
    if analytics:
        print("\nAvailable analytics tables:")
        for name, table in analytics.items():
            if isinstance(table, dict):
                keys = ", ".join(table.keys())
                print(f"- {name} ({keys})")
            else:
                print(f"- {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
