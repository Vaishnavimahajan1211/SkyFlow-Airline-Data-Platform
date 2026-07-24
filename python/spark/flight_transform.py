
"""
Flight Transformation using PySpark
"""

from pyspark.sql.functions import upper, trim, col, to_timestamp

from python.spark.spark_session import get_spark
from python.config.config import BRONZE_FOLDER

spark = get_spark()

# Read Bronze Layer
df = spark.read.csv(
    str(BRONZE_FOLDER / "flight.csv"),
    header=True,
    inferSchema=True
)

print("\n========== ORIGINAL FLIGHT DATA ==========")
df.show(10, truncate=False)

# Remove duplicate flights
df = df.dropDuplicates(["flight_id"])

# Remove null Flight IDs
df = df.dropna(subset=["flight_id"])

# Trim string columns
string_columns = [
    "flight_number",
    "route_id",
    "aircraft_id",
    "flight_status",
    "terminal",
    "gate_number"
]

for column in string_columns:
    df = df.withColumn(column, trim(col(column)))

# Status uppercase
df = df.withColumn(
    "flight_status",
    upper(col("flight_status"))
)

# Convert datetime columns
df = df.withColumn(
    "departure_datetime",
    to_timestamp(col("departure_datetime"))
)

df = df.withColumn(
    "arrival_datetime",
    to_timestamp(col("arrival_datetime"))
)

# Keep only valid flights
df = df.filter(
    col("arrival_datetime") > col("departure_datetime")
)

# Select required columns
df = df.select(
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

# Sort
df = df.orderBy("departure_datetime")

print("\n========== TRANSFORMED FLIGHT DATA ==========")
df.show(20, truncate=False)

print("\nTotal Flights :", df.count())

# (Write to Silver Layer abhi intentionally skip kar rahe hain,
# kyunki Windows + Hadoop issue solve karenge ek hi baar sab scripts ke liye.)

spark.stop()