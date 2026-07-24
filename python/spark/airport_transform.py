"""
Airport Transformation using PySpark
"""

from pyspark.sql.functions import upper, trim, col

from python.spark.spark_session import get_spark
from python.config.config import BRONZE_FOLDER, SILVER_FOLDER

spark = get_spark()

# Read Bronze Layer
df = spark.read.csv(
    str(BRONZE_FOLDER / "airport.csv"),
    header=True,
    inferSchema=True
)

print("\n========== ORIGINAL AIRPORT DATA ==========")
df.show(10, truncate=False)

# Remove duplicate airports
df = df.dropDuplicates(["airport_code"])

# Remove null airport codes
df = df.dropna(subset=["airport_code"])

# Trim text columns
df = (
    df.withColumn("airport_name", trim(col("airport_name")))
      .withColumn("city", trim(col("city")))
      .withColumn("country", trim(col("country")))
)

# Standardize country names
df = df.withColumn(
    "country",
    upper(col("country"))
)

# Select required columns
df = df.select(
    "airport_code",
    "airport_name",
    "city",
    "country",
    "timezone"
)

# Sort records
df = df.orderBy("airport_code")

print("\n========== TRANSFORMED AIRPORT DATA ==========")
df.show(20, truncate=False)

print("\nTotal Airports :", df.count())

# Write to Silver Layer
df.write.mode("overwrite") \
    .option("header", True) \
    .csv(str(SILVER_FOLDER / "airport"))

print("\nAirport data successfully written to Silver Layer.")

spark.stop()
