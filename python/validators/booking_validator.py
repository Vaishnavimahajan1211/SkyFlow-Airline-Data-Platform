"""
Booking Validator
"""

import pandas as pd

from python.config.config import RAW_FOLDER, BRONZE_FOLDER


def validate_bookings():

    df = pd.read_csv(RAW_FOLDER / "booking.csv")

    df = df.drop_duplicates(subset=["booking_id"])

    df = df.dropna(subset=["booking_id"])

    df["booking_date"] = pd.to_datetime(df["booking_date"])

    df["seat_class"] = df["seat_class"].str.strip()

    df["booking_status"] = df["booking_status"].str.strip()

    output = BRONZE_FOLDER / "booking.csv"

    df.to_csv(output, index=False)

    print(f"Booking validation completed: {output}")


if __name__ == "__main__":
    validate_bookings()