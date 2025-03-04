from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import col, from_unixtime, to_date, avg, min, max, date_format

class Analysis_PreProcessor(object):
    
    def __init__(self, spark):
        self.spark = spark

    def prepare_dataframe(self, df: DataFrame) -> DataFrame:
        return df.withColumn("Timestamp", from_unixtime(col("Timestamp")).cast("timestamp"))

    def prepare_datetime_column(self, df: DataFrame) -> DataFrame:
        df = self.prepare_dataframe(df)
        df = df.withColumn("Day", date_format(col("Timestamp"), "dd-MM-yyyy"))
        df = df.withColumn("Rilevation_Time", date_format(col("Timestamp"), "HH:mm:ss"))
        df = df.drop("Timestamp")
        return df

