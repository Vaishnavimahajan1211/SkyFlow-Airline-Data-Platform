"""
Booking Transformation using PySpark
"""

from pyspark.sql.functions import upper, trim, col

from python.spark.spark_session import get_spark
from python.config.config import BRONZE_FOLDER

spark = get_spark()

# Read Bronze Layer
df = spark.read.csv(
    str(BRONZE_FOLDER / "booking.csv"),
    header=True,
    inferSchema=True
)

print("\n========== ORIGINAL BOOKING DATA ==========")
df.show(10, truncate=False)

# Remove duplicate bookings
df = df.dropDuplicates(["booking_id"])

# Remove null booking ids
df = df.dropna(subset=["booking_id"])

# Trim string columns
string_columns = [
    "passenger_id",
    "flight_id",
    "seat_class",
    "booking_status",
    "payment_status"
]

for column in string_columns:
    df = df.withColumn(column, trim(col(column)))

# Convert important fields to uppercase
df = (
    df.withColumn("seat_class", upper(col("seat_class")))
      .withColumn("booking_status", upper(col("booking_status")))
      .withColumn("payment_status", upper(col("payment_status")))
)

# Select required columns
df = df.select(
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

# Sort by booking id
df = df.orderBy("booking_id")

print("\n========== TRANSFORMED BOOKING DATA ==========")
df.show(20, truncate=False)

print("\nTotal Bookings :", df.count())

spark.stop()