"""
SkyFlow - Passenger Gold Dimension
Silver Layer -> Gold Layer
"""

# ============================================================
# WINDOWS HADOOP SETUP
# IMPORTANT: PySpark import hone se pehle hona chahiye
# ============================================================

import os
from pathlib import Path

os.environ["HADOOP_HOME"] = r"C:\hadoop"

if r"C:\hadoop\bin" not in os.environ.get("PATH", ""):
    os.environ["PATH"] = (
        r"C:\hadoop\bin;"
        + os.environ.get("PATH", "")
    )


# ============================================================
# PYSPARK IMPORTS
# ============================================================

from pyspark.sql.functions import (
    col,
    trim,
    upper,
    concat_ws
)

from python.spark.spark_session import get_spark
from python.config.config import SILVER_FOLDER, GOLD_FOLDER


# ============================================================
# CREATE SPARK SESSION
# ============================================================

spark = get_spark()

spark.sparkContext.setLogLevel("WARN")


# ============================================================
# PATHS
# ============================================================

SILVER_PASSENGER_FOLDER = (
    Path(SILVER_FOLDER) / "passenger"
)

GOLD_PASSENGER_FOLDER = (
    Path(GOLD_FOLDER) / "dim_passenger"
)


# ============================================================
# FIND ACTUAL SILVER CSV FILE
# ============================================================

silver_files = list(
    SILVER_PASSENGER_FOLDER.glob("part-*.csv")
)

if not silver_files:
    raise FileNotFoundError(
        f"Silver passenger CSV nahi mila: "
        f"{SILVER_PASSENGER_FOLDER}"
    )

silver_passenger_file = silver_files[0]


print("\n========== PASSENGER GOLD PIPELINE ==========")

print("\nSilver Passenger File:")
print(silver_passenger_file)


# ============================================================
# READ SILVER DATA
# ============================================================

passenger_df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(str(silver_passenger_file))
)


print("\n========== SILVER PASSENGER DATA ==========")

passenger_df.show(
    10,
    truncate=False
)


# ============================================================
# GOLD TRANSFORMATION
# ============================================================

passenger_gold = (
    passenger_df

    # Passenger ID
    .withColumn(
        "passenger_id",
        upper(trim(col("passenger_id")))
    )

    # First Name
    .withColumn(
        "first_name",
        trim(col("first_name"))
    )

    # Last Name
    .withColumn(
        "last_name",
        trim(col("last_name"))
    )

    # Full Name
    .withColumn(
        "full_name",
        concat_ws(
            " ",
            col("first_name"),
            col("last_name")
        )
    )

    # Gender
    .withColumn(
        "gender",
        upper(trim(col("gender")))
    )

    # Email
    .withColumn(
        "email",
        trim(col("email"))
    )

    # Phone
    .withColumn(
        "phone",
        trim(
            col("phone").cast("string")
        )
    )

    # Passport
    .withColumn(
        "passport_number",
        upper(
            trim(col("passport_number"))
        )
    )

    # Nationality
    .withColumn(
        "nationality",
        upper(
            trim(col("nationality"))
        )
    )

    # Remove duplicate passengers
    .dropDuplicates(
        ["passenger_id"]
    )

    # Remove null passenger IDs
    .filter(
        col("passenger_id").isNotNull()
    )

    # Final Gold columns
    .select(
        "passenger_id",
        "first_name",
        "last_name",
        "full_name",
        "gender",
        "date_of_birth",
        "email",
        "phone",
        "passport_number",
        "nationality"
    )

    # Sort
    .orderBy(
        "passenger_id"
    )
)


# ============================================================
# SHOW GOLD DATA
# ============================================================

print(
    "\n========== GOLD PASSENGER DIMENSION =========="
)

passenger_gold.show(
    20,
    truncate=False
)


# ============================================================
# COUNT
# ============================================================

total_passengers = passenger_gold.count()

print(
    f"\nTotal Passengers : {total_passengers}"
)


# ============================================================
# WRITE TO GOLD LAYER
# ============================================================

print(
    "\n========== WRITING GOLD PASSENGER DATA =========="
)

(
    passenger_gold
    .coalesce(1)
    .write
    .mode("overwrite")
    .option("header", True)
    .csv(
        str(GOLD_PASSENGER_FOLDER)
    )
)


# ============================================================
# SUCCESS
# ============================================================

print(
    "\nPassenger Gold Dimension "
    "successfully written to Gold Layer."
)

print(
    f"Gold Path : {GOLD_PASSENGER_FOLDER}"
)


# ============================================================
# STOP SPARK
# ============================================================

spark.stop()


print(
    "\n========== PASSENGER GOLD COMPLETED =========="
)