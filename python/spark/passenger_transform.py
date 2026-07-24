"""
Passenger Transformation using PySpark
"""

from pyspark.sql.functions import upper, trim, col, to_date

from python.spark.spark_session import get_spark
from python.config.config import BRONZE_FOLDER

spark = get_spark()

# Read Bronze Layer
df = spark.read.csv(
    str(BRONZE_FOLDER / "passenger.csv"),
    header=True,
    inferSchema=True
)

print("\n========== ORIGINAL PASSENGER DATA ==========")
df.show(10, truncate=False)

# Remove duplicate passengers
df = df.dropDuplicates(["passenger_id"])

# Remove null passenger IDs
df = df.dropna(subset=["passenger_id"])

# Trim text columns
df = (
    df.withColumn("first_name", trim(col("first_name")))
      .withColumn("last_name", trim(col("last_name")))
      .withColumn("gender", trim(col("gender")))
      .withColumn("email", trim(col("email")))
      .withColumn("phone", trim(col("phone")))
      .withColumn("passport_number", trim(col("passport_number")))
      .withColumn("nationality", trim(col("nationality")))
)

# Standardize values
df = (
    df.withColumn("gender", upper(col("gender")))
      .withColumn("nationality", upper(col("nationality")))
)

# Convert DOB to Date
df = df.withColumn(
    "date_of_birth",
    to_date(col("date_of_birth"))
)

# Select required columns
df = df.select(
    "passenger_id",
    "first_name",
    "last_name",
    "gender",
    "date_of_birth",
    "email",
    "phone",
    "passport_number",
    "nationality"
)

# Sort records
df = df.orderBy("passenger_id")

print("\n========== TRANSFORMED PASSENGER DATA ==========")
df.show(20, truncate=False)

print("\nTotal Passengers :", df.count())

spark.stop()