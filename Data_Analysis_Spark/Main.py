from pyspark.sql import SparkSession

from CO2_SparkAnalyzer import CO2_Analyzer
from SparkDataReader import SparkDataRader

spark = SparkSession.builder.appName("HeatMapJob").getOrCreate()

try:
    print("Loading Data...")

    reader = SparkDataRader(spark)
    co2 = CO2_Analyzer(spark, reader)
    co2.run_analysis()

    print("Loading Operation Complete")
except Exception as e:
    print(f"Error: {e}")
finally:
    spark.stop()
