"""
Flight Transformation using PySpark
Bronze -> Silver
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, trim, upper, to_timestamp

from python.config.config import BRONZE_FOLDER, SILVER_FOLDER


# =========================
# SPARK SESSION
# =========================

spark = (
    SparkSession.builder
    .appName("Flight Silver Transformation")
    .master("local[*]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")


# =========================
# READ BRONZE DATA
# =========================

flight_df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(str(BRONZE_FOLDER / "flight.csv"))
)


print("\n========== ORIGINAL FLIGHT DATA ==========")
flight_df.show(10, truncate=False)


# =========================
# TRANSFORMATION
# =========================

flight_silver = (
    flight_df

    # Clean IDs
    .withColumn("flight_id", upper(trim(col("flight_id"))))
    .withColumn("flight_number", upper(trim(col("flight_number"))))
    .withColumn("route_id", upper(trim(col("route_id"))))
    .withColumn("aircraft_id", upper(trim(col("aircraft_id"))))

    # Convert datetime strings to timestamp
    .withColumn(
        "departure_datetime",
        to_timestamp(col("departure_datetime"))
    )
    .withColumn(
        "arrival_datetime",
        to_timestamp(col("arrival_datetime"))
    )

    # Clean status and terminal/gate
    .withColumn(
        "flight_status",
        upper(trim(col("flight_status")))
    )
    .withColumn(
        "terminal",
        upper(trim(col("terminal")))
    )
    .withColumn(
        "gate_number",
        upper(trim(col("gate_number")))
    )

    # Clean delay
    .withColumn(
        "delay_minutes",
        col("delay_minutes").cast("integer")
    )

    # Remove duplicate flights
    .dropDuplicates(["flight_id"])

    # Remove records without flight_id
    .filter(col("flight_id").isNotNull())

    # Keep required columns
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

    # Sort by flight_id
    .orderBy("flight_id")
)


# =========================
# SHOW TRANSFORMED DATA
# =========================

print("\n========== TRANSFORMED FLIGHT DATA ==========")

flight_silver.show(20, truncate=False)

print(f"\nTotal Flights : {flight_silver.count()}")


# =========================
# WRITE TO SILVER
# =========================

(
    flight_silver
    .write
    .mode("overwrite")
    .option("header", True)
    .csv(str(SILVER_FOLDER / "flight"))
)


print("\nFlight data successfully written to Silver Layer.")


# =========================
# STOP SPARK
# =========================

spark.stop()