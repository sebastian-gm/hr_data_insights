"""Lightweight data validation primitives for HR datasets."""

from __future__ import annotations

from typing import Iterable, List

import pandas as pd


def validate_unique_employee_id(df: pd.DataFrame) -> list[str]:
    """Ensure employee IDs are unique and non-null."""

    issues: List[str] = []
    if "employee_id" not in df.columns:
        issues.append("Column 'employee_id' not present in dataset.")
        return issues

    if df["employee_id"].isna().any():
        issues.append("Dataset contains null values in 'employee_id'.")

    duplicates = df["employee_id"].duplicated()
    if duplicates.any():
        dup_values = df.loc[duplicates, "employee_id"].unique()
        sample = ", ".join(map(str, dup_values[:5]))
        issues.append(
            f"Dataset contains duplicate employee_id values (sample): {sample}"
        )
    return issues


def validate_chronology(df: pd.DataFrame) -> list[str]:
    """Check that hire dates precede termination dates."""

    issues: List[str] = []
    if {"hire_date", "termdate"} - set(df.columns):
        return issues

    invalid = df["termdate"].notna() & (df["termdate"] < df["hire_date"])
    if invalid.any():
        count = int(invalid.sum())
        issues.append(
            f"{count} records have termination dates before hire dates."
        )
    return issues


def validate_age_bounds(
    df: pd.DataFrame,
    *,
    minimum_age: int = 16,
    maximum_age: int = 90,
) -> list[str]:
    """Warn about implausible ages."""

    issues: List[str] = []
    if "age" not in df.columns:
        return issues

    too_young = df["age"].dropna() < minimum_age
    if too_young.any():
        issues.append(
            f"{int(too_young.sum())} employees fall below the minimum age of {minimum_age}."
        )

    too_old = df["age"].dropna() > maximum_age
    if too_old.any():
        issues.append(
            f"{int(too_old.sum())} employees exceed the maximum age of {maximum_age}."
        )
    return issues


def run_validations(
    df: pd.DataFrame,
    validators: Iterable = (
        validate_unique_employee_id,
        validate_chronology,
        validate_age_bounds,
    ),
) -> list[str]:
    """Execute validators, returning a list of warning messages."""

    issues: List[str] = []
    for validator in validators:
        issues.extend(validator(df))
    return issues
