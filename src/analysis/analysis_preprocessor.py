from typing import List

from pyspark.sql import DataFrame
from pyspark.sql.functions import col, from_unixtime


def convert_timestamp_field(df: DataFrame) -> DataFrame:
    return df.withColumn("Timestamp", from_unixtime(col("Timestamp")).cast("timestamp"))


def run_preprocess(rooms: List[List[DataFrame]]) -> List[List[DataFrame]]:
    return [[convert_timestamp_field(df) for df in group] for group in rooms]
