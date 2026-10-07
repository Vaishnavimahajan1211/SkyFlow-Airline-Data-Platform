import os
from pathlib import Path

# ==============================
# HADOOP CONFIGURATION
# ==============================

os.environ["HADOOP_HOME"] = r"C:\hadoop"
os.environ["PATH"] = r"C:\hadoop\bin;" + os.environ.get("PATH", "")

# ==============================
# PYSPARK
# ==============================

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    trim,
    upper,
    to_timestamp,
    round as spark_round,
    sum as spark_sum,
    count
)

# ==============================
# PROJECT PATH
# ==============================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

SILVER_PAYMENT_FOLDER = PROJECT_ROOT / "data" / "silver" / "payment"
GOLD_PAYMENT_FOLDER = PROJECT_ROOT / "data" / "gold" / "fact_payment"

# ==============================
# SPARK SESSION
# ==============================

spark = (
    SparkSession.builder
    .appName("SkyFlow_Payment_Fact")
    .master("local[*]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

print("\n========== PAYMENT FACT PIPELINE ==========")

print("\nSilver Payment Folder:")
print(SILVER_PAYMENT_FOLDER)

# ==============================
# FIND SILVER FILE
# ==============================

payment_files = list(SILVER_PAYMENT_FOLDER.glob("part-*.csv"))

print("\nPayment Files Found:")
print(payment_files)

if not payment_files:
    raise FileNotFoundError(
        "No Silver Payment CSV file found."
    )

silver_file = payment_files[0]

print("\nSilver Payment File:")
print(silver_file)

# ==============================
# READ SILVER PAYMENT
# ==============================

df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(str(silver_file))
)

print("\n========== SILVER PAYMENT DATA ==========")

df.show(5, truncate=False)

print("\nSilver Payment Schema:")
df.printSchema()

# ==============================
# TRANSFORMATION
# ==============================

df_gold = (
    df
    .dropDuplicates(["payment_id"])
    .dropna(subset=["payment_id"])

    # Clean IDs
    .withColumn("payment_id", trim(col("payment_id")))
    .withColumn("booking_id", trim(col("booking_id")))

    # Clean payment attributes
    .withColumn(
        "payment_method",
        upper(trim(col("payment_method")))
    )
    .withColumn(
        "payment_status",
        upper(trim(col("payment_status")))
    )

    # Convert payment date
    .withColumn(
        "payment_date",
        to_timestamp(col("payment_date"))
    )

    # Standardize amount
    .withColumn(
        "amount",
        spark_round(col("amount"), 2)
    )

    # Final Gold columns
    .select(
        "payment_id",
        "booking_id",
        "payment_date",
        "payment_method",
        "amount",
        "payment_status"
    )

    .orderBy("payment_id")
)

# ==============================
# VALIDATION
# ==============================

print("\n========== GOLD PAYMENT DATA ==========")

df_gold.show(10, truncate=False)

total_payments = df_gold.count()

print("\nTotal Payments :", total_payments)

# ==============================
# PAYMENT METRICS
# ==============================

successful_payments = (
    df_gold
    .filter(col("payment_status") == "SUCCESS")
    .count()
)

failed_payments = (
    df_gold
    .filter(col("payment_status") == "FAILED")
    .count()
)

pending_payments = (
    df_gold
    .filter(col("payment_status") == "PENDING")
    .count()
)

successful_revenue = (
    df_gold
    .filter(col("payment_status") == "SUCCESS")
    .agg(spark_sum("amount"))
    .collect()[0][0]
)

print("\nSuccessful Payments :", successful_payments)
print("Failed Payments     :", failed_payments)
print("Pending Payments    :", pending_payments)
print(
    "Successful Payment Revenue :",
    round(successful_revenue or 0, 2)
)

# ==============================
# WRITE GOLD
# ==============================

print("\n========== WRITING GOLD PAYMENT FACT ==========")

(
    df_gold
    .coalesce(1)
    .write
    .mode("overwrite")
    .option("header", True)
    .csv(str(GOLD_PAYMENT_FOLDER))
)

print("\nPayment Fact Table successfully written to Gold Layer.")
print("Gold Path :", GOLD_PAYMENT_FOLDER)

print("\n========== PAYMENT FACT COMPLETED ==========\n")

# ==============================
# STOP SPARK
# ==============================

spark.stop()