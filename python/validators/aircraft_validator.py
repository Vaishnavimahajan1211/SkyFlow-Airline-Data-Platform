"""
Aircraft Validator
"""

import pandas as pd

from python.config.config import RAW_FOLDER, BRONZE_FOLDER


def validate_aircraft():

    df = pd.read_csv(RAW_FOLDER / "aircraft.csv")

    # Remove duplicate aircraft
    df = df.drop_duplicates(subset=["aircraft_id"])

    # Remove null IDs
    df = df.dropna(subset=["aircraft_id"])

    # Remove spaces
    df["manufacturer"] = df["manufacturer"].str.strip()
    df["model"] = df["model"].str.strip()
    df["status"] = df["status"].str.strip()

    # Capacity should be positive
    df = df[df["capacity"] > 0]

    output = BRONZE_FOLDER / "aircraft.csv"

    df.to_csv(output, index=False)

    print(f"Aircraft validation completed: {output}")


if __name__ == "__main__":
    validate_aircraft()