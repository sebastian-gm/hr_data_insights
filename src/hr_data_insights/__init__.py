"""
Utilities for cleaning, validating, and analysing Human Resources datasets.

The package exposes high-level helpers via ``hr_data_insights.pipeline`` while
keeping domain-specific logic inside dedicated modules (cleaning, analytics,
validation).  Importing the package initialises nothing; consumers should call
``hr_data_insights.pipeline.run`` or the underlying functions directly.
"""

from .config import DatasetConfig, DEFAULT_CONFIG  # noqa: F401
from .pipeline import run_pipeline  # noqa: F401

__all__ = [
    "DatasetConfig",
    "DEFAULT_CONFIG",
    "run_pipeline",
]
