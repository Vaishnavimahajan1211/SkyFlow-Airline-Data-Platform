"""
Generic Cleaner
SkyFlow Enterprise Airline Data Platform
"""

import pandas as pd

from python.config.config import BRONZE_FOLDER, SILVER_FOLDER


def clean_dataset(file_name):

    input_file = BRONZE_FOLDER / file_name
    output_file = SILVER_FOLDER / file_name

    df = pd.read_csv(input_file)

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Remove leading/trailing spaces from text columns
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].str.strip()

    # Replace empty strings with NULL
    df.replace("", pd.NA, inplace=True)

    df.to_csv(output_file, index=False)

    print(f"{file_name} cleaned successfully.")


if __name__ == "__main__":

    files = [
        "airport.csv",
        "aircraft.csv",
        "route.csv",
        "passenger.csv",
        "flight.csv",
        "booking.csv",
        "payment.csv"
    ]

    for file in files:
        clean_dataset(file)

    print("\nSilver Layer Created Successfully.")