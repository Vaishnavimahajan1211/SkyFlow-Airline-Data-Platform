"""
Load Route CSV into MySQL
"""

import pandas as pd
import mysql.connector

from python.config.config import RAW_FOLDER, MYSQL_CONFIG


def load_route():

    conn = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = conn.cursor()

    df = pd.read_csv(RAW_FOLDER / "route.csv")

    cursor.execute("DELETE FROM route")

    insert_query = """
    INSERT INTO route
    (
        route_id,
        source_airport,
        destination_airport,
        route_type,
        distance_km,
        duration_minutes,
        fuel_estimate_liters
    )
    VALUES (%s,%s,%s,%s,%s,%s,%s)
    """

    for _, row in df.iterrows():

        cursor.execute(
            insert_query,
            (
                row["route_id"],
                row["source_airport"],
                row["destination_airport"],
                row["route_type"],
                row["distance_km"],
                row["duration_minutes"],
                row["fuel_estimate_liters"]
            )
        )

    conn.commit()

    print(f"{len(df)} route records inserted successfully.")

    cursor.close()
    conn.close()


if __name__ == "__main__":
    load_route()