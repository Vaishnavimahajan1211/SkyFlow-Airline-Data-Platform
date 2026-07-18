"""
Flight Generator
SkyFlow Enterprise Airline Data Platform
"""

import random
import pandas as pd
from datetime import datetime, timedelta

from python.config.config import RAW_FOLDER


STATUS = [
    "Scheduled",
    "Delayed",
    "Cancelled"
]


def generate_flights():

    route_df = pd.read_csv(RAW_FOLDER / "route.csv")
    aircraft_df = pd.read_csv(RAW_FOLDER / "aircraft.csv")

    routes = route_df.to_dict("records")
    aircraft = aircraft_df["aircraft_id"].tolist()

    flights = []

    start_date = datetime(2026, 8, 1, 6, 0)

    for i in range(1, 201):

        route = random.choice(routes)

        departure = start_date + timedelta(
            hours=random.randint(0, 24 * 30),
            minutes=random.randint(0, 59)
        )

        arrival = departure + timedelta(
            minutes=int(route["duration_minutes"])
        )

        flights.append({

            "flight_id": f"FL{i:04}",

            "flight_number": f"SF{1000+i}",

            "route_id": route["route_id"],

            "aircraft_id": random.choice(aircraft),

            "departure_datetime": departure.strftime("%Y-%m-%d %H:%M:%S"),

            "arrival_datetime": arrival.strftime("%Y-%m-%d %H:%M:%S"),

            "status": random.choices(
                STATUS,
                weights=[85, 10, 5],
                k=1
            )[0]

        })

    df = pd.DataFrame(flights)

    output_file = RAW_FOLDER / "flight.csv"

    df.to_csv(output_file, index=False)

    print(f"Flight data generated successfully: {output_file}")


if __name__ == "__main__":
    generate_flights()