"""
SkyFlow - Route Gold Dimension
"""

import os

os.environ["HADOOP_HOME"] = r"C:\hadoop"
os.environ["PATH"] = r"C:\hadoop\bin;" + os.environ.get("PATH", "")

from pyspark.sql.functions import upper, trim, col

from python.spark.spark_session import get_spark
from python.config.config import SILVER_FOLDER, GOLD_FOLDER

print("\n========== ROUTE GOLD PIPELINE ==========")

spark = get_spark()

SILVER_ROUTE_FOLDER = SILVER_FOLDER / "route"
GOLD_ROUTE_FOLDER = GOLD_FOLDER / "dim_route"

print("\nSilver Route Folder:")
print(SILVER_ROUTE_FOLDER)

route_files = list(SILVER_ROUTE_FOLDER.glob("part-*.csv"))

print("\nRoute Files Found:")
print(route_files)

silver_route_file = route_files[0]

print("\nSilver Route File:")
print(silver_route_file)

df = spark.read.csv(
str(silver_route_file),
header=True,
inferSchema=True
)

print("\n========== SILVER ROUTE DATA ==========")

df.show(20, truncate=False)

df_gold = (
df
.dropDuplicates(["route_id"])
.dropna(subset=["route_id"])
.withColumn("route_id", trim(col("route_id")))
.withColumn("source_airport", trim(col("source_airport")))
.withColumn("destination_airport", trim(col("destination_airport")))
.withColumn("route_type", trim(col("route_type")))
.withColumn("source_airport", upper(col("source_airport")))
.withColumn("destination_airport", upper(col("destination_airport")))
.withColumn("route_type", upper(col("route_type")))
.select(
"route_id",
"source_airport",
"destination_airport",
"route_type",
"distance_km",
"duration_minutes",
"fuel_estimate_liters"
)
.orderBy("route_id")
)

print("\n========== GOLD ROUTE DIMENSION ==========")

df_gold.show(20, truncate=False)

total_routes = df_gold.count()

print("\nTotal Routes :", total_routes)

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
