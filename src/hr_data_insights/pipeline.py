"""High-level orchestration for the HR data pipeline."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

import pandas as pd

from . import analytics, cleaning, io, validation
from .config import DatasetConfig, DEFAULT_CONFIG

LOGGER = logging.getLogger(__name__)


def run_pipeline(
    *,
    config: DatasetConfig = DEFAULT_CONFIG,
    input_path: Optional[Path] = None,
    output_path: Optional[Path] = None,
    compute_metrics: bool = True,
) -> dict[str, object]:
    """
    Execute the end-to-end HR analytics pipeline.

    Parameters
    ----------
    config:
        Dataset configuration controlling IO, parsing, and validation.
    input_path:
        Optional override for the raw dataset location.
    output_path:
        Optional override for the cleaned dataset destination.
    compute_metrics:
        Whether to compute analytics summaries alongside cleaning.

    Returns
    -------
    dict
        Dictionary containing the cleaned dataframe, validation messages,
        analytics (if requested), and the filesystem path to the exported CSV.
    """

    LOGGER.info("Loading HR dataset")
    raw_df = io.load_raw_dataset(config, path_override=input_path)

    LOGGER.info("Cleaning dataset")
    cleaned_df = cleaning.clean_dataset(raw_df, config)

    LOGGER.info("Running validations")
    validation_messages = validation.run_validations(cleaned_df)
    if validation_messages:
        LOGGER.warning("Validation warnings: %s", validation_messages)

    LOGGER.info("Writing cleaned dataset")
    output_csv = io.write_clean_dataset(
        cleaned_df,
        config,
        path_override=output_path,
    )

    metrics: Optional[dict[str, object]] = None
    if compute_metrics:
        LOGGER.info("Calculating analytics views")
        metrics = analytics.calculate_all_metrics(cleaned_df)

    return {
        "cleaned": cleaned_df,
        "validation_messages": validation_messages,
        "output_path": output_csv,
        "analytics": metrics,
    }


def dataframe_to_markdown(df: pd.DataFrame, *, max_rows: int = 10) -> str:
    """
    Render a dataframe as a Markdown table trimmed to the requested number of
    rows.  This is handy for README/report generation.
    """

    if df.shape[0] > max_rows:
        display_df = df.head(max_rows)
    else:
        display_df = df
    return display_df.to_markdown(index=False)
