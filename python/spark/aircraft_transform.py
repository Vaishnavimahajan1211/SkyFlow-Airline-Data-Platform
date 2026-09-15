"""
Aircraft Transformation using PySpark
Bronze -> Silver
"""

from pyspark.sql.functions import upper, trim, col

from python.spark.spark_session import get_spark
from python.config.config import BRONZE_FOLDER, SILVER_FOLDER


# =========================
# CREATE SPARK SESSION
# =========================

spark = get_spark()


# =========================
# READ BRONZE LAYER
# =========================

df = spark.read.csv(
    str(BRONZE_FOLDER / "aircraft.csv"),
    header=True,
    inferSchema=True
)


print("\n========== ORIGINAL AIRCRAFT DATA ==========")

df.show(10, truncate=False)


# =========================
# REMOVE DUPLICATES
# =========================

df = df.dropDuplicates(["aircraft_id"])


# =========================
# REMOVE NULL AIRCRAFT IDs
# =========================

df = df.dropna(subset=["aircraft_id"])


# =========================
# TRIM STRING COLUMNS
# =========================

df = (
    df
    .withColumn("aircraft_id", trim(col("aircraft_id")))
    .withColumn("aircraft_code", trim(col("aircraft_code")))
    .withColumn("manufacturer", trim(col("manufacturer")))
    .withColumn("model", trim(col("model")))
    .withColumn("status", trim(col("status")))
)


# =========================
# STANDARDIZE TEXT
# =========================

df = (
    df
    .withColumn("aircraft_id", upper(col("aircraft_id")))
    .withColumn("aircraft_code", upper(col("aircraft_code")))
    .withColumn("manufacturer", upper(col("manufacturer")))
    .withColumn("status", upper(col("status")))
)


# =========================
# DATA VALIDATION
# =========================

# Capacity should be greater than zero
df = df.filter(col("capacity") > 0)

# Manufacturing year should be valid
df = df.filter(col("manufacturing_year") > 1900)


# =========================
# SELECT REQUIRED COLUMNS
# =========================

df = df.select(
    "aircraft_id",
    "aircraft_code",
    "manufacturer",
    "model",
    "capacity",
    "manufacturing_year",
    "status"
)


# =========================
# SORT DATA
# =========================

df = df.orderBy("aircraft_code")


# =========================
# SHOW TRANSFORMED DATA
# =========================

print("\n========== TRANSFORMED AIRCRAFT DATA ==========")

df.show(20, truncate=False)

print("\nTotal Aircraft :", df.count())


# =========================
# WRITE TO SILVER LAYER
# =========================

(
    df.write
    .mode("overwrite")
    .option("header", True)
    .csv(str(SILVER_FOLDER / "aircraft"))
)


print("\nAircraft data successfully written to Silver Layer.")


# =========================
# STOP SPARK
# =========================

spark.stop()