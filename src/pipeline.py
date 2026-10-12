import os

from dotenv import load_dotenv

from src.extract import extract
from src.load import load_table
from src.transform import (
    global_daily_totals,
    to_daily_counts,
    top_countries_by_confirmed,
)


def main() -> None:
    load_dotenv()
    source = os.environ.get("SOURCE_CSV", "tests/fixtures/sample_covid.csv")
    db_path = os.environ.get("DB_PATH", "data/warehouse.db")
    top_n = int(os.environ.get("TOP_N_COUNTRIES", "10"))

    raw = extract(source)

    daily = to_daily_counts(raw)
    load_table(daily, db_path, "country_daily")
    load_table(global_daily_totals(daily), db_path, "global_daily")
    top = top_countries_by_confirmed(raw, n=top_n)
    load_table(top, db_path, "top_countries")

    print(f"Loaded {len(daily)} country-day rows into {db_path}")
    print(f"Top country by confirmed cases: {top.iloc[0]['Country']}")


if __name__ == "__main__":
    main()