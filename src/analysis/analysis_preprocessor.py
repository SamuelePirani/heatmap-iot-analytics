from pyspark.sql import DataFrame
from pyspark.sql.functions import col, from_unixtime


def convert_timestamp_field(df: DataFrame) -> DataFrame:
    return df.withColumn("Timestamp", from_unixtime(col("Timestamp")).cast("timestamp"))


def run_preprocess(rooms):
    for i, dfs in enumerate(rooms):
        for j, df in enumerate(dfs):
            rooms[i][j] = convert_timestamp_field(df)
    return rooms
