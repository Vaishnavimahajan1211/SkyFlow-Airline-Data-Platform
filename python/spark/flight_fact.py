import os
from pathlib import Path

# ==============================
# HADOOP CONFIGURATION
# ==============================

os.environ["HADOOP_HOME"] = r"C:\hadoop"
os.environ["PATH"] = r"C:\hadoop\bin;" + os.environ.get("PATH", "")

# ==============================
# PYSPARK
# ==============================

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    trim,
    upper,
    to_timestamp,
    round as spark_round
)

# ==============================
# PROJECT PATH
# ==============================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

SILVER_FLIGHT_FOLDER = PROJECT_ROOT / "data" / "silver" / "flight"
GOLD_FLIGHT_FOLDER = PROJECT_ROOT / "data" / "gold" / "fact_flight"

# ==============================
# SPARK SESSION
# ==============================

spark = (
    SparkSession.builder
    .appName("SkyFlow_Flight_Fact")
    .master("local[*]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

print("\n========== FLIGHT FACT PIPELINE ==========")

print("\nSilver Flight Folder:")
print(SILVER_FLIGHT_FOLDER)

# ==============================
# FIND SILVER FILE
# ==============================

flight_files = list(SILVER_FLIGHT_FOLDER.glob("part-*.csv"))

print("\nFlight Files Found:")
print(flight_files)

if not flight_files:
    raise FileNotFoundError(
        "No Silver Flight CSV file found."
    )

silver_file = flight_files[0]

print("\nSilver Flight File:")
print(silver_file)

# ==============================
# READ SILVER FLIGHT
# ==============================

df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(str(silver_file))
)

print("\n========== SILVER FLIGHT DATA ==========")

df.show(5, truncate=False)

print("\nSilver Flight Schema:")
df.printSchema()

# ==============================
# TRANSFORMATION
# ==============================

df_gold = (
    df
    .dropDuplicates(["flight_id"])
    .dropna(subset=["flight_id"])

    # Clean IDs
    .withColumn("flight_id", trim(col("flight_id")))
    .withColumn("flight_number", trim(col("flight_number")))
    .withColumn("route_id", trim(col("route_id")))
    .withColumn("aircraft_id", trim(col("aircraft_id")))

    # Standardize categorical columns
    .withColumn("flight_status", upper(trim(col("flight_status"))))
    .withColumn("terminal", upper(trim(col("terminal"))))
    .withColumn("gate_number", upper(trim(col("gate_number"))))

    # Convert datetime columns
    .withColumn(
        "departure_datetime",
        to_timestamp(col("departure_datetime"))
    )
    .withColumn(
        "arrival_datetime",
        to_timestamp(col("arrival_datetime"))
    )

    # Standardize delay
    .withColumn(
        "delay_minutes",
        spark_round(col("delay_minutes"), 0)
    )

    # Select final Gold columns
    .select(
        "flight_id",
        "flight_number",
        "route_id",
        "aircraft_id",
        "departure_datetime",
        "arrival_datetime",
        "flight_status",
        "terminal",
        "gate_number",
        "delay_minutes"
    )

    .orderBy("flight_id")
)

# ==============================
# VALIDATION
# ==============================

print("\n========== GOLD FLIGHT DATA ==========")

df_gold.show(10, truncate=False)

total_flights = df_gold.count()

print("\nTotal Flights :", total_flights)

# ==============================
# OPERATIONAL METRICS
# ==============================

completed_flights = (
    df_gold
    .filter(
        col("flight_status").isin("LANDED", "DEPARTED")
    )
    .count()
)

delayed_flights = (
    df_gold
    .filter(col("delay_minutes") > 0)
    .count()
)

cancelled_flights = (
    df_gold
    .filter(col("flight_status") == "CANCELLED")
    .count()
)

print("\nCompleted Flights :", completed_flights)
print("Delayed Flights   :", delayed_flights)
print("Cancelled Flights :", cancelled_flights)

# ==============================
# WRITE GOLD
# ==============================

print("\n========== WRITING GOLD FLIGHT FACT ==========")

(
    df_gold
    .coalesce(1)
    .write
    .mode("overwrite")
    .option("header", True)
    .csv(str(GOLD_FLIGHT_FOLDER))
)

print("\nFlight Fact Table successfully written to Gold Layer.")
print("Gold Path :", GOLD_FLIGHT_FOLDER)

print("\n========== FLIGHT FACT COMPLETED ==========\n")

# ==============================
# STOP SPARK
# ==============================

spark.stop()