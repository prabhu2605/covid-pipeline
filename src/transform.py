import pandas as pd


def to_daily_counts(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values(["Country", "Date"])

    df["new_cases"] = df.groupby("Country")["Confirmed"].diff()
    df["new_deaths"] = df.groupby("Country")["Deaths"].diff()

    out = df[["Date", "Country", "new_cases", "new_deaths"]].copy()
    out["Date"] = out["Date"].astype(str)
    return out.reset_index(drop=True)