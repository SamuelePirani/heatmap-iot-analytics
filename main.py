from pyspark.sql import SparkSession

from Data_Analysis_Spark.CO2Analyzer import CO2Analyzer
from Data_Analysis_Spark.SparkDataReader import SparkDataReader


def main():
    spark = SparkSession.builder.appName("HeatMapJob").getOrCreate()
    try:
        print("Loading Data...")
        reader = SparkDataReader(spark)
        co2_analyzer = CO2Analyzer(spark, reader)
        co2_analyzer.run_analysis()
        print("Loading Operation Complete")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
