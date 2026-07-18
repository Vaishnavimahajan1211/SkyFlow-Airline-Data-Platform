"""
Booking Generator
SkyFlow Enterprise Airline Data Platform
"""

import random
import pandas as pd
from datetime import timedelta

from python.config.config import RAW_FOLDER


BOOKING_STATUS = [
    "Confirmed",
    "Cancelled",
    "Pending"
]

SEAT_CLASSES = [
    "Economy",
    "Premium Economy",
    "Business",
    "First"
]


def generate_bookings():

    passenger_df = pd.read_csv(RAW_FOLDER / "passenger.csv")
    flight_df = pd.read_csv(RAW_FOLDER / "flight.csv")

    passengers = passenger_df["passenger_id"].tolist()
    flights = flight_df.to_dict("records")

    bookings = []

    for i in range(1, 5001):

        flight = random.choice(flights)

        departure = pd.to_datetime(flight["departure_datetime"])

        booking_date = departure - timedelta(
            days=random.randint(1, 120)
        )

        bookings.append({

            "booking_id": f"BK{i:05}",

            "passenger_id": random.choice(passengers),

            "flight_id": flight["flight_id"],

            "booking_date": booking_date.strftime("%Y-%m-%d %H:%M:%S"),

            "seat_class": random.choices(
                SEAT_CLASSES,
                weights=[70, 10, 15, 5],
                k=1
            )[0],

            "booking_status": random.choices(
                BOOKING_STATUS,
                weights=[85, 5, 10],
                k=1
            )[0]

        })

    df = pd.DataFrame(bookings)

    output_file = RAW_FOLDER / "booking.csv"

    df.to_csv(output_file, index=False)

    print(f"Booking data generated successfully: {output_file}")


if __name__ == "__main__":
    generate_bookings()