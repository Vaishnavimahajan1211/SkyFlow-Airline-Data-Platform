"""
Load Payment CSV into MySQL
"""

import pandas as pd
import mysql.connector

from python.config.config import RAW_FOLDER, MYSQL_CONFIG


def load_payment():

    conn = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = conn.cursor()

    df = pd.read_csv(RAW_FOLDER / "payment.csv")

    insert_query = """
    INSERT INTO payment
    (
        payment_id,
        booking_id,
        payment_date,
        payment_method,
        amount,
        payment_status
    )
    VALUES (%s,%s,%s,%s,%s,%s)
    """

    for _, row in df.iterrows():

        cursor.execute(
            insert_query,
            (
                row["payment_id"],
                row["booking_id"],
                row["payment_date"],
                row["payment_method"],
                row["amount"],
                row["payment_status"]
            )
        )

    conn.commit()

    print(f"{len(df)} payment records inserted successfully.")

    cursor.close()
    conn.close()


if __name__ == "__main__":
    load_payment()