"""IO helpers for reading and persisting HR datasets."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import pandas as pd

from .config import DatasetConfig, resolve_path


def load_raw_dataset(
    config: DatasetConfig,
    *,
    path_override: Optional[Path] = None,
) -> pd.DataFrame:
    """
    Load the HR dataset using sane defaults.

    Parameters
    ----------
    config:
        Dataset configuration describing column expectations and default
        locations.
    path_override:
        Optional path override when the caller wants to load a different file.

    Returns
    -------
    pandas.DataFrame
        The raw dataset.
    """

    csv_path = resolve_path(path_override or config.input_path)
    if not csv_path.exists():
        raise FileNotFoundError(
            f"Input dataset not found at {csv_path}. "
            "Update DatasetConfig.input_path or provide a path_override."
        )

    df = pd.read_csv(
        csv_path,
        dtype=config.dtype_overrides,
        low_memory=False,
    )
    return _strip_bom_columns(df)


def write_clean_dataset(
    df: pd.DataFrame,
    config: DatasetConfig,
    *,
    path_override: Optional[Path] = None,
) -> Path:
    """
    Persist the cleaned dataset to disk.

    Parameters
    ----------
    df:
        Cleaned HR dataset.
    config:
        Dataset configuration describing column expectations and default
        locations.
    path_override:
        Optional path override for the output file.

    Returns
    -------
    Path
        Absolute path to the written CSV file.
    """

    output_path = resolve_path(path_override or config.output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    return output_path


def _strip_bom_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Remove any byte-order-mark artefacts from column headers."""

    bom_prefix = "\ufeff"
    rename_map = {
        column: column.lstrip(bom_prefix)
        for column in df.columns
        if column.startswith(bom_prefix)
    }
    return df.rename(columns=rename_map)
