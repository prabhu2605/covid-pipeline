import pytest

from src.extract import extract


def test_extract_reads_local_csv(tmp_path):
    csv = tmp_path / "covid.csv"
    csv.write_text(
        "Date,Country,Confirmed,Recovered,Deaths\n"
        "2022-01-01,Testland,100,0,2\n"
    )
    df = extract(str(csv))
    assert len(df) == 1
    assert df.loc[0, "Country"] == "Testland"
def test_extract_rejects_missing_columns(tmp_path):
    csv = tmp_path / "bad.csv"
    csv.write_text("Date,Country\n2022-01-01,Testland\n")
    with pytest.raises(ValueError, match="missing expected columns"):
        extract(str(csv))