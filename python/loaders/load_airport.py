"""
Load Airport CSV into MySQL
"""

import pandas as pd
import mysql.connector

from python.config.config import RAW_FOLDER, MYSQL_CONFIG


def load_airport():

    conn = mysql.connector.connect(**MYSQL_CONFIG)

    cursor = conn.cursor()

    df = pd.read_csv(RAW_FOLDER / "airport.csv")

    cursor.execute("DELETE FROM airport")

    insert_query = """
    INSERT INTO airport
    (
        airport_code,
        airport_name,
        city,
        country,
        timezone
    )
    VALUES (%s,%s,%s,%s,%s)
    """

    for _, row in df.iterrows():

        cursor.execute(
            insert_query,
            (
                row["airport_code"],
                row["airport_name"],
                row["city"],
                row["country"],
                row["timezone"]
            )
        )

    conn.commit()

    print(f"{len(df)}  airport records inserted successfully.")

    cursor.close()
    conn.close()


if __name__ == "__main__":
    load_airport()