import pandas as pd

from python.cleaners import cleaner


def test_clean_dataset_removes_duplicate_rows(tmp_path, monkeypatch):
    bronze = tmp_path / "bronze"
    silver = tmp_path / "silver"
    bronze.mkdir()
    silver.mkdir()

    input_file = bronze / "sample.csv"
    pd.DataFrame({
        "id": [1, 1, 2],
        "name": ["Alice", "Alice", "Bob"]
    }).to_csv(input_file, index=False)

    monkeypatch.setattr(cleaner, "BRONZE_FOLDER", bronze)
    monkeypatch.setattr(cleaner, "SILVER_FOLDER", silver)

    cleaner.clean_dataset("sample.csv")

    result = pd.read_csv(silver / "sample.csv")

    assert len(result) == 2
    assert result["id"].tolist() == [1, 2]


def test_clean_dataset_strips_text_spaces(tmp_path, monkeypatch):
    bronze = tmp_path / "bronze"
    silver = tmp_path / "silver"
    bronze.mkdir()
    silver.mkdir()

    pd.DataFrame({
        "name": ["  Alice  ", " Bob "]
    }).to_csv(bronze / "sample.csv", index=False)

    monkeypatch.setattr(cleaner, "BRONZE_FOLDER", bronze)
    monkeypatch.setattr(cleaner, "SILVER_FOLDER", silver)

    cleaner.clean_dataset("sample.csv")

    result = pd.read_csv(silver / "sample.csv")

    assert result["name"].tolist() == ["Alice", "Bob"]


def test_clean_dataset_converts_empty_strings_to_null(tmp_path, monkeypatch):
    bronze = tmp_path / "bronze"
    silver = tmp_path / "silver"
    bronze.mkdir()
    silver.mkdir()

    pd.DataFrame({
        "name": ["Alice", "", "Bob"]
    }).to_csv(bronze / "sample.csv", index=False)

    monkeypatch.setattr(cleaner, "BRONZE_FOLDER", bronze)
    monkeypatch.setattr(cleaner, "SILVER_FOLDER", silver)

    cleaner.clean_dataset("sample.csv")

    result = pd.read_csv(silver / "sample.csv")

    assert pd.isna(result.loc[1, "name"])
