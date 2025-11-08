#!/usr/bin/env python
"""
Generate PNG visualisations referenced in the HR Workforce Intelligence report.

Usage
-----
python scripts/create_visuals.py

The script outputs four PNG files in ``docs/visualizations``:
    * age_composition.png
    * department_headcount.png
    * department_attrition.png
    * location_split.png

Requirements
------------
matplotlib>=3.6
pandas>=1.5
numpy>=1.24
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

plt.style.use("seaborn-v0_8-whitegrid")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("data/processed/Cleaned_HR_Data.csv"),
        help="Path to the cleaned HR dataset.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("docs/visualizations"),
        help="Directory where PNG files will be stored.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    # Some operating systems require an explicit matplotlib configuration dir.
    os.environ.setdefault(
        "MPLCONFIGDIR", str(args.output_dir / ".mplconfig"),
    )
    Path(os.environ["MPLCONFIGDIR"]).mkdir(parents=True, exist_ok=True)

    current_date = pd.Timestamp("today").normalize()
    df = pd.read_csv(
        args.input,
        parse_dates=["birthdate", "hire_date", "termdate"],
    )

    active = df[(df["termdate"].isna()) | (df["termdate"] > current_date)].copy()

    _plot_age_composition(df, args.output_dir)
    _plot_department_headcount(active, args.output_dir)
    _plot_department_attrition(df, current_date, args.output_dir)
    _plot_location_split(active, args.output_dir)

    print("Saved visuals to", args.output_dir.resolve())
    return 0


def _plot_age_composition(df: pd.DataFrame, output_dir: Path) -> None:
    bins = [18, 25, 35, 45, 55, 65, 200]
    labels = ["18-24", "25-34", "35-44", "45-54", "55-64", "65+"]
    age_band = pd.cut(df["age"], bins=bins, labels=labels, right=False)
    age_pct = age_band.value_counts().reindex(labels).fillna(0)
    age_pct = age_pct / age_pct.sum() * 100

    fig, ax = plt.subplots(figsize=(8, 5))
    age_pct.plot(kind="bar", color="#4477AA", ax=ax)
    ax.set_ylabel("Share of Workforce (%)")
    ax.set_xlabel("Age Band (years)")
    ax.set_title("Workforce Age Composition")
    ax.set_ylim(0, max(age_pct.max() + 5, 35))
    for patch, value in zip(ax.patches, age_pct):
        ax.annotate(
            f"{value:.1f}%",
            (patch.get_x() + patch.get_width() / 2, patch.get_height()),
            ha="center",
            va="bottom",
            fontsize=9,
        )
    fig.tight_layout()
    fig.savefig(output_dir / "age_composition.png", dpi=150)
    plt.close(fig)


def _plot_department_headcount(active: pd.DataFrame, output_dir: Path) -> None:
    headcount = active["department"].value_counts().head(10)

    fig, ax = plt.subplots(figsize=(9, 5))
    headcount.plot(kind="barh", color="#66AA55", ax=ax)
    ax.set_xlabel("Active Headcount")
    ax.set_ylabel("Department")
    ax.invert_yaxis()
    ax.set_title("Top Departments by Active Headcount")
    for patch, value in zip(ax.patches, headcount.values):
        ax.annotate(
            f"{value:,}",
            (value, patch.get_y() + patch.get_height() / 2),
            ha="left",
            va="center",
            fontsize=9,
        )
    fig.tight_layout()
    fig.savefig(output_dir / "department_headcount.png", dpi=150)
    plt.close(fig)


def _plot_department_attrition(
    df: pd.DataFrame,
    current_date: pd.Timestamp,
    output_dir: Path,
) -> None:
    attrition = (
        df.groupby("department")
        .agg(
            headcount=("id", "count"),
            terminations=(
                "termdate",
                lambda s: ((s.notna()) & (s <= current_date)).sum(),
            ),
        )
    )
    attrition["attrition_rate"] = attrition["terminations"] / attrition["headcount"]
    attrition = attrition[attrition["headcount"] >= 200]
    attrition = attrition.sort_values("attrition_rate", ascending=False).head(10)

    fig, ax = plt.subplots(figsize=(9, 5))
    (attrition["attrition_rate"] * 100).plot(kind="bar", color="#CC6677", ax=ax)
    ax.set_ylabel("Attrition Rate (%)")
    ax.set_xlabel("Department")
    ax.set_title("Highest Attrition Departments (Headcount ≥ 200)")
    ax.set_ylim(0, max((attrition["attrition_rate"] * 100).max() + 2, 20))
    for patch, value in zip(ax.patches, attrition["attrition_rate"] * 100):
        ax.annotate(
            f"{value:.1f}%",
            (patch.get_x() + patch.get_width() / 2, value),
            ha="center",
            va="bottom",
            fontsize=9,
        )
    fig.tight_layout()
    fig.savefig(output_dir / "department_attrition.png", dpi=150)
    plt.close(fig)


def _plot_location_split(active: pd.DataFrame, output_dir: Path) -> None:
    location_counts = active["location"].value_counts()
    total = location_counts.sum()
    labels = [
        f"{label} ({value / total * 100:.1f}%)"
        for label, value in location_counts.items()
    ]

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(
        location_counts.values,
        labels=labels,
        autopct="%1.1f%%",
        startangle=140,
        colors=["#88CCEE", "#DDCC77"],
    )
    ax.set_title("Active Workforce by Work Location")
    fig.tight_layout()
    fig.savefig(output_dir / "location_split.png", dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    raise SystemExit(main())
