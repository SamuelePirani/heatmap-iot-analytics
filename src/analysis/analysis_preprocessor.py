from pyspark.sql import DataFrame
from pyspark.sql.functions import col, from_unixtime


def convert_timestamp_field(df: DataFrame) -> DataFrame:
    return df.withColumn("Timestamp", from_unixtime(col("Timestamp")).cast("timestamp"))


def run_preprocess(dfs):
    prepared_dfs = []
    for df in dfs:
        df = convert_timestamp_field(df)
        prepared_dfs.append(df)
    return prepared_dfs
