
import pandas as pd

from python.validators import flight_validator


def make_flight_data():
    return pd.DataFrame({
        "flight_id": [1, 1, 2, 3, 4, 5],
        "departure_datetime": [
            "2026-10-12 08:00:00",
            "2026-10-12 08:00:00",
            "2026-10-12 09:00:00",
            "2026-10-12 11:00:00",
            "2026-10-12 12:00:00",
            "2026-10-12 13:00:00"
        ],
        "arrival_datetime": [
            "2026-10-12 10:00:00",
            "2026-10-12 10:00:00",
            "2026-10-12 10:00:00",
            "2026-10-12 12:00:00",
            "2026-10-12 14:00:00",
            "2026-10-12 15:00:00"
        ],
        "flight_status": [
            " Scheduled ",
            " Scheduled ",
            "Landed",
            "Delayed",
            "Scheduled",
            "Cancelled"
        ],
        "terminal": [" T1 ", " T1 ", "T2", "T1", "T3", "T2"],
        "gate_number": [" G1 ", " G1 ", "G2", "G3", "G4", "G5"],
        "delay_minutes": [0, 0, 0, 10, -5, None]
    })


def setup_flight_test(tmp_path, monkeypatch):
    raw = tmp_path / "raw"
    bronze = tmp_path / "bronze"

    raw.mkdir()
    bronze.mkdir()

    make_flight_data().to_csv(raw / "flight.csv", index=False)

    monkeypatch.setattr(flight_validator, "RAW_FOLDER", raw)
    monkeypatch.setattr(flight_validator, "BRONZE_FOLDER", bronze)

    return bronze / "flight.csv"


def test_validate_flights_removes_duplicates_and_invalid_rows(
    tmp_path, monkeypatch
):
    output_file = setup_flight_test(tmp_path, monkeypatch)

    flight_validator.validate_flights()

    result = pd.read_csv(output_file)

    assert result["flight_id"].tolist() == [1, 2, 3, 5]
    assert (result["delay_minutes"] >= 0).all()


def test_validate_flights_cleans_text_and_missing_delay(
    tmp_path, monkeypatch
):
    output_file = setup_flight_test(tmp_path, monkeypatch)

    flight_validator.validate_flights()

    result = pd.read_csv(output_file)

    first_flight = result.loc[
        result["flight_id"] == 1
    ].iloc[0]

    fifth_flight = result.loc[
        result["flight_id"] == 5
    ].iloc[0]

    assert first_flight["flight_status"] == "Scheduled"
    assert first_flight["terminal"] == "T1"
    assert first_flight["gate_number"] == "G1"
    assert fifth_flight["delay_minutes"] == 0
