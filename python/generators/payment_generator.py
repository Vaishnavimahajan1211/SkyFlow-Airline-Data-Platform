"""
Payment Generator
SkyFlow Enterprise Airline Data Platform
"""

import random
import pandas as pd
from datetime import timedelta

from python.config.config import RAW_FOLDER


PAYMENT_METHODS = [
    "Credit Card",
    "Debit Card",
    "UPI",
    "Net Banking",
    "Wallet"
]

PAYMENT_STATUS = [
    "Success",
    "Failed",
    "Refunded"
]


def generate_payments():

    booking_df = pd.read_csv(RAW_FOLDER / "booking.csv")

    bookings = booking_df.to_dict("records")

    payments = []

    for i, booking in enumerate(bookings, start=1):

        booking_date = pd.to_datetime(booking["booking_date"])

        payment_date = booking_date + timedelta(
            minutes=random.randint(1, 60)
        )

        amount = random.choice([
            3500, 4200, 5600, 7200, 8900,
            10500, 12500, 14800, 17500, 22000
        ])

        payments.append({

            "payment_id": f"PY{i:05}",

            "booking_id": booking["booking_id"],

            "payment_date": payment_date.strftime("%Y-%m-%d %H:%M:%S"),

            "payment_method": random.choice(PAYMENT_METHODS),

            "amount": amount,

            "payment_status": random.choices(
                PAYMENT_STATUS,
                weights=[90, 5, 5],
                k=1
            )[0]

        })

    df = pd.DataFrame(payments)

    output_file = RAW_FOLDER / "payment.csv"

    df.to_csv(output_file, index=False)

    print(f"Payment data generated successfully: {output_file}")


if __name__ == "__main__":
    generate_payments()