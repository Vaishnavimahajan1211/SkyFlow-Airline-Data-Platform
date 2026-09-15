"""
Route Transformation using PySpark
Bronze -> Silver
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, trim, upper

from python.config.config import BRONZE_FOLDER, SILVER_FOLDER


# =========================
# SPARK SESSION
# =========================

spark = (
    SparkSession.builder
    .appName("Route Silver Transformation")
    .master("local[*]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")


# =========================
# READ BRONZE DATA
# =========================

route_df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(str(BRONZE_FOLDER / "route.csv"))
)

print("\n========== ORIGINAL ROUTE DATA ==========")
route_df.show(10, truncate=False)


# =========================
# TRANSFORMATION
# =========================

route_silver = (
    route_df

    # Clean IDs and airport codes
    .withColumn("route_id", upper(trim(col("route_id"))))
    .withColumn("source_airport", upper(trim(col("source_airport"))))
    .withColumn("destination_airport", upper(trim(col("destination_airport"))))

    # Clean route type
    .withColumn("route_type", upper(trim(col("route_type"))))

    # Remove duplicate routes
    .dropDuplicates(["route_id"])

    # Remove null route IDs
    .filter(col("route_id").isNotNull())

    # Keep valid distances
    .filter(col("distance_km") > 0)

    # Select required columns
    .select(
        "route_id",
        "source_airport",
        "destination_airport",
        "route_type",
        "distance_km",
        "duration_minutes",
        "fuel_estimate_liters"
    )

    # Sort by route ID
    .orderBy("route_id")
)


# =========================
# SHOW TRANSFORMED DATA
# =========================

print("\n========== TRANSFORMED ROUTE DATA ==========")
route_silver.show(20, truncate=False)

print(f"\nTotal Routes : {route_silver.count()}")


# =========================
# WRITE TO SILVER
# =========================

(
    route_silver
    .write
    .mode("overwrite")
    .option("header", True)
    .csv(str(SILVER_FOLDER / "route"))
)

print("\nRoute data successfully written to Silver Layer.")


# =========================
# STOP SPARK
# =========================

spark.stop()