import logging
from src.normalization.data_id_mapper import DataIdMarker, write_data

logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

def invoke_normalization(config_file):
    try:
        if config_file["is_normalized"] is not True:
            data_normalizer = DataIdMarker(config_file["config_datapath"]["iot_data"])
            logger.info("Start Data Normalization...")
            csv_data = data_normalizer.read_data()
            write_data(csv_data)
            logger.info("Data Normalization Complete")
        else:
            logger.info("Data already normalized")
    except Exception as e:
        print(f"Error: {e}")
