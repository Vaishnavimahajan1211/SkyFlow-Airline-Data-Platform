"""
Flight Validator
"""

import pandas as pd

from python.config.config import RAW_FOLDER, BRONZE_FOLDER


def validate_flights():

    df = pd.read_csv(RAW_FOLDER / "flight.csv")

    # Remove duplicate Flight IDs
    df = df.drop_duplicates(subset=["flight_id"])

    # Remove rows with missing Flight IDs
    df = df.dropna(subset=["flight_id"])

    # Convert datetime columns
    df["departure_datetime"] = pd.to_datetime(df["departure_datetime"])
    df["arrival_datetime"] = pd.to_datetime(df["arrival_datetime"])

    # Arrival must be after Departure
    df = df[df["arrival_datetime"] > df["departure_datetime"]]

    # Clean Flight Status
    df["flight_status"] = df["flight_status"].astype(str).str.strip()

    # Clean Terminal
    df["terminal"] = df["terminal"].astype(str).str.strip()

    # Clean Gate Number
    df["gate_number"] = df["gate_number"].astype(str).str.strip()

    # Delay should never be negative
    df["delay_minutes"] = df["delay_minutes"].fillna(0)
    df = df[df["delay_minutes"] >= 0]

    output = BRONZE_FOLDER / "flight.csv"

    df.to_csv(output, index=False)

    print(f"Flight validation completed: {output}")


if __name__ == "__main__":
    validate_flights()