import pandas as pd

from src.transform import to_daily_counts

RAW = pd.DataFrame({
    "Date": ["2022-01-01", "2022-01-02", "2022-01-03", "2022-01-04"] * 2,
    "Country": ["Testland"] * 4 + ["Otherland"] * 4,
    "Confirmed": [100, 120, 115, 130, 50, 80, 95, 110],
    "Recovered": [0] * 8,
    "Deaths": [2, 3, 3, 4, 1, 1, 2, 2],
})


def test_first_day_uses_cumulative_value_as_new_count():
    out = to_daily_counts(RAW)
    first = out[(out["Country"] == "Testland") & (out["Date"] == "2022-01-01")]
    assert first["new_cases"].iloc[0] == 100


def test_negative_correction_is_clipped_to_zero():
    out = to_daily_counts(RAW)
    day = out[(out["Country"] == "Testland") & (out["Date"] == "2022-01-03")]
    assert day["new_cases"].iloc[0] == 0