import datetime
from typing import List

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col, from_unixtime, to_date, avg, min, max, window


class CO2Analyzer:

    def __init__(self, spark: SparkSession, reader):
        self.spark = spark
        self.csv_dataframes: List[DataFrame] = reader.read("co2.csv")

    def prepare_dataframe(self, df: DataFrame) -> DataFrame:
        return df.withColumn("Timestamp", from_unixtime(col("Timestamp")).cast("timestamp"))

    def extract_unique_days(self, df: DataFrame) -> List[datetime.date]:
        df_with_day = df.withColumn("day", to_date(col("Timestamp")))
        return [row["day"] for row in df_with_day.select("day").distinct().collect()]

    def aggregate_by_15min_windows(self, df: DataFrame) -> DataFrame:
        return (df.groupBy(window(col("Timestamp"), "15 minutes")).agg(avg("Value_co2").alias("average_value"),
                                                                       min("Value_co2").alias("minimum_value"),
                                                                       max("Value_co2").alias("maximum_value")).orderBy(
            "window"))

    def run_analysis(self):
        for raw_df in self.csv_dataframes:
            prepared_df = self.prepare_dataframe(raw_df)
            for day in self.extract_unique_days(prepared_df):
                day_str = day.strftime("%Y-%m-%d")
                print(f"Aggregating data for {day_str}")
                # Filter records for the specific day
                filtered_df = prepared_df.filter(to_date(col("Timestamp")) == day)
                aggregated_df = self.aggregate_by_15min_windows(filtered_df)
                aggregated_df.show(truncate=False)
