from pyspark.sql import SparkSession

from src.analysis.co2_analyzer import CO2Analyzer
from src.analysis.spark_data_reader import SparkDataReader


def main():
    spark = SparkSession.builder.appName("HeatMapJob").getOrCreate()
    try:
        print("Loading data...")
        reader = SparkDataReader(spark)
        co2_analyzer = CO2Analyzer(spark, reader)
        #co2_analyzer.run_analysis()
        print("Loading Operation Complete")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
