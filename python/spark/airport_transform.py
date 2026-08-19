"""
SkyFlow - Airport Silver Transformation

Bronze Layer  ->  Cleaning & Transformation  ->  Silver Layer
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, trim, upper, initcap


from python.config.config import BRONZE_FOLDER, SILVER_FOLDER


# ============================================================
# 1. CREATE SPARK SESSION
# ============================================================

spark = (
    SparkSession.builder
    .appName("SkyFlow - Airport Silver Transformation")
    .master("local[*]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")


# ============================================================
# 2. READ BRONZE AIRPORT DATA
# ============================================================

bronze_path = str(BRONZE_FOLDER / "airport.csv")

airport_df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(bronze_path)
)

print("\n" + "=" * 70)
print("ORIGINAL AIRPORT DATA - BRONZE LAYER")
print("=" * 70)

airport_df.show(10, truncate=False)


# ============================================================
# 3. CLEAN AND TRANSFORM DATA
# ============================================================

airport_silver = (
    airport_df

    # Clean airport code
    .withColumn(
        "airport_code",
        upper(trim(col("airport_code")))
    )

    # Clean airport name
    .withColumn(
        "airport_name",
        trim(col("airport_name"))
    )

    # Standardize city name
    .withColumn(
        "city",
        initcap(trim(col("city")))
    )

    # Standardize country name
    .withColumn(
        "country",
        initcap(trim(col("country")))
    )

    # Clean timezone
    .withColumn(
        "timezone",
        trim(col("timezone"))
    )

    # Remove records where airport code is missing
    .filter(
        col("airport_code").isNotNull()
        & (trim(col("airport_code")) != "")
    )

    # Remove duplicate airports
    .dropDuplicates(["airport_code"])

    # Select final Silver columns
    .select(
        "airport_code",
        "airport_name",
        "city",
        "country",
        "timezone"
    )
)


# ============================================================
# 4. SHOW TRANSFORMED DATA
# ============================================================

print("\n" + "=" * 70)
print("TRANSFORMED AIRPORT DATA - SILVER LAYER")
print("=" * 70)

airport_silver.show(20, truncate=False)


# ============================================================
# 5. DATA QUALITY SUMMARY
# ============================================================

total_airports = airport_silver.count()

print("\n" + "=" * 70)
print("AIRPORT DATA QUALITY SUMMARY")
print("=" * 70)

print(f"Total Airports : {total_airports}")

print("\nNull Values:")
airport_silver.select(
    [
        col(column).isNull().cast("int").alias(column)
        for column in airport_silver.columns
    ]
).show()


# ============================================================
# 6. WRITE DATA TO SILVER LAYER
# ============================================================

silver_path = str(SILVER_FOLDER / "airport")

(
    airport_silver
    .write
    .mode("overwrite")
    .option("header", True)
    .csv(silver_path)
)


# ============================================================
# 7. SUCCESS MESSAGE
# ============================================================

print("\n" + "=" * 70)
print("SUCCESS")
print("=" * 70)

print("Airport data successfully written to Silver Layer.")
print(f"Silver Path : {silver_path}")


# ============================================================
# 8. STOP SPARK
# ============================================================

spark.stop()