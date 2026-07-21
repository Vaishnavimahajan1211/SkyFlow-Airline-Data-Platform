"""
Load Booking CSV into MySQL
"""

import pandas as pd
import mysql.connector

from python.config.config import RAW_FOLDER, MYSQL_CONFIG


def load_booking():

    conn = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = conn.cursor()

    df = pd.read_csv(RAW_FOLDER / "booking.csv")

    cursor.execute("DELETE FROM booking")

    insert_query = """
    INSERT INTO booking
    (
        booking_id,
        passenger_id,
        flight_id,
        booking_date,
        seat_class,
        booking_status,
        ticket_price,
        tax,
        discount,
        final_amount,
        payment_status
    )
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

    for _, row in df.iterrows():

        cursor.execute(
            insert_query,
            (
                row["booking_id"],
                row["passenger_id"],
                row["flight_id"],
                row["booking_date"],
                row["seat_class"],
                row["booking_status"],
                row["ticket_price"],
                row["tax"],
                row["discount"],
                row["final_amount"],
                row["payment_status"]
            )
        )

    conn.commit()

    print(f"{len(df)} booking records inserted successfully.")

    cursor.close()
    conn.close()


if __name__ == "__main__":
    load_booking()