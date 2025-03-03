import os
import sys
import yaml

ROOT = sys.path[1]
print(ROOT)

config_file_path = os.path.join(ROOT, "config.yml")

with open(config_file_path) as file:
    config = yaml.safe_load(file)

config["iot_data_path"] = os.path.join(ROOT, config["iot_data_path"])


class SparkDataReader(object):
    def __init__(self, spark):
        self.spark_session = spark


    def read(self, csv_to_read):
        csv_files = []
        for subdir, dirs, files in os.walk(config["iot_data_path"]):
            for f in files:
                if f.endswith(csv_to_read):
                    path_name = os.path.join(subdir, f)
                    df = self.spark_session.read.csv(path_name, header=False, inferSchema=True)
                    column_names = ["ID_Room", f"Timestamp", f"Value_{os.path.splitext(f)[0]}"]
                    df = df.toDF(*column_names)
                    csv_files.append(df)
        return csv_files
