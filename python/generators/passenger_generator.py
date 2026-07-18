"""
Passenger Generator
SkyFlow Enterprise Airline Data Platform
"""

import random
import pandas as pd
from faker import Faker

from python.config.config import RAW_FOLDER

fake = Faker("en_IN")

GENDERS = ["Male", "Female"]

NATIONALITIES = [
    "Indian",
    "American",
    "British",
    "Canadian",
    "Australian",
    "German",
    "French",
    "Japanese",
    "Singaporean",
    "UAE"
]


def generate_passengers():

    passengers = []

    for i in range(1, 1001):

        gender = random.choice(GENDERS)

        passengers.append({

            "passenger_id": f"PS{i:05}",

            "first_name": fake.first_name_male() if gender == "Male" else fake.first_name_female(),

            "last_name": fake.last_name(),

            "gender": gender,

            "date_of_birth": fake.date_of_birth(minimum_age=18, maximum_age=70),

            "email": fake.unique.email(),

            "phone": fake.phone_number(),

            "passport_number": fake.unique.bothify(text='??#######'),

            "nationality": random.choice(NATIONALITIES)

        })

    df = pd.DataFrame(passengers)

    output_file = RAW_FOLDER / "passenger.csv"

    df.to_csv(output_file, index=False)

    print(f"Passenger data generated successfully: {output_file}")


if __name__ == "__main__":
    generate_passengers()