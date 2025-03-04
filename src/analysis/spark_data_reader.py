import os
from typing import List

import yaml
from pyspark.sql import SparkSession, DataFrame


class SparkDataReader:

    def __init__(self, spark: SparkSession, config_path: str = None):
        self.spark_session = spark
        self.config = self._load_config(config_path)
        self.data_path = self.config["iot_data_path"]

    def _load_config(self, config_path: str = None) -> dict:
        root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        config_file_path = config_path or os.path.join(root, "config.yml")
        with open(config_file_path, "r") as file:
            config = yaml.safe_load(file)
        config["iot_data_path"] = os.path.join(root, config["iot_data_path"])
        return config

    def read(self, file_suffix: str) -> List[DataFrame]:
        rooms = []
        for subdir, _, files in os.walk(self.data_path):
            csv_files = []
            for filename in files:
                if filename.endswith(file_suffix):
                    full_path = os.path.join(subdir, filename)
                    df = self.spark_session.read.csv(full_path, header=False, inferSchema=True)
                    base_name = os.path.splitext(filename)[0]
                    column_names = ["ID_Room", "Timestamp", f"Value_{base_name}"]
                    df = df.toDF(*column_names)
                    csv_files.append(df)
            rooms.append(csv_files)
        return rooms
