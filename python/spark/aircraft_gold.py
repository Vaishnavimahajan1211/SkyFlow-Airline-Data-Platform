"""
SkyFlow - Aircraft Gold Dimension
"""

import os

os.environ["HADOOP_HOME"] = r"C:\hadoop"
os.environ["PATH"] = (
    r"C:\hadoop\bin;"
    + os.environ.get("PATH", "")
)

from pyspark.sql.functions import upper, trim, col

from python.spark.spark_session import get_spark
from python.config.config import SILVER_FOLDER, GOLD_FOLDER

print("\n========== AIRCRAFT GOLD PIPELINE ==========")

spark = get_spark()

# Silver Aircraft folder
SILVER_AIRCRAFT_FOLDER = SILVER_FOLDER / "aircraft"

# Gold Aircraft folder
GOLD_AIRCRAFT_FOLDER = GOLD_FOLDER / "dim_aircraft"

# Find Silver CSV
aircraft_files = list(
    SILVER_AIRCRAFT_FOLDER.glob("part-*.csv")
)

if not aircraft_files:
    raise FileNotFoundError(
        f"No Silver Aircraft CSV found in: {SILVER_AIRCRAFT_FOLDER}"
    )

silver_aircraft_file = aircraft_files[0]

print("\nSilver Aircraft File:")
print(silver_aircraft_file)

# Read Silver data
df = spark.read.csv(
    str(silver_aircraft_file),
    header=True,
    inferSchema=True
)

print("\n========== SILVER AIRCRAFT DATA ==========")
df.show(20, truncate=False)

# Transform data for Gold
df_gold = (
    df
    .dropDuplicates(["aircraft_id"])
    .dropna(subset=["aircraft_id"])
    .withColumn("aircraft_id", trim(col("aircraft_id")))
    .withColumn("aircraft_code", trim(col("aircraft_code")))
    .withColumn("manufacturer", trim(col("manufacturer")))
    .withColumn("model", trim(col("model")))
    .withColumn("status", trim(col("status")))
    .withColumn("aircraft_code", upper(col("aircraft_code")))
    .withColumn("manufacturer", upper(col("manufacturer")))
    .withColumn("status", upper(col("status")))
    .select(
        "aircraft_id",
        "aircraft_code",
        "manufacturer",
        "model",
        "capacity",
        "manufacturing_year",
        "status"
    )
    .orderBy("aircraft_code")
)

print("\n========== GOLD AIRCRAFT DIMENSION ==========")
df_gold.show(20, truncate=False)

# Count records
total_aircraft = df_gold.count()

print("\nTotal Aircraft :", total_aircraft)

# Create Gold folder
GOLD_AIRCRAFT_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)

print("\n========== WRITING GOLD AIRCRAFT DATA ==========")

(
    df_gold
    .coalesce(1)
    .write
    .mode("overwrite")
    .option("header", True)
    .csv(str(GOLD_AIRCRAFT_FOLDER))
)

print("\nAircraft Gold Dimension successfully written to Gold Layer.")
print("Gold Path :", GOLD_AIRCRAFT_FOLDER)

print("\n========== AIRCRAFT GOLD COMPLETED ==========")

spark.stop()