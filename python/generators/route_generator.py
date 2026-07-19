"""
Route Generator
SkyFlow Enterprise Airline Data Platform
"""

import random
import pandas as pd

from python.config.config import RAW_FOLDER


ROUTE_TYPES = [
    "Domestic",
    "International"
]


def generate_routes():

    airport_df = pd.read_csv(RAW_FOLDER / "airport.csv")

    airports = airport_df.to_dict("records")

    routes = []

    used_routes = set()

    route_id = 1

    while len(routes) < 100:

        source = random.choice(airports)
        destination = random.choice(airports)

        if source["airport_code"] == destination["airport_code"]:
            continue

        route_key = (
            source["airport_code"],
            destination["airport_code"]
        )

        if route_key in used_routes:
            continue

        used_routes.add(route_key)

        if source["country"] == destination["country"]:

            route_type = "Domestic"

            distance = random.randint(300, 2500)

        else:

            route_type = "International"

            distance = random.randint(2501, 12000)

        duration_minutes = random.randint(
            int(distance / 10),
            int(distance / 7)
        )

        fuel_estimate_liters = round(distance * 4.8, 2)

        routes.append({

            "route_id": f"RT{route_id:04}",

            "source_airport": source["airport_code"],

            "destination_airport": destination["airport_code"],

            "route_type": route_type,

            "distance_km": distance,

            "duration_minutes": duration_minutes,

            "fuel_estimate_liters": fuel_estimate_liters

        })

        route_id += 1

    df = pd.DataFrame(routes)

    output_file = RAW_FOLDER / "route.csv"

    df.to_csv(output_file, index=False)

    print(f"Route data generated successfully: {output_file}")


if __name__ == "__main__":
    generate_routes()