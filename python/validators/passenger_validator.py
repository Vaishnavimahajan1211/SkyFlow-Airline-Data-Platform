"""
Passenger Validator
"""

import pandas as pd

from python.config.config import RAW_FOLDER, BRONZE_FOLDER


def validate_passengers():

    df = pd.read_csv(RAW_FOLDER / "passenger.csv")

    # Remove duplicate passengers
    df = df.drop_duplicates(subset=["passenger_id"])

    # Remove null passenger IDs
    df = df.dropna(subset=["passenger_id"])

    # Remove spaces
    string_columns = [
        "first_name",
        "last_name",
        "gender",
        "email",
        "phone",
        "passport_number",
        "nationality"
    ]

    for col in string_columns:
        df[col] = df[col].astype(str).str.strip()

    # Remove rows with missing important values
    df = df.dropna(subset=[
        "first_name",
        "last_name",
        "email"
    ])

    output = BRONZE_FOLDER / "passenger.csv"

    df.to_csv(output, index=False)

    print(f"Passenger validation completed: {output}")


if __name__ == "__main__":
    validate_passengers()