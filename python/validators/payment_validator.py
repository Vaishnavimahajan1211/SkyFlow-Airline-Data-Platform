
"""
Payment Validator
"""

import pandas as pd

from python.config.config import RAW_FOLDER, BRONZE_FOLDER


def validate_payments():

    df = pd.read_csv(RAW_FOLDER / "payment.csv")

    df = df.drop_duplicates(subset=["payment_id"])

    df = df.dropna(subset=["payment_id"])

    df["payment_date"] = pd.to_datetime(df["payment_date"])

    df = df[df["amount"] > 0]

    df["payment_method"] = df["payment_method"].str.strip()

    df["payment_status"] = df["payment_status"].str.strip()

    output = BRONZE_FOLDER / "payment.csv"

    df.to_csv(output, index=False)

    print(f"Payment validation completed: {output}")


if __name__ == "__main__":
    validate_payments()