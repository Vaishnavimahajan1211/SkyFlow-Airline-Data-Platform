
import os
from pathlib import Path

os.environ["HADOOP_HOME"] = r"C:\hadoop"
os.environ["PATH"] = r"C:\hadoop\bin;" + os.environ.get("PATH", "")

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    trim,
    upper,
    to_timestamp,
    round as spark_round
)
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    IntegerType
)

# ==============================
# PROJECT PATHS
# ==============================

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SILVER_FLIGHT_FOLDER = PROJECT_ROOT / "data" / "silver" / "flight"
GOLD_FLIGHT_FOLDER = PROJECT_ROOT / "data" / "gold" / "fact_flight"

# ==============================
# SILVER CSV SCHEMA
# ==============================

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

# ==============================
# SPARK SESSION
# ==============================

spark = (
    SparkSession.builder
    .appName("SkyFlow_Flight_Fact")
    .master("local[*]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

try:
    print("\n========== FLIGHT FACT PIPELINE ==========")
    print("\nSilver Flight Folder:")
    print(SILVER_FLIGHT_FOLDER)

    # ==============================
    # FIND SILVER CSV
    # ==============================

    flight_files = sorted(
        SILVER_FLIGHT_FOLDER.glob("part-*.csv")
    )

    print("\nFlight Files Found:")
    print(flight_files)

    if not flight_files:
        raise FileNotFoundError(
            f"No Silver Flight CSV found in {SILVER_FLIGHT_FOLDER}"
        )

    silver_file = flight_files[0]
    print("\nSilver Flight File:")
    print(silver_file)

    # ==============================
    # READ SILVER
    # ==============================

    df = (
        spark.read
        .schema(flight_schema)
        .option("header", True)
        .csv(str(silver_file))
    )

    print("\n========== SILVER FLIGHT DATA ==========")
    df.show(5, truncate=False)

    print("\nSilver Flight Schema:")
    df.printSchema()

    # ==============================
    # TRANSFORM TO GOLD
    # ==============================

    df_gold = (
        df
        .withColumn("flight_id", trim(col("flight_id")))
        .dropna(subset=["flight_id"])
        .filter(col("flight_id") != "")
        .dropDuplicates(["flight_id"])

        .withColumn("flight_number", trim(col("flight_number")))
        .withColumn("route_id", trim(col("route_id")))
        .withColumn("aircraft_id", trim(col("aircraft_id")))

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

        # Parse ISO timestamps, including timezone offsets
        .withColumn(
            "departure_datetime",
            to_timestamp(
                col("departure_datetime"),
                "yyyy-MM-dd'T'HH:mm:ss.SSSXXX"
            )
        )
        .withColumn(
            "arrival_datetime",
            to_timestamp(
                col("arrival_datetime"),
                "yyyy-MM-dd'T'HH:mm:ss.SSSXXX"
            )
        )

        .withColumn(
            "delay_minutes",
            spark_round(col("delay_minutes"), 0).cast("integer")
        )

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
        .orderBy("flight_id")
    )

    # ==============================
    # VALIDATE GOLD
    # ==============================

    print("\n========== GOLD FLIGHT DATA ==========")
    df_gold.show(10, truncate=False)

    total_flights = df_gold.count()

    null_departures = df_gold.filter(
        col("departure_datetime").isNull()
    ).count()

    null_arrivals = df_gold.filter(
        col("arrival_datetime").isNull()
    ).count()

    print("\nTotal Flights:", total_flights)
    print("Null Departure Datetimes:", null_departures)
    print("Null Arrival Datetimes  :", null_arrivals)

    print("\nTerminal Distribution:")
    df_gold.groupBy("terminal").count().orderBy("terminal").show()

    print("\nGold Flight Schema:")
    df_gold.printSchema()

    # ==============================
    # OPERATIONAL METRICS
    # ==============================

    completed_flights = df_gold.filter(
        col("flight_status").isin("LANDED", "DEPARTED")
    ).count()

    delayed_flights = df_gold.filter(
        col("delay_minutes") > 0
    ).count()

    cancelled_flights = df_gold.filter(
        col("flight_status") == "CANCELLED"
    ).count()

    print("\n========== OPERATIONAL METRICS ==========")
    print("Completed Flights:", completed_flights)
    print("Delayed Flights  :", delayed_flights)
    print("Cancelled Flights:", cancelled_flights)

    # ==============================
    # WRITE GOLD
    # ==============================

    print("\n========== WRITING GOLD FLIGHT FACT ==========")

    (
        df_gold
        .coalesce(1)
        .write
        .mode("overwrite")
        .option("header", True)
        .csv(str(GOLD_FLIGHT_FOLDER))
    )

    print("\nFlight Fact Table successfully written to Gold Layer.")
    print("Gold Path:", GOLD_FLIGHT_FOLDER)
    print("\n========== FLIGHT FACT COMPLETED ==========")

finally:
    spark.stop()
    print("Spark session stopped.")
