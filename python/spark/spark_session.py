"""
Spark Session
SkyFlow Enterprise Airline Data Platform
"""

from pyspark.sql import SparkSession


def get_spark():

    spark = (
        SparkSession.builder
        .appName("SkyFlow")
        .master("local[*]")
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("ERROR")

    return spark


if __name__ == "__main__":

    spark = get_spark()

    print("=" * 50)
    print("Spark Session Created Successfully")
    print("=" * 50)

    print("Application Name :", spark.sparkContext.appName)
    print("Spark Version    :", spark.version)

    spark.stop()