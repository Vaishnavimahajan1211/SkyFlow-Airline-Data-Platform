"""
SkyFlow - Airport Gold Dimension
"""

import os
from pathlib import Path

# Hadoop Windows configuration
os.environ["HADOOP_HOME"] = r"C:\hadoop"
os.environ["PATH"] = (
    r"C:\hadoop\bin;"
    + os.environ.get("PATH", "")
)

from pyspark.sql.functions import upper, trim, col

from python.spark.spark_session import get_spark
from python.config.config import SILVER_FOLDER, GOLD_FOLDER


print("\n========== AIRPORT GOLD PIPELINE ==========")

# --------------------------------------------------
# Spark Session
# --------------------------------------------------

spark = get_spark()


# --------------------------------------------------
# Paths
# --------------------------------------------------

SILVER_AIRPORT_FOLDER = SILVER_FOLDER / "airport"
GOLD_AIRPORT_FOLDER = GOLD_FOLDER / "dim_airport"


# --------------------------------------------------
# Find Silver Airport CSV
# --------------------------------------------------

airport_files = list(
    SILVER_AIRPORT_FOLDER.glob("part-*.csv")
)

if not airport_files:
    raise FileNotFoundError(
        f"No Silver Airport CSV found in: {SILVER_AIRPORT_FOLDER}"
    )

silver_airport_file = airport_files[0]

print("\nSilver Airport File:")
print(silver_airport_file)


# --------------------------------------------------
# Read Silver Layer
# --------------------------------------------------

df = spark.read.csv(
    str(silver_airport_file),
    header=True,
    inferSchema=True
)

print("\n========== SILVER AIRPORT DATA ==========")

df.show(
    20,
    truncate=False
)


# --------------------------------------------------
# Airport Gold Transformation
# --------------------------------------------------

df_gold = (
    df

    # Remove duplicate airport codes
    .dropDuplicates(["airport_code"])

    # Remove null airport codes
    .dropna(subset=["airport_code"])

    # Trim text columns
    .withColumn(
        "airport_code",
        trim(col("airport_code"))
    )

    .withColumn(
        "airport_name",
        trim(col("airport_name"))
    )

    .withColumn(
        "city",
        trim(col("city"))
    )

    .withColumn(
        "country",
        trim(col("country"))
    )

    .withColumn(
        "timezone",
        trim(col("timezone"))
    )

    # Standardize country
    .withColumn(
        "country",
        upper(col("country"))
    )

    # Standardize airport code
    .withColumn(
        "airport_code",
        upper(col("airport_code"))
    )

    # Select final Gold columns
    .select(
        "airport_code",
        "airport_name",
        "city",
        "country",
        "timezone"
    )

    # Sort by airport code
    .orderBy("airport_code")
)


# --------------------------------------------------
# Display Gold Data
# --------------------------------------------------

print("\n========== GOLD AIRPORT DIMENSION ==========")

df_gold.show(
    20,
    truncate=False
)


# --------------------------------------------------
# Count
# --------------------------------------------------

total_airports = df_gold.count()

print("\nTotal Airports :", total_airports)


# --------------------------------------------------
# Create Gold Folder
# --------------------------------------------------

GOLD_AIRPORT_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)


# --------------------------------------------------
# Write Gold Layer
# --------------------------------------------------

print("\n========== WRITING GOLD AIRPORT DATA ==========")

(
    df_gold
    .coalesce(1)
    .write
    .mode("overwrite")
    .option("header", True)
    .csv(str(GOLD_AIRPORT_FOLDER))
)


print("\nAirport Gold Dimension successfully written to Gold Layer.")

print("Gold Path :", GOLD_AIRPORT_FOLDER)


# --------------------------------------------------
# Finish
# --------------------------------------------------

print("\n========== AIRPORT GOLD COMPLETED ==========")

spark.stop()