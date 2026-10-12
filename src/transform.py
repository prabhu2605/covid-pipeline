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

# 7-day rolling average smooths day-of-week reporting noise.
    df["new_cases_7d_avg"] = (
        df.groupby("Country")["new_cases"]
        .transform(lambda s: s.rolling(7, min_periods=1).mean())
        .round(1)
    )

    out = df[["Date", "Country", "new_cases", "new_deaths", "new_cases_7d_avg"]].copy()
    out["Date"] = out["Date"].astype(str)
    return out.reset_index(drop=True)



def top_countries_by_confirmed(raw_df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    latest = raw_df.sort_values("Date").groupby("Country", as_index=False).tail(1)
    top = latest.sort_values("Confirmed", ascending=False).head(n)
    return top[["Country", "Confirmed", "Deaths"]].reset_index(drop=True)


def global_daily_totals(daily_counts: pd.DataFrame) -> pd.DataFrame:
    return (
        daily_counts.groupby("Date", as_index=False)["new_cases"]
        .sum()
        .rename(columns={"new_cases": "global_new_cases"})
    )

