"""Reusable analytical aggregates mirroring common HR business questions."""

from __future__ import annotations

from typing import Iterable

import pandas as pd

AGE_GROUP_BOUNDS = [18, 25, 35, 45, 55, 65, float("inf")]
AGE_GROUP_LABELS = ["18-24", "25-34", "35-44", "45-54", "55-64", "65+"]


def _filter_adult_employees(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["age"].notna() & (df["age"] >= 18)]


def gender_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    adults = _filter_adult_employees(df)
    result = adults.groupby("gender", dropna=False)["employee_id"].count().reset_index()
    return result.rename(columns={"employee_id": "employee_count"})


def race_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    adults = _filter_adult_employees(df)
    result = (
        adults.groupby("race", dropna=False)["employee_id"].count().reset_index()
        .sort_values("employee_count", ascending=False)
    )
    return result.rename(columns={"employee_id": "employee_count"})


def age_distribution(df: pd.DataFrame) -> dict[str, pd.DataFrame | pd.Series]:
    adults = _filter_adult_employees(df)
    return {
        "range": adults["age"].agg(["min", "max"]).rename({"min": "youngest", "max": "oldest"}),
        "by_decade": (
            adults.assign(age_decade=(adults["age"] // 10) * 10)
            .groupby("age_decade")["employee_id"]
            .count()
            .reset_index()
            .rename(columns={"employee_id": "employee_count"})
        ),
        "by_band": (
            adults.assign(
                age_group=pd.cut(
                    adults["age"],
                    bins=AGE_GROUP_BOUNDS,
                    labels=AGE_GROUP_LABELS,
                    right=False,
                    include_lowest=True,
                )
            )
            .groupby("age_group")["employee_id"]
            .count()
            .reset_index()
            .rename(columns={"employee_id": "employee_count"})
        ),
    }


def age_gender_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    adults = _filter_adult_employees(df)
    grouped = (
        adults.assign(
            age_group=pd.cut(
                adults["age"],
                bins=AGE_GROUP_BOUNDS,
                labels=AGE_GROUP_LABELS,
                right=False,
                include_lowest=True,
            )
        )
        .groupby(["age_group", "gender"], dropna=False)["employee_id"]
        .count()
        .reset_index()
        .rename(columns={"employee_id": "employee_count"})
        .sort_values(["age_group", "gender"])
    )
    return grouped


def location_distribution(df: pd.DataFrame) -> pd.DataFrame:
    adults = _filter_adult_employees(df)
    return (
        adults.groupby("location", dropna=False)["employee_id"]
        .count()
        .reset_index()
        .rename(columns={"employee_id": "employee_count"})
        .sort_values("employee_count", ascending=False)
    )


def average_terminated_tenure(df: pd.DataFrame) -> float:
    adults = _filter_adult_employees(df)
    terminated = adults[
        adults["termdate"].notna() & (adults["termdate"] <= pd.Timestamp.today())
    ]
    if terminated.empty:
        return float("nan")
    return round((terminated["termdate"] - terminated["hire_date"]).dt.days.mean() / 365, 2)


def department_gender_distribution(df: pd.DataFrame) -> pd.DataFrame:
    adults = _filter_adult_employees(df)
    return (
        adults.groupby(["department", "gender"], dropna=False)["employee_id"]
        .count()
        .reset_index()
        .rename(columns={"employee_id": "employee_count"})
        .sort_values(["department", "gender"])
    )


def jobtitle_distribution(df: pd.DataFrame, *, top_n: int | None = None) -> pd.DataFrame:
    adults = _filter_adult_employees(df)
    grouped = (
        adults.groupby("jobtitle", dropna=False)["employee_id"]
        .count()
        .reset_index()
        .rename(columns={"employee_id": "employee_count"})
        .sort_values("employee_count", ascending=False)
    )
    if top_n:
        return grouped.head(top_n)
    return grouped


def department_turnover(df: pd.DataFrame) -> pd.DataFrame:
    adults = _filter_adult_employees(df)
    terminated_mask = adults["termdate"].notna() & (adults["termdate"] <= pd.Timestamp.today())

    summary = (
        adults.assign(
            terminated=terminated_mask,
        )
        .groupby("department")
        .agg(
            total_headcount=("employee_id", "count"),
            terminated_count=("terminated", "sum"),
        )
        .reset_index()
    )
    summary["active_count"] = summary["total_headcount"] - summary["terminated_count"]
    summary["turnover_rate"] = summary["terminated_count"] / summary["total_headcount"]
    return summary.sort_values("turnover_rate", ascending=False)


def location_state_distribution(df: pd.DataFrame) -> pd.DataFrame:
    adults = _filter_adult_employees(df)
    return (
        adults.groupby("location_state", dropna=False)["employee_id"]
        .count()
        .reset_index()
        .rename(columns={"employee_id": "employee_count"})
        .sort_values("employee_count", ascending=False)
    )


def employee_count_over_time(df: pd.DataFrame) -> pd.DataFrame:
    adults = _filter_adult_employees(df)
    hires = adults.assign(hire_year=adults["hire_date"].dt.year)
    terminated = adults[
        adults["termdate"].notna() & (adults["termdate"] <= pd.Timestamp.today())
    ].assign(term_year=lambda frame: frame["termdate"].dt.year)

    hire_counts = hires.groupby("hire_year")["employee_id"].count()
    term_counts = terminated.groupby("term_year")["employee_id"].count()

    calendar = pd.Index(sorted(set(hire_counts.index) | set(term_counts.index)), name="year")
    summary = pd.DataFrame(index=calendar)
    summary["hires"] = hire_counts
    summary["terminations"] = term_counts
    summary = summary.fillna(0).astype(int)
    summary["net_change"] = summary["hires"] - summary["terminations"]
    summary["net_change_percent"] = (
        summary["net_change"] / summary["hires"].replace(0, pd.NA)
    ).mul(100).round(2)
    return summary.reset_index()


def department_tenure_distribution(df: pd.DataFrame) -> pd.DataFrame:
    adults = _filter_adult_employees(df)
    terminated = adults[
        adults["termdate"].notna() & (adults["termdate"] <= pd.Timestamp.today())
    ]
    return (
        terminated.assign(
            tenure_years=lambda frame: (frame["termdate"] - frame["hire_date"]).dt.days / 365.25
        )
        .groupby("department")["tenure_years"]
        .mean()
        .round(1)
        .reset_index()
        .rename(columns={"tenure_years": "avg_tenure_years"})
    )


def calculate_all_metrics(df: pd.DataFrame) -> dict[str, pd.DataFrame | pd.Series | float]:
    """
    Convenience helper that mirrors the existing SQL business questions.
    """

    return {
        "gender_breakdown": gender_breakdown(df),
        "race_breakdown": race_breakdown(df),
        "age_distribution": age_distribution(df),
        "age_gender_breakdown": age_gender_breakdown(df),
        "location_distribution": location_distribution(df),
        "average_terminated_tenure": average_terminated_tenure(df),
        "department_gender_distribution": department_gender_distribution(df),
        "jobtitle_distribution": jobtitle_distribution(df),
        "department_turnover": department_turnover(df),
        "location_state_distribution": location_state_distribution(df),
        "employee_count_over_time": employee_count_over_time(df),
        "department_tenure_distribution": department_tenure_distribution(df),
    }
