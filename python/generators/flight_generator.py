"""
Flight Generator
SkyFlow Enterprise Airline Data Platform
"""

import random
import pandas as pd
from datetime import datetime, timedelta

from python.config.config import RAW_FOLDER


FLIGHT_STATUS = [
    "Scheduled",
    "Boarding",
    "Departed",
    "Delayed",
    "Cancelled",
    "Landed"
]

TERMINALS = [
    "T1",
    "T2",
    "T3"
]

GATES = [
    "A01","A02","A03","A04","A05",
    "B01","B02","B03","B04","B05",
    "C01","C02","C03","C04","C05"
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

        status = random.choices(
            FLIGHT_STATUS,
            weights=[45, 10, 15, 15, 5, 10],
            k=1
        )[0]

        delay_minutes = 0

        if status == "Delayed":
            delay_minutes = random.choice([
                15,
                30,
                45,
                60,
                90,
                120
            ])

        departure = departure + timedelta(minutes=delay_minutes)

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

            "flight_status": status,

            "terminal": random.choice(TERMINALS),

            "gate_number": random.choice(GATES),

            "delay_minutes": delay_minutes

        })

    df = pd.DataFrame(flights)

    output_file = RAW_FOLDER / "flight.csv"

    df.to_csv(output_file, index=False)

    print(f"Flight data generated successfully: {output_file}")


if __name__ == "__main__":
    generate_flights()