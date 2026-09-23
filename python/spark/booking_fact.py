"""
SkyFlow - Booking Fact Table
"""

import os

os.environ["HADOOP_HOME"] = r"C:\hadoop"
os.environ["PATH"] = r"C:\hadoop\bin;" + os.environ.get("PATH", "")

from pyspark.sql.functions import (
trim,
upper,
col,
to_timestamp,
round
)

from python.spark.spark_session import get_spark
from python.config.config import SILVER_FOLDER, GOLD_FOLDER

print("\n========== BOOKING FACT PIPELINE ==========")

spark = get_spark()

# ==========================================================

# PATHS

# ==========================================================

SILVER_BOOKING_FOLDER = SILVER_FOLDER / "booking"
GOLD_BOOKING_FOLDER = GOLD_FOLDER / "fact_booking"

print("\nSilver Booking Folder:")
print(SILVER_BOOKING_FOLDER)

# ==========================================================

# FIND SILVER BOOKING FILE

# ==========================================================

booking_files = list(
SILVER_BOOKING_FOLDER.glob("part-*.csv")
)

print("\nBooking Files Found:")
print(booking_files)

silver_booking_file = booking_files[0]

print("\nSilver Booking File:")
print(silver_booking_file)

# ==========================================================

# READ SILVER BOOKING

# ==========================================================

df = spark.read.csv(
str(silver_booking_file),
header=True,
inferSchema=True
)

print("\n========== SILVER BOOKING DATA ==========")

df.show(
20,
truncate=False
)

# ==========================================================

# GOLD TRANSFORMATION

# ==========================================================

df_gold = (
df

# Remove duplicate bookings
.dropDuplicates(["booking_id"])

# Remove invalid booking IDs
.dropna(subset=["booking_id"])

# Clean booking ID
.withColumn(
    "booking_id",
    trim(col("booking_id"))
)

# Clean passenger ID
.withColumn(
    "passenger_id",
    trim(col("passenger_id"))
)

# Clean flight ID
.withColumn(
    "flight_id",
    trim(col("flight_id"))
)

# Convert booking date to timestamp
.withColumn(
    "booking_date",
    to_timestamp(col("booking_date"))
)

# Standardize seat class
.withColumn(
    "seat_class",
    upper(trim(col("seat_class")))
)

# Standardize booking status
.withColumn(
    "booking_status",
    upper(trim(col("booking_status")))
)

# Standardize payment status
.withColumn(
    "payment_status",
    upper(trim(col("payment_status")))
)

# Round monetary values
.withColumn(
    "ticket_price",
    round(col("ticket_price"), 2)
)

.withColumn(
    "tax",
    round(col("tax"), 2)
)

.withColumn(
    "discount",
    round(col("discount"), 2)
)

.withColumn(
    "final_amount",
    round(col("final_amount"), 2)
)

# Select final Gold columns
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

)

# ==========================================================

# DISPLAY GOLD DATA

# ==========================================================

print("\n========== GOLD BOOKING FACT ==========")

df_gold.show(
20,
truncate=False
)

# ==========================================================

# COUNT BOOKINGS

# ==========================================================

total_bookings = df_gold.count()

print("\nTotal Bookings :", total_bookings)

# ==========================================================

# REVENUE SUMMARY

# ==========================================================

total_revenue = (
df_gold
.filter(col("booking_status") != "CANCELLED")
.agg(
round(
__import__("pyspark.sql.functions", fromlist=["sum"])
.sum("final_amount"),
2
).alias("total_revenue")
)
.collect()[0]["total_revenue"]
)

print("\nTotal Revenue from Active Bookings :", total_revenue)

# ==========================================================

# CREATE GOLD FOLDER

# ==========================================================

GOLD_BOOKING_FOLDER.mkdir(
parents=True,
exist_ok=True
)

print("\n========== WRITING GOLD BOOKING FACT ==========")

# ==========================================================

# WRITE GOLD DATA

# ==========================================================

(
df_gold
.coalesce(1)
.write
.mode("overwrite")
.option("header", True)
.csv(str(GOLD_BOOKING_FOLDER))
)

print(
"\nBooking Fact Table successfully written to Gold Layer."
)

print(
"Gold Path :",
GOLD_BOOKING_FOLDER
)

print(
"\n========== BOOKING FACT COMPLETED =========="
)

spark.stop()
