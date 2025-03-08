import logging

from src.normalization.data_id_mapper import DataIdMapper

logger = logging.getLogger(__name__)
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)


def invoke_normalization(config: dict) -> None:
    if not config.get("is_normalized", False):
        iot_data_path = config["config_datapath"]["iot_data"]
        logger.info("Starting data normalization process...")
        data_mapper = DataIdMapper(iot_data_path)
        data_mapper.normalize_all()
        logger.info("Data normalization complete")
    else:
        logger.info("Data already normalized")
