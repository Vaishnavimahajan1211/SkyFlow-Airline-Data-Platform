"""
Passenger Transformation using PySpark
Bronze -> Silver
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, trim, upper, initcap, to_date

from python.config.config import BRONZE_FOLDER, SILVER_FOLDER


# =========================
# SPARK SESSION
# =========================

spark = (
    SparkSession.builder
    .appName("Passenger Silver Transformation")
    .master("local[*]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")


# =========================
# READ BRONZE DATA
# =========================

passenger_df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(str(BRONZE_FOLDER / "passenger.csv"))
)


print("\n========== ORIGINAL PASSENGER DATA ==========")

passenger_df.show(10, truncate=False)


# =========================
# TRANSFORMATION
# =========================

passenger_silver = (
    passenger_df

    # Clean passenger ID
    .withColumn(
        "passenger_id",
        upper(trim(col("passenger_id")))
    )

    # Clean names
    .withColumn(
        "first_name",
        initcap(trim(col("first_name")))
    )
    .withColumn(
        "last_name",
        initcap(trim(col("last_name")))
    )

    # Clean gender
    .withColumn(
        "gender",
        initcap(trim(col("gender")))
    )

    # Convert DOB to date
    .withColumn(
        "date_of_birth",
        to_date(col("date_of_birth"))
    )

    # Clean email
    .withColumn(
        "email",
        trim(col("email"))
    )

    # Clean phone
    .withColumn(
        "phone",
        trim(col("phone"))
    )

    # Clean passport
    .withColumn(
        "passport_number",
        upper(trim(col("passport_number")))
    )

    # Clean nationality
    .withColumn(
        "nationality",
        initcap(trim(col("nationality")))
    )

    # Remove duplicate passengers
    .dropDuplicates(["passenger_id"])

    # Remove records without passenger ID
    .filter(col("passenger_id").isNotNull())

    # Select required columns
    .select(
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

    # Sort by passenger ID
    .orderBy("passenger_id")
)


# =========================
# SHOW TRANSFORMED DATA
# =========================

print("\n========== TRANSFORMED PASSENGER DATA ==========")

passenger_silver.show(20, truncate=False)

print(f"\nTotal Passengers : {passenger_silver.count()}")


# =========================
# WRITE TO SILVER
# =========================

(
    passenger_silver
    .write
    .mode("overwrite")
    .option("header", True)
    .csv(str(SILVER_FOLDER / "passenger"))
)


print("\nPassenger data successfully written to Silver Layer.")


# =========================
# STOP SPARK
# =========================

spark.stop()