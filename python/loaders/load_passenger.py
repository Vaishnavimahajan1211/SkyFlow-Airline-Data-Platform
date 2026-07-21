"""
Load Passenger CSV into MySQL
"""

import pandas as pd
import mysql.connector

from python.config.config import RAW_FOLDER, MYSQL_CONFIG


def load_passenger():

    conn = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = conn.cursor()

    df = pd.read_csv(RAW_FOLDER / "passenger.csv")

    cursor.execute("DELETE FROM passenger")

    insert_query = """
    INSERT INTO passenger
    (
        passenger_id,
        first_name,
        last_name,
        gender,
        date_of_birth,
        email,
        phone,
        passport_number,
        nationality
    )
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

    for _, row in df.iterrows():

        cursor.execute(
            insert_query,
            (
                row["passenger_id"],
                row["first_name"],
                row["last_name"],
                row["gender"],
                row["date_of_birth"],
                row["email"],
                row["phone"],
                row["passport_number"],
                row["nationality"]
            )
        )

    conn.commit()

    print(f"{len(df)} passenger records inserted successfully.")

    cursor.close()
    conn.close()


if __name__ == "__main__":
    load_passenger()