
"""
SkyFlow - Route Gold Dimension
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

print("\n========== ROUTE GOLD PIPELINE ==========")

spark = get_spark()

# Silver Route folder
SILVER_ROUTE_FOLDER = SILVER_FOLDER / "route"

# Gold Route folder
GOLD_ROUTE_FOLDER = GOLD_FOLDER / "dim_route"

# Find Silver CSV
route_files = list(
    SILVER_ROUTE_FOLDER.glob("part-*.csv")
)

if not route_files:
    raise FileNotFoundError(
        f"No Silver Route CSV found in: {SILVER_ROUTE_FOLDER}"
    )

silver_route_file = route_files[0]

print("\nSilver Route File:")
print(silver_route_file)

# Read Silver data
df = spark.read.csv(
    str(silver_route_file),
    header=True,
    inferSchema=True
)

print("\n========== SILVER ROUTE DATA ==========")
df.show(20, truncate=False)

# Transform Route data for Gold
df_gold = (
    df
    .dropDuplicates(["route_id"])
    .dropna(subset=["route_id"])
    .withColumn("route_id", trim(col("route_id")))
    .withColumn("origin_airport", trim(col("origin_airport")))
    .withColumn("destination_airport", trim(col("destination_airport")))
    .withColumn("origin_airport", upper(col("origin_airport")))
    .withColumn("destination_airport", upper(col("destination_airport")))
    .select(
        "route_id",
        "origin_airport",
        "destination_airport",
        "distance_km",
        "duration_minutes"
    )
    .orderBy("route_id")
)

print("\n========== GOLD ROUTE DIMENSION ==========")
df_gold.show(20, truncate=False)

# Count records
total_routes = df_gold.count()

print("\nTotal Routes :", total_routes)

# Create Gold folder
GOLD_ROUTE_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)

print("\n========== WRITING GOLD ROUTE DATA ==========")

(
    df_gold
    .coalesce(1)
    .write
    .mode("overwrite")
    .option("header", True)
    .csv(str(GOLD_ROUTE_FOLDER))
)

print("\nRoute Gold Dimension successfully written to Gold Layer.")
print("Gold Path :", GOLD_ROUTE_FOLDER)

print("\n========== ROUTE GOLD COMPLETED ==========")

spark.stop()

