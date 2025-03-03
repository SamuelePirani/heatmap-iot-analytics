import os
import yaml

# Open config.yaml, in order to obtain the iot data path
with open("config.yml", "r") as file:
    config = yaml.safe_load(file)

class SparkDataRader(object):
    def __init__(self, spark):
        self.spark_session = spark

    #Read data based on the name provided by the sender class
    def read(self, csv_to_read):
        csv_files = []
        for subdir, dirs, files in os.walk(config["iot_data_path"]):
            for file in files:
                if file.endswith(csv_to_read):
                    path_name = os.path.join(subdir, file)
                    df = self.spark_session.read.csv(path_name, header=False, inferSchema=True)
                    column_names = ["ID_Room", f"Timestamp",
                                f"Value_{os.path.splitext(file)[0]}"]
                    df = df.toDF(*column_names)
                    csv_files.append(df)
        return csv_files