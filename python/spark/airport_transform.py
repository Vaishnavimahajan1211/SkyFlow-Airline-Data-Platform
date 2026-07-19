"""
Airport Transformation using PySpark
"""

from pyspark.sql.functions import upper, col

from python.spark.spark_session import get_spark
from python.config.config import SILVER_FOLDER

spark = get_spark()

df = spark.read.csv(
    str(SILVER_FOLDER / "airport.csv"),
    header=True,
    inferSchema=True
)

print("\n========== ORIGINAL ==========")
df.show(5, truncate=False)

# Select only required columns
df = df.select(
    "airport_code",
    "airport_name",
    "city",
    "country"
)

# Convert country to uppercase
df = df.withColumn(
    "country",
    upper(col("country"))
)

# Sort by airport code
df = df.orderBy("airport_code")

print("\n========== TRANSFORMED ==========")
df.show(20, truncate=False)

print("\nTotal Airports :", df.count())

spark.stop()