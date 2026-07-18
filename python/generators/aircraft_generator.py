"""
Aircraft Generator
SkyFlow Enterprise Airline Data Platform
"""

import random
import pandas as pd

from python.config.config import RAW_FOLDER

MODELS = [

    ("Airbus", "A320", 180),
    ("Airbus", "A321", 220),
    ("Airbus", "A330", 280),
    ("Airbus", "A350", 320),

    ("Boeing", "737-800", 189),
    ("Boeing", "737 MAX 8", 210),
    ("Boeing", "777-300ER", 396),
    ("Boeing", "787-9 Dreamliner", 290)

]

STATUS = [

    "Active",
    "Maintenance",
    "Inactive"

]


def generate_aircraft():

    aircraft_data = []

    for i in range(1, 51):

        manufacturer, model, capacity = random.choice(MODELS)

        aircraft_data.append({

            "aircraft_id": f"AC{i:04}",
            "aircraft_code": f"{model.replace(' ','')}-{i:03}",
            "manufacturer": manufacturer,
            "model": model,
            "capacity": capacity,
            "manufacturing_year": random.randint(2016, 2025),
            "status": random.choice(STATUS)

        })

    df = pd.DataFrame(aircraft_data)

    output_file = RAW_FOLDER / "aircraft.csv"

    df.to_csv(output_file, index=False)

    print(f"Aircraft data generated successfully: {output_file}")


if __name__ == "__main__":
    generate_aircraft()