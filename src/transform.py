import pandas as pd


def to_daily_counts(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values(["Country", "Date"])

    df["new_cases"] = df.groupby("Country")["Confirmed"].diff()
    df["new_deaths"] = df.groupby("Country")["Deaths"].diff()

    first_day = df.groupby("Country").cumcount() == 0
    df.loc[first_day, "new_cases"] = df.loc[first_day, "Confirmed"]
    df.loc[first_day, "new_deaths"] = df.loc[first_day, "Deaths"]

    df["new_cases"] = df["new_cases"].clip(lower=0)
    df["new_deaths"] = df["new_deaths"].clip(lower=0)
    
    out = df[["Date", "Country", "new_cases", "new_deaths"]].copy()
    out["Date"] = out["Date"].astype(str)
    return out.reset_index(drop=True)