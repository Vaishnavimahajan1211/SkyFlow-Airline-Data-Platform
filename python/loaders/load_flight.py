"""
Load Flight CSV into MySQL
"""

import pandas as pd
import mysql.connector

from python.config.config import RAW_FOLDER, MYSQL_CONFIG


def load_flight():

    conn = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = conn.cursor()

    df = pd.read_csv(RAW_FOLDER / "flight.csv")

    cursor.execute("DELETE FROM flight")

    insert_query = """
    INSERT INTO flight
    (
        flight_id,
        flight_number,
        route_id,
        aircraft_id,
        departure_datetime,
        arrival_datetime,
        flight_status,
        terminal,
        gate_number,
        delay_minutes
    )
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

    for _, row in df.iterrows():

        cursor.execute(
            insert_query,
            (
                row["flight_id"],
                row["flight_number"],
                row["route_id"],
                row["aircraft_id"],
                row["departure_datetime"],
                row["arrival_datetime"],
                row["flight_status"],
                row["terminal"],
                row["gate_number"],
                row["delay_minutes"]
            )
        )

    conn.commit()

    print(f"{len(df)} flight records inserted successfully.")

    cursor.close()
    conn.close()


if __name__ == "__main__":
    load_flight()