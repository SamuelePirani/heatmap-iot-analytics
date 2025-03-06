import os
import logging
from pyspark.sql import SparkSession
from src.analysis.analyzer import Analyzer
from src.analysis.spark_data_reader import SparkDataReader
from config.configuration_manager import ConfigurationManager

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
        logger.info("Setup Environment...")
        config_manager = ConfigurationManager(os.path.join(os.getcwd(), "config.yml"))
        config_manager.setup_data_path_user()
        config = config_manager.get_config()
        logger.info("Setup Complete")
        logger.info("Loading data...")
        reader = SparkDataReader(spark, config)
        analyzer = Analyzer(reader)
        logger.info("Loading Operation Complete")
        logger.info("Running analysis...")
        analyzer.run_analysis(config["intervals"])
        logger.info("Analysis complete")
    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        logger.info("Finalizing Spark Job...")
        spark.stop()


if __name__ == "__main__":
    main()
