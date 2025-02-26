from functools import reduce
import os
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("HeatMapJob").getOrCreate()

try:
    os.system("python Python-DataNormalizer\Main.py")
    csv_file = spark.createDataFrame([])
    for subdir, dirs, files in os.walk("Data\IotData"):
        for file in files:
            if file.endswith(".csv"):
                path_name = os.path.join(subdir, file)
                csv_file = csv_file.append(spark.read.csv(path_name, header=False, inferSchema=True))
                csv_file.show()
            

except Exception as e:
    print(f"Error: {e}")
finally:
    spark.stop()



