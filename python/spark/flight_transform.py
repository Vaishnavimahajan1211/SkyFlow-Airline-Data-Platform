
"""
Flight Transformation using PySpark
Bronze -> Silver
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, trim, upper, to_timestamp
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    IntegerType
)

from python.config.config import BRONZE_FOLDER, SILVER_FOLDER


# =========================
# SPARK SESSION
# =========================

spark = (
    SparkSession.builder
    .appName("Flight Silver Transformation")
    .master("local[*]")
    .config("spark.driver.host", "127.0.0.1")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")


try:
    # =========================
    # READ BRONZE DATA
    # =========================

    flight_schema = StructType([
        StructField("flight_id", StringType(), True),
        StructField("flight_number", StringType(), True),
        StructField("route_id", StringType(), True),
        StructField("aircraft_id", StringType(), True),
        StructField("departure_datetime", StringType(), True),
        StructField("arrival_datetime", StringType(), True),
        StructField("flight_status", StringType(), True),
        StructField("terminal", StringType(), True),
        StructField("gate_number", StringType(), True),
        StructField("delay_minutes", IntegerType(), True)
    ])

    flight_df = (
        spark.read
        .option("header", True)
        .schema(flight_schema)
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

        # Convert datetime columns
        .withColumn(
            "departure_datetime",
            to_timestamp(col("departure_datetime"), "yyyy-MM-dd HH:mm:ss")
        )
        .withColumn(
            "arrival_datetime",
            to_timestamp(col("arrival_datetime"), "yyyy-MM-dd HH:mm:ss")
        )

        # Clean status
        .withColumn(
            "flight_status",
            upper(trim(col("flight_status")))
        )

        # Keep terminal as text: T1, T2, T3
        .withColumn(
            "terminal",
            upper(trim(col("terminal").cast("string")))
        )

        # Clean gate
        .withColumn(
            "gate_number",
            upper(trim(col("gate_number")))
        )

        # Ensure delay is an integer
        .withColumn(
            "delay_minutes",
            col("delay_minutes").cast("integer")
        )

        # Remove duplicate flights
        .dropDuplicates(["flight_id"])

        # Remove missing flight IDs
        .filter(
            col("flight_id").isNotNull()
            & (trim(col("flight_id")) != "")
        )

        # Select required columns
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

        # Sort flights
        .orderBy("flight_id")
    )

    # =========================
    # VERIFY TRANSFORMED DATA
    # =========================

    print("\n========== TRANSFORMED FLIGHT DATA ==========")
    flight_silver.show(20, truncate=False)

    print("\n========== FLIGHT SCHEMA ==========")
    flight_silver.printSchema()

    print("\n========== TERMINAL VALUES ==========")
    flight_silver.groupBy("terminal").count().show()

    print(f"\nTotal Flights: {flight_silver.count()}")

    # =========================
    # WRITE TO SILVER
    # =========================

    output_path = str(SILVER_FOLDER / "flight")

    (
        flight_silver
        .write
        .mode("overwrite")
        .option("header", True)
        .csv(output_path)
    )

    print(f"\nFlight data successfully written to Silver Layer: {output_path}")

finally:
    # =========================
    # STOP SPARK
    # =========================

    spark.stop()
    print("Spark session stopped.")


