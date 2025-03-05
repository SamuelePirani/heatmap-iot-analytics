import os
from typing import List
import yaml
from concurrent.futures import ThreadPoolExecutor
from pyspark.sql import SparkSession, DataFrame


def _load_config(config_path: str = None) -> dict:
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    config_file_path = config_path or os.path.join(root, "config.yml")
    with open(config_file_path, "r") as file:
        config = yaml.safe_load(file)
    config["iot_data_path"] = os.path.join(root, config["iot_data_path"])
    return config


class SparkDataReader:

    def __init__(self, spark: SparkSession, config_path: str = None):
        self.spark_session = spark
        self.config = _load_config(config_path)
        self.data_path = self.config["iot_data_path"]

    def _read_file(self, full_path):
        df = self.spark_session.read.csv(full_path, header=False, inferSchema=True)
        base_name = os.path.splitext(os.path.basename(full_path))[0]
        column_names = ["ID_Room", "Timestamp", f"Value_{base_name}"]
        df = df.toDF(*column_names)
        return df

    def _read_files_in_subdir(self, files_with_suffix):
        dfs = []
        for file_path in files_with_suffix:
            df = self._read_file(file_path)
            dfs.append(df)
        return dfs

    def read(self, file_suffix: str) -> List[List[DataFrame]]:
        rooms = []
        tasks = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            for subdir, _, files in os.walk(self.data_path):
                files_with_suffix = [os.path.join(subdir, f) for f in files if f.endswith(file_suffix)]
                if files_with_suffix:
                    tasks.append(executor.submit(self._read_files_in_subdir, files_with_suffix))
            for task in tasks:
                dfs = task.result()
                if dfs:
                    rooms.append(dfs)
        return rooms

    """
    def read(self, file_suffix: str) -> List[List[DataFrame]]:
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
                    df.cache()
                    csv_files.append(df)
                    print("SubLento")
            print("MergeLentp")
            if len(csv_files) != 0:
                rooms.append(csv_files)
        return rooms
    """
