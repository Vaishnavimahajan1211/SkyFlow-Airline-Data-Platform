"""
Booking Summary using PySpark
"""

from pyspark.sql.functions import count, sum, round

from python.spark.spark_session import get_spark
from python.config.config import SILVER_FOLDER

spark = get_spark()

# Read datasets
booking_df = spark.read.csv(
    str(SILVER_FOLDER / "booking.csv"),
    header=True,
    inferSchema=True
)

passenger_df = spark.read.csv(
    str(SILVER_FOLDER / "passenger.csv"),
    header=True,
    inferSchema=True
)

# Join booking with passenger
joined_df = booking_df.join(
    passenger_df,
    on="passenger_id",
    how="inner"
)

print("\n===== Joined Data =====")
joined_df.show(10, truncate=False)

summary_df = (
    joined_df
    .groupBy("seat_class")
    .agg(
        count("*").alias("total_bookings")
    )
    .orderBy("seat_class")
)

print("\n===== Booking Summary =====")
summary_df.show(truncate=False)

spark.stop()