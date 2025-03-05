import logging

from pyspark.sql import SparkSession

from src.analysis.co2_analyzer import CO2Analyzer
from src.analysis.spark_data_reader import SparkDataReader

logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)


def main():
    spark = SparkSession.builder.appName("HeatMapJob") \
        .getOrCreate()
    spark.sparkContext.setLogLevel("WARN")
    try:
        logger.info("Loading data")
        reader = SparkDataReader(spark)
        logger.info("Running analysis")
        co2_analyzer = CO2Analyzer(spark, reader)
        logger.info("Loading Operation Complete")
        co2_analyzer.run_analysis()
    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
