"""
Payment Transformation using PySpark
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
    .appName("Payment Silver Transformation")
    .master("local[*]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")


# =========================
# READ BRONZE DATA
# =========================

payment_df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(str(BRONZE_FOLDER / "payment.csv"))
)


print("\n========== ORIGINAL PAYMENT DATA ==========")

payment_df.show(10, truncate=False)


# =========================
# TRANSFORMATION
# =========================

payment_silver = (
    payment_df

    # Clean IDs
    .withColumn(
        "payment_id",
        upper(trim(col("payment_id")))
    )
    .withColumn(
        "booking_id",
        upper(trim(col("booking_id")))
    )

    # Convert payment date to timestamp
    .withColumn(
        "payment_date",
        to_timestamp(col("payment_date"))
    )

    # Clean payment method
    .withColumn(
        "payment_method",
        upper(trim(col("payment_method")))
    )

    # Clean payment status
    .withColumn(
        "payment_status",
        upper(trim(col("payment_status")))
    )

    # Ensure amount is numeric
    .withColumn(
        "amount",
        col("amount").cast("double")
    )

    # Remove duplicate payments
    .dropDuplicates(["payment_id"])

    # Remove records without payment ID
    .filter(col("payment_id").isNotNull())

    # Keep required columns
    .select(
        "payment_id",
        "booking_id",
        "payment_date",
        "payment_method",
        "amount",
        "payment_status"
    )

    # Sort by payment ID
    .orderBy("payment_id")
)


# =========================
# SHOW TRANSFORMED DATA
# =========================

print("\n========== TRANSFORMED PAYMENT DATA ==========")

payment_silver.show(20, truncate=False)

print(f"\nTotal Payments : {payment_silver.count()}")


# =========================
# WRITE TO SILVER
# =========================

(
    payment_silver
    .write
    .mode("overwrite")
    .option("header", True)
    .csv(str(SILVER_FOLDER / "payment"))
)


print("\nPayment data successfully written to Silver Layer.")


# =========================
# STOP SPARK
# =========================

spark.stop()