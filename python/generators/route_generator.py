"""
Route Generator
SkyFlow Enterprise Airline Data Platform
"""

import random
import pandas as pd

from python.config.config import RAW_FOLDER


def generate_routes():

    airport_file = RAW_FOLDER / "airport.csv"

    airport_df = pd.read_csv(airport_file)

    airport_codes = airport_df["airport_code"].tolist()

    routes = []

    used_routes = set()

    route_id = 1

    while len(routes) < 100:

        source = random.choice(airport_codes)
        destination = random.choice(airport_codes)

        if source == destination:
            continue

        if (source, destination) in used_routes:
            continue

        used_routes.add((source, destination))

        distance = random.randint(300, 12000)

        duration = int(distance / 8)

        routes.append({

            "route_id": f"RT{route_id:04}",
            "source_airport": source,
            "destination_airport": destination,
            "distance_km": distance,
            "duration_minutes": duration

        })

        route_id += 1

    df = pd.DataFrame(routes)

    output_file = RAW_FOLDER / "route.csv"

    df.to_csv(output_file, index=False)

    print(f"Route data generated successfully: {output_file}")


if __name__ == "__main__":
    generate_routes()