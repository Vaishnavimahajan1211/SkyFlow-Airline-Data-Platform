"""
Aircraft Transformation using PySpark
"""

from pyspark.sql.functions import upper, trim, col

from python.spark.spark_session import get_spark
from python.config.config import BRONZE_FOLDER

spark = get_spark()

# Read Bronze Layer
df = spark.read.csv(
    str(BRONZE_FOLDER / "aircraft.csv"),
    header=True,
    inferSchema=True
)

print("\n========== ORIGINAL AIRCRAFT DATA ==========")
df.show(10, truncate=False)

# Remove duplicate aircraft
df = df.dropDuplicates(["aircraft_id"])

# Remove null IDs
df = df.dropna(subset=["aircraft_id"])

# Trim string columns
df = (
    df.withColumn("aircraft_code", trim(col("aircraft_code")))
      .withColumn("manufacturer", trim(col("manufacturer")))
      .withColumn("model", trim(col("model")))
      .withColumn("status", trim(col("status")))
)

# Standardize text
df = (
    df.withColumn("manufacturer", upper(col("manufacturer")))
      .withColumn("status", upper(col("status")))
)

# Select required columns
df = df.select(
    "aircraft_id",
    "aircraft_code",
    "manufacturer",
    "model",
    "capacity",
    "manufacturing_year",
    "status"
)

# Sort
df = df.orderBy("aircraft_code")

print("\n========== TRANSFORMED AIRCRAFT DATA ==========")
df.show(20, truncate=False)

print("\nTotal Aircraft :", df.count())

spark.stop()