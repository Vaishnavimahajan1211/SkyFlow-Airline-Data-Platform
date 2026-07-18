"""
Route Validator
"""

import pandas as pd

from python.config.config import RAW_FOLDER, BRONZE_FOLDER


def validate_routes():

    df = pd.read_csv(RAW_FOLDER / "route.csv")

    # Remove duplicate routes
    df = df.drop_duplicates(subset=["route_id"])

    # Remove null IDs
    df = df.dropna(subset=["route_id"])

    # Source and Destination cannot be same
    df = df[df["source_airport"] != df["destination_airport"]]

    # Distance and duration must be positive
    df = df[df["distance_km"] > 0]
    df = df[df["duration_minutes"] > 0]

    # Remove extra spaces
    df["source_airport"] = df["source_airport"].str.strip()
    df["destination_airport"] = df["destination_airport"].str.strip()

    output = BRONZE_FOLDER / "route.csv"

    df.to_csv(output, index=False)

    print(f"Route validation completed: {output}")


if __name__ == "__main__":
    validate_routes()