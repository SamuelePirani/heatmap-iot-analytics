from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import col, from_unixtime, to_date, avg, min, max, date_format

class Analysis_PreProcessor(object):
    
    def __init__(self, spark):
        self.spark = spark

    def convert_timestamp_field(self, df: DataFrame) -> DataFrame:
        return df.withColumn("Timestamp", from_unixtime(col("Timestamp")).cast("timestamp"))

    def prepare_datetime_column(self, df: DataFrame) -> DataFrame:
        df = df.withColumn("Day", date_format(col("Timestamp"), "dd-MM-yyyy"))
        df = df.withColumn("Rilevation_Time", date_format(col("Timestamp"), "HH:mm:ss"))
        df = df.drop("Timestamp")
        return self.order_column_dataframe(df)

    def order_column_dataframe(self, df) -> DataFrame:
        value_name = next((col_name for col_name in df.columns if col_name.startswith("Value_")), None)
        order_columns = ["ID_Room", "Day", "Rilevation_Time", value_name]
        return df.select(order_columns)

    def run_preprocess(self, dfs):
        prepared_dfs = []
        for df in dfs:
            df = self.convert_timestamp_field(df)
            prepared_dfs.append(df)
        return prepared_dfs