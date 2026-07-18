"""
Flight Validator
"""

import pandas as pd

from python.config.config import RAW_FOLDER, BRONZE_FOLDER


def validate_flights():

    df = pd.read_csv(RAW_FOLDER / "flight.csv")

    df = df.drop_duplicates(subset=["flight_id"])

    df = df.dropna(subset=["flight_id"])

    df["departure_datetime"] = pd.to_datetime(df["departure_datetime"])

    df["arrival_datetime"] = pd.to_datetime(df["arrival_datetime"])

    df = df[df["arrival_datetime"] > df["departure_datetime"]]

    df["status"] = df["status"].str.strip()

    output = BRONZE_FOLDER / "flight.csv"

    df.to_csv(output, index=False)

    print(f"Flight validation completed: {output}")


if __name__ == "__main__":
    validate_flights()