from functools import reduce
import os
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_unixtime, col

spark = SparkSession.builder.appName("HeatMapJob").getOrCreate()

try:
    #os.system("python Python-DataNormalizer\Main.py")
    csv_files = []
    result = []
    for subdir, dirs, files in os.walk("Data\IotData"):
        for file in files:
            if file.endswith(".csv"):
                path_name = os.path.join(subdir, file)
                df = spark.read.csv(path_name, header=False, inferSchema=True)
                column_names = ["ID_Room", f"TimeStamp_{os.path.splitext(file)[0]}", f"Value_{os.path.splitext(file)[0]}"]
                df = df.toDF(*column_names)
                csv_files.append(df)
        if len(csv_files) != 0:
            cobiner = csv_files[0]
            for csv in csv_files[1:]:
                cobiner = cobiner.join(csv, on="ID_Room", how='inner')
            csv_files = []
            result.append(cobiner)
    result[0].printSchema()
except Exception as e:
    print(f"Error: {e}")
finally:
    spark.stop()




