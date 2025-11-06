"""Core data-cleaning routines for the HR analytics dataset."""

from __future__ import annotations

from typing import Iterable, Mapping, Sequence

import numpy as np
import pandas as pd

from .config import DatasetConfig

ColumnCollection = Sequence[str] | Iterable[str]


def clean_dataset(
    df: pd.DataFrame,
    config: DatasetConfig,
    *,
    as_of: pd.Timestamp | None = None,
    minimum_age: int = 18,
) -> pd.DataFrame:
    """
    Apply canonical cleaning steps to the HR dataset.

    Parameters
    ----------
    df:
        Raw HR dataset.
    config:
        Dataset configuration describing required columns and processing
        preferences.
    as_of:
        Reference date (defaults to today) used for age and tenure calculations.
    minimum_age:
        Minimum allowed employee age. Records below this threshold are dropped.

    Returns
    -------
    pandas.DataFrame
        Cleaned dataset ready for downstream analytics.
    """

    working = df.copy()
    working.columns = canonicalise_column_names(working.columns)
    validate_required_columns(working, config.required_columns)

    working = working.drop_duplicates(subset="id").reset_index(drop=True)
    working = _rename_columns(working)

    working = _standardise_dates(working, config.date_columns)
    working = _normalise_text_columns(
        working,
        titlecase_columns=config.string_titlecase_columns,
        normalise_columns=config.categorical_normalise_columns,
    )

    working["age"] = calculate_age(
        working["birthdate"],
        as_of=as_of,
    )

    working = working[working["age"].isna() | (working["age"] >= minimum_age)]
    working["age"] = working["age"].astype("Int64")

    working["tenure_years"] = calculate_tenure_years(
        working["hire_date"],
        working["termdate"],
        as_of=as_of,
    )

    working = _enforce_date_relationships(working)

    return working


def canonicalise_column_names(columns: ColumnCollection) -> list[str]:
    """Transform raw column labels into snake_case equivalents."""

    cleaned = []
    for column in columns:
        normalised = (
            str(column)
            .strip()
            .replace("/", "_")
            .replace("-", "_")
            .replace(" ", "_")
        )
        normalised = "".join(filter(str.isprintable, normalised))
        cleaned.append(normalised.lower())
    return cleaned


def validate_required_columns(df: pd.DataFrame, required: ColumnCollection) -> None:
    """Raise a ValueError when expected columns are missing."""

    missing = [column for column in required if column not in df.columns]
    if missing:
        raise ValueError(
            "Dataset is missing required columns: "
            + ", ".join(sorted(missing))
        )


def calculate_age(
    birthdate: pd.Series,
    *,
    as_of: pd.Timestamp | None = None,
) -> pd.Series:
    """Compute age in whole years."""

    if as_of is None:
        as_of = pd.Timestamp.today().normalize()
    else:
        as_of = pd.Timestamp(as_of).normalize()

    birthdate = pd.to_datetime(birthdate, errors="coerce")
    years = as_of.year - birthdate.dt.year
    has_had_birthday = (
        (as_of.month > birthdate.dt.month)
        | (
            (as_of.month == birthdate.dt.month)
            & (as_of.day >= birthdate.dt.day)
        )
    )
    return years - (~has_had_birthday.fillna(False)).astype(int)


def calculate_tenure_years(
    hire_date: pd.Series,
    termdate: pd.Series,
    *,
    as_of: pd.Timestamp | None = None,
) -> pd.Series:
    """
    Compute tenure in whole years between hire and termination (or today).
    """

    if as_of is None:
        as_of = pd.Timestamp.today().normalize()
    else:
        as_of = pd.Timestamp(as_of).normalize()

    hire = pd.to_datetime(hire_date, errors="coerce")
    term = pd.to_datetime(termdate, errors="coerce")
    end_dates = term.fillna(as_of)
    tenure_days = (end_dates - hire).dt.days
    tenure_years = (tenure_days / 365.25).round(1)
    tenure_years[tenure_days < 0] = np.nan
    return tenure_years


def _standardise_dates(df: pd.DataFrame, columns: ColumnCollection) -> pd.DataFrame:
    for column in columns:
        if column not in df.columns:
            continue
        parsed = pd.to_datetime(
            df[column],
            errors="coerce",
            utc=True,
        )
        parsed = parsed.dt.tz_convert(None)
        df[column] = parsed.dt.floor("D")
    return df


def _normalise_text_columns(
    df: pd.DataFrame,
    *,
    titlecase_columns: ColumnCollection,
    normalise_columns: ColumnCollection,
) -> pd.DataFrame:
    for column in normalise_columns:
        if column in df.columns:
            df[column] = _standardise_text(df[column])
    for column in titlecase_columns:
        if column in df.columns:
            df[column] = df[column].astype("string").str.title()
    return df


def _enforce_date_relationships(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ensure termination dates follow hire dates and purge impossible values.
    """

    mask = df["termdate"].notna() & (df["termdate"] < df["hire_date"])
    df.loc[mask, "termdate"] = pd.NaT
    return df


def _rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    rename_map: Mapping[str, str] = {
        "id": "employee_id",
    }
    return df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})


def _standardise_text(series: pd.Series) -> pd.Series:
    series = series.astype("string")
    series = series.str.strip()
    series = series.str.replace(r"\s+", " ", regex=True)
    return series
