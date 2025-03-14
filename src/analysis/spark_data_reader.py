import os
from concurrent.futures import ThreadPoolExecutor
from typing import List

import yaml
from pyspark.sql import SparkSession, DataFrame


def _load_config(config_path: str = None) -> dict:
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    config_file_path = config_path or os.path.join(root, "config.yml")
    with open(config_file_path) as file:
        config = yaml.safe_load(file)
    config["iot_data"] = os.path.join(root, config["iot_data"])
    return config


class SparkDataReader:
    def __init__(self, spark: SparkSession, config: dict) -> None:
        self.spark = spark
        self.iot_data_path = config["config_datapath"]["iot_data"]

    def _read_file(self, full_path: str) -> DataFrame:
        df = self.spark.read.csv(full_path, header=False, inferSchema=True)
        base_name = os.path.splitext(os.path.basename(full_path))[0]
        column_names = ["ID_Room", "Timestamp", f"Value_{base_name}"]
        return df.toDF(*column_names)

    def _read_files_in_subdir(self, file_list: List[str]) -> List[DataFrame]:
        return [self._read_file(file_path) for file_path in file_list]

    def read(self, file_suffix: str) -> List[List[DataFrame]]:
        rooms = []
        tasks = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            for subdir, _, files in os.walk(self.iot_data_path):
                csv_files = [os.path.join(subdir, str(f)) for f in files if str(f).endswith(file_suffix)]
                if csv_files:
                    tasks.append(executor.submit(self._read_files_in_subdir, csv_files))
            for future in tasks:
                try:
                    group_dfs = future.result()
                    rooms.append(group_dfs)
                except Exception as e:
                    raise RuntimeError(f"Error reading files in subdir: {e}") from e
        return rooms
