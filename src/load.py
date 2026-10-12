import sqlite3

import pandas as pd


def load_table(df: pd.DataFrame, db_path: str, table: str) -> None:
    with sqlite3.connect(db_path) as conn:
        df.to_sql(table, conn, if_exists="replace", index=False)