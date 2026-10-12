import sqlite3

from src.pipeline import main


def test_pipeline_end_to_end(tmp_path, monkeypatch):
    db_path = tmp_path / "warehouse.db"
    monkeypatch.setenv("SOURCE_CSV", "tests/fixtures/sample_covid.csv")
    monkeypatch.setenv("DB_PATH", str(db_path))
    monkeypatch.setenv("TOP_N_COUNTRIES", "2")

    main()

    with sqlite3.connect(db_path) as conn:
        tables = {
            row[0]
            for row in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            )
        }
        assert {"country_daily", "global_daily", "top_countries"} <= tables
        top = conn.execute(
            "SELECT Country FROM top_countries ORDER BY Confirmed DESC LIMIT 1"
        ).fetchone()
        assert top[0] == "Testland"