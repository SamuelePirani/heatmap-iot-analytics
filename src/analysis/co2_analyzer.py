import datetime
from typing import List
from functools import reduce
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col, from_unixtime, to_date, avg, min, max, window, mean
from src.analysis.analysis_preprocessor import Analysis_PreProcessor


class CO2Analyzer:

    def __init__(self, spark: SparkSession, reader):
        self.spark = spark
        self.csv_dataframes: List[DataFrame] = reader.read(".csv")

    def extract_unique_days(self, df: DataFrame) -> List[datetime.date]:
        df_with_day = df.withColumn("day", to_date(col("Timestamp")))
        return [row["day"] for row in df_with_day.select("day").distinct().collect()]

    def aggregate_by_15min_windows(self, dfs):
        intermediate = []
        for df in dfs:
                value_column = next((col_name for col_name in df.columns if col_name.startswith("Value_")), None)
                risultati_15_min = df.groupBy(
                    col("ID_Room"),
                    window(col("Timestamp"), "30 minutes"))\
                .agg(
                    mean(value_column).alias("media_15_min"),
                    min(value_column).alias("min_15_min"),
                    max(value_column).alias("max_15_min")
                )
                risultati_15_min = risultati_15_min.orderBy("window")
                intermediate.append(risultati_15_min)
        result = reduce(lambda df_left, df_right: df_left.join(df_right, on=["ID_Room", "window"], how="outer"), intermediate)
        result.show(truncate=False)

    def run_analysis(self):
        prepocessor = Analysis_PreProcessor(self.spark)
        for dfs in self.csv_dataframes:
            prepared_dfs = prepocessor.run_preprocess(dfs)
            self.aggregate_by_15min_windows(prepared_dfs)

            """
            for raw_df in self.csv_dataframes:
            prepared_df = self.prepare_dataframe(raw_df)
            for day in self.extract_unique_days(prepared_df):
                day_str = day.strftime("%Y-%m-%d")
                print(f"Aggregating data for {day_str}")
                # Filter records for the specific day
                filtered_df = prepared_df.filter(to_date(col("Timestamp")) == day)
                aggregated_df = self.aggregate_by_15min_windows(filtered_df)
                aggregated_df.show(truncate=False)
                """
