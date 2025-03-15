import logging
import os

from pyspark.sql import SparkSession

from src.analysis.analyzer import Analyzer
from src.analysis.spark_data_reader import SparkDataReader
from src.config.configuration_manager import ConfigurationManager
from src.database.db_config import connect_to_db
from src.normalization.mapper_invoker import invoke_normalization

logger = logging.getLogger(__name__)
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)


def setup_spark():
    logger.info("Initializing Spark session...")
    spark = SparkSession.builder.appName("HeatMapJob").getOrCreate()
    spark.sparkContext.setLogLevel("WARN")
    return spark


def load_configuration(config_path: str):
    logger.info("Setting up configuration...")
    config_manager = ConfigurationManager(config_path)
    config = config_manager.configure_data_paths()
    logger.info("Configuration setup complete")
    return config


def run_normalization(config: dict):
    try:
        invoke_normalization(config)
    except Exception as e:
        logger.error(f"Error during normalization: {e}")
        raise


def load_and_analyze(spark, config: dict, client):
    try:
        logger.info("Loading data...")
        reader = SparkDataReader(spark, config)
        analyzer = Analyzer(reader)
        logger.info("Data loading complete")
        logger.info("Running analysis...")
        analyzer.run_analysis(config["intervals"], client)
        logger.info("Analysis complete")
    except Exception as e:
        logger.error(f"Error during loading or analysis: {e}")
        raise


def finalize_spark(spark):
    if spark:
        logger.info("Finalizing Spark Job...")
        spark.stop()


def main():
    spark = None
    try:
        spark = setup_spark()
        client = connect_to_db()
        config_path = os.path.join(os.getcwd(), "config.yml")
        config = load_configuration(config_path)
        run_normalization(config)
        load_and_analyze(spark, config, client)
    except Exception as e:
        logger.error(f"Execution failed: {e}")
    finally:
        finalize_spark(spark)


if __name__ == "__main__":
    main()
