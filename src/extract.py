import pandas as pd

expected_columns = {"Date", "Country", "Confirmed", "Recovered", "Deaths"}
def extract(source: str) -> pd.DataFrame:
    df = pd.read_csv(source)
    missing = expected_columns - set(df.columns)
    if missing:
        raise ValueError(f"Source is missing expected columns: {missing}")
    return df