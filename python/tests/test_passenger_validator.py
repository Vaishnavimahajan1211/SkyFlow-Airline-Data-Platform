import pandas as pd

from python.validators import passenger_validator


def test_validate_passengers_removes_duplicate_and_null_ids(
    tmp_path, monkeypatch
):
    raw = tmp_path / "raw"
    bronze = tmp_path / "bronze"
    raw.mkdir()
    bronze.mkdir()

    df = pd.DataFrame({
        "passenger_id": [1, 1, None, 2],
        "first_name": ["Alice", "Alice", "Missing", "Bob"],
        "last_name": ["Smith", "Smith", "Person", "Jones"],
        "gender": ["F", "F", "F", "M"],
        "email": ["alice@example.com", "alice@example.com",
                  "missing@example.com", "bob@example.com"],
        "phone": ["111", "111", "222", "333"],
        "passport_number": ["P1", "P1", "P2", "P3"],
        "nationality": ["Indian", "Indian", "Indian", "Indian"]
    })

    df.to_csv(raw / "passenger.csv", index=False)

    monkeypatch.setattr(passenger_validator, "RAW_FOLDER", raw)
    monkeypatch.setattr(passenger_validator, "BRONZE_FOLDER", bronze)

    passenger_validator.validate_passengers()

    result = pd.read_csv(bronze / "passenger.csv")

    assert len(result) == 2
    assert result["passenger_id"].tolist() == [1.0, 2.0]


def test_validate_passengers_strips_text_spaces(tmp_path, monkeypatch):
    raw = tmp_path / "raw"
    bronze = tmp_path / "bronze"
    raw.mkdir()
    bronze.mkdir()

    df = pd.DataFrame({
        "passenger_id": [1],
        "first_name": [" Alice "],
        "last_name": [" Smith "],
        "gender": [" F "],
        "email": [" alice@example.com "],
        "phone": [" 111 "],
        "passport_number": [" P1 "],
        "nationality": [" Indian "]
    })

    df.to_csv(raw / "passenger.csv", index=False)

    monkeypatch.setattr(passenger_validator, "RAW_FOLDER", raw)
    monkeypatch.setattr(passenger_validator, "BRONZE_FOLDER", bronze)

    passenger_validator.validate_passengers()

    result = pd.read_csv(bronze / "passenger.csv")

    assert result.loc[0, "first_name"] == "Alice"
    assert result.loc[0, "email"] == "alice@example.com"
    assert result.loc[0, "nationality"] == "Indian"
