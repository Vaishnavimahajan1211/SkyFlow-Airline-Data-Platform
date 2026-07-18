"""
Airport Validator
"""

import pandas as pd

from python.config.config import RAW_FOLDER, BRONZE_FOLDER


def validate_airports():

    df = pd.read_csv(RAW_FOLDER / "airport.csv")

    # Remove duplicate airports
    df = df.drop_duplicates(subset=["airport_code"])

    # Remove rows with null airport code
    df = df.dropna(subset=["airport_code"])

    # Remove leading/trailing spaces
    df["airport_name"] = df["airport_name"].str.strip()
    df["city"] = df["city"].str.strip()
    df["country"] = df["country"].str.strip()

    output = BRONZE_FOLDER / "airport.csv"

    df.to_csv(output, index=False)

    print(f"Airport validation completed: {output}")


if __name__ == "__main__":
    validate_airports()