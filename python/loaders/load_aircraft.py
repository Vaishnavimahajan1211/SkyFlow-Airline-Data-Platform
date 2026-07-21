"""
Load Aircraft CSV into MySQL
"""

import pandas as pd
import mysql.connector

from python.config.config import RAW_FOLDER, MYSQL_CONFIG


def load_aircraft():

    conn = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = conn.cursor()

    df = pd.read_csv(RAW_FOLDER / "aircraft.csv")

    cursor.execute("DELETE FROM aircraft")

    insert_query = """
    INSERT INTO aircraft
    (
        aircraft_id,
        aircraft_code,
        manufacturer,
        model,
        capacity,
        manufacturing_year,
        status
    )
    VALUES (%s,%s,%s,%s,%s,%s,%s)
    """

    for _, row in df.iterrows():

        cursor.execute(
            insert_query,
            (
                row["aircraft_id"],
                row["aircraft_code"],
                row["manufacturer"],
                row["model"],
                row["capacity"],
                row["manufacturing_year"],
                row["status"]
            )
        )

    conn.commit()

    print(f"{len(df)} aircraft records inserted successfully.")

    cursor.close()
    conn.close()


if __name__ == "__main__":
    load_aircraft()