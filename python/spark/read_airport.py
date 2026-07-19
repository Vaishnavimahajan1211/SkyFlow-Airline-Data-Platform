"""
Read Airport Dataset using PySpark
"""

from python.spark.spark_session import get_spark
from python.config.config import SILVER_FOLDER

spark = get_spark()

df = spark.read.csv(
    str(SILVER_FOLDER / "airport.csv"),
    header=True,
    inferSchema=True
)

print("=" * 60)
print("SCHEMA")
print("=" * 60)

df.printSchema()

print("=" * 60)
print("FIRST 10 ROWS")
print("=" * 60)

df.show(10, truncate=False)

print("=" * 60)
print("TOTAL RECORDS")
print("=" * 60)

print(df.count())

spark.stop()