import pandas as pd

from python.validators import airport_validator


def test_validate_airports_removes_duplicate_and_null_codes(
    tmp_path, monkeypatch
):
    raw = tmp_path / "raw"
    bronze = tmp_path / "bronze"
    raw.mkdir()
    bronze.mkdir()

    df = pd.DataFrame({
        "airport_code": ["DEL", "DEL", None, "BOM"],
        "airport_name": [
            "Delhi Airport",
            "Delhi Airport",
            "Unknown Airport",
            "Mumbai Airport"
        ],
        "city": ["Delhi", "Delhi", "Unknown", "Mumbai"],
        "country": ["India", "India", "India", "India"]
    })

    df.to_csv(raw / "airport.csv", index=False)

    monkeypatch.setattr(airport_validator, "RAW_FOLDER", raw)
    monkeypatch.setattr(airport_validator, "BRONZE_FOLDER", bronze)

    airport_validator.validate_airports()

    result = pd.read_csv(bronze / "airport.csv")

    assert len(result) == 2
    assert result["airport_code"].tolist() == ["DEL", "BOM"]


def test_validate_airports_strips_text_spaces(tmp_path, monkeypatch):
    raw = tmp_path / "raw"
    bronze = tmp_path / "bronze"
    raw.mkdir()
    bronze.mkdir()

    df = pd.DataFrame({
        "airport_code": ["DEL"],
        "airport_name": [" Delhi Airport "],
        "city": [" Delhi "],
        "country": [" India "]
    })

    df.to_csv(raw / "airport.csv", index=False)

    monkeypatch.setattr(airport_validator, "RAW_FOLDER", raw)
    monkeypatch.setattr(airport_validator, "BRONZE_FOLDER", bronze)

    airport_validator.validate_airports()

    result = pd.read_csv(bronze / "airport.csv")

    assert result.loc[0, "airport_name"] == "Delhi Airport"
    assert result.loc[0, "city"] == "Delhi"
    assert result.loc[0, "country"] == "India"
