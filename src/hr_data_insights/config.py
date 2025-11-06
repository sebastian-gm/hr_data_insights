"""Configuration objects describing how to work with the HR dataset."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Mapping, Sequence


@dataclass(frozen=True)
class DatasetConfig:
    """
    Parameters that control the behaviour of the HR data pipeline.

    Attributes
    ----------
    input_path:
        Location of the raw CSV input file.  The default assumes a
        ``data/raw`` directory relative to the project root.
    output_path:
        Location for the cleaned CSV output.  Parents are created on demand.
    date_columns:
        Column names that should be parsed as datetimes.
    string_titlecase_columns:
        Columns that should be formatted to title case (e.g., names).
    categorical_normalise_columns:
        Columns that require whitespace trimming and consistent casing.
    required_columns:
        Columns expected to exist in the raw dataset; validation will fail
        early if any are missing.
    dtype_overrides:
        Optional explicit dtypes to pass to `pandas.read_csv`.
    """

    input_path: Path = Path("data/raw/Human Resources.csv")
    output_path: Path = Path("data/processed/Cleaned_HR_Data.csv")
    date_columns: Sequence[str] = (
        "birthdate",
        "hire_date",
        "termdate",
    )
    string_titlecase_columns: Sequence[str] = (
        "first_name",
        "last_name",
    )
    categorical_normalise_columns: Sequence[str] = (
        "gender",
        "race",
        "department",
        "jobtitle",
        "location",
        "location_city",
        "location_state",
    )
    required_columns: Sequence[str] = (
        "id",
        "birthdate",
        "hire_date",
        "gender",
        "department",
    )
    dtype_overrides: Mapping[str, str] = field(
        default_factory=lambda: {
            "id": "string",
            "gender": "category",
            "race": "category",
            "department": "category",
            "jobtitle": "category",
            "location": "category",
            "location_city": "category",
            "location_state": "category",
        }
    )


DEFAULT_CONFIG = DatasetConfig()


def resolve_path(path: Path) -> Path:
    """
    Resolve a path relative to the project root.

    Parameters
    ----------
    path:
        Relative or absolute path to resolve.

    Returns
    -------
    Path
        An absolute path pointing to the requested location.
    """

    return (Path.cwd() / path).resolve()
