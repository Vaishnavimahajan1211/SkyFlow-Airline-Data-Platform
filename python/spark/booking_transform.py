"""
Booking Transformation using PySpark
Bronze -> Silver
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, trim, upper, round

from python.config.config import BRONZE_FOLDER, SILVER_FOLDER


# =========================
# SPARK SESSION
# =========================

spark = (
    SparkSession.builder
    .appName("Booking Silver Transformation")
    .master("local[*]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")


# =========================
# READ BRONZE DATA
# =========================

booking_df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(str(BRONZE_FOLDER / "booking.csv"))
)


print("\n========== ORIGINAL BOOKING DATA ==========")
booking_df.show(10, truncate=False)


# =========================
# TRANSFORMATION
# =========================

booking_silver = (
    booking_df

    # Remove duplicate bookings
    .dropDuplicates(["booking_id"])

    # Remove records without booking_id
    .filter(col("booking_id").isNotNull())

    # Clean string columns
    .withColumn("booking_id", trim(col("booking_id")))
    .withColumn("passenger_id", trim(col("passenger_id")))
    .withColumn("flight_id", trim(col("flight_id")))
    .withColumn("seat_class", upper(trim(col("seat_class"))))
    .withColumn("booking_status", upper(trim(col("booking_status"))))
    .withColumn("payment_status", upper(trim(col("payment_status"))))

    # Round financial columns
    .withColumn("ticket_price", round(col("ticket_price"), 2))
    .withColumn("tax", round(col("tax"), 2))
    .withColumn("discount", round(col("discount"), 2))
    .withColumn("final_amount", round(col("final_amount"), 2))

    # Select required columns
    .select(
        "booking_id",
        "passenger_id",
        "flight_id",
        "booking_date",
        "seat_class",
        "booking_status",
        "ticket_price",
        "tax",
        "discount",
        "final_amount",
        "payment_status"
    )

    # Sort by booking ID
    .orderBy("booking_id")
)


# =========================
# SHOW TRANSFORMED DATA
# =========================

print("\n========== TRANSFORMED BOOKING DATA ==========")

booking_silver.show(20, truncate=False)

print(f"\nTotal Bookings : {booking_silver.count()}")


# =========================
# WRITE TO SILVER
# =========================

(
    booking_silver
    .write
    .mode("overwrite")
    .option("header", True)
    .csv(str(SILVER_FOLDER / "booking"))
)


print("\nBooking data successfully written to Silver Layer.")


# =========================
# STOP SPARK
# =========================

spark.stop()