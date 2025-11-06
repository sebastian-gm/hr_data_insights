import pandas as pd

from hr_data_insights.cleaning import clean_dataset
from hr_data_insights.config import DatasetConfig


def _sample_raw_frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "id": ["001", "002", "002"],
            "first name": ["alicia", "  mark", "  mark"],
            "last name": ["Nguyen", "ross", "ross"],
            "birthdate": ["01/15/1990", "1992-05-01", "1992-05-01"],
            "hire_date": ["2015-03-01", "04/01/2016", "04/01/2016"],
            "termdate": ["2019-05-02 00:00:00 UTC", "", ""],
            "gender": [" female", "MALE", "MALE"],
            "department": ["Sales", "Engineering", "Engineering"],
        }
    )


def test_clean_dataset_parses_dates_and_deduplicates():
    raw = _sample_raw_frame()
    cleaned = clean_dataset(raw, DatasetConfig())

    assert cleaned.shape[0] == 2
    for expected_column in {"employee_id", "first_name", "birthdate"}:
        assert expected_column in cleaned.columns

    assert cleaned.loc[cleaned["employee_id"] == "001", "birthdate"].iloc[0].strftime(
        "%Y-%m-%d"
    ) == "1990-01-15"
    assert cleaned["hire_date"].dt.tz is None


def test_clean_dataset_computes_age_and_tenure(monkeypatch):
    raw = _sample_raw_frame()
    reference_date = pd.Timestamp("2024-01-01")
    cleaned = clean_dataset(raw, DatasetConfig(), as_of=reference_date)

    alicia_age = cleaned.loc[cleaned["employee_id"] == "001", "age"].iat[0]
    assert int(alicia_age) == 33

    tenure_years = cleaned.loc[cleaned["employee_id"] == "001", "tenure_years"].iat[0]
    assert abs(float(tenure_years) - 4.2) < 0.1
