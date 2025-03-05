from typing import List
from functools import reduce
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col, min, max, window, mean, round
from src.analysis.analysis_preprocessor import run_preprocess


def aggregate_by_15min_windows(dfs):
    intermediate = []
    for df in dfs:
        value_column = next((col_name for col_name in df.columns if col_name.startswith("Value_")), None)
        results_30_minutes = df.groupBy(
            col("ID_Room"),
            window(col("Timestamp"), "30 minutes")) \
            .agg(
            round(mean(value_column), 3).alias(value_column.split("_")[1] + " mean"),
            min(value_column).alias(value_column.split("_")[1] + " min"),
            max(value_column).alias(value_column.split("_")[1] + " max")
        )
        results_30_minutes = results_30_minutes.orderBy("window")
        intermediate.append(results_30_minutes)
    result = reduce(lambda df_left, df_right: df_left.join(df_right, on=["ID_Room", "window"], how="outer"),
                    intermediate)
    result = result.withColumn("Start", col("window.start")) \
        .withColumn("End", col("window.end")) \
        .drop("window")
    column_order = ["ID_Room", "Start", "End"] + [c for c in result.columns if
                                                  c not in ["ID_Room", "Start", "End"]]
    result = result.select(*column_order)
    result.show(truncate=False)


class CO2Analyzer:

    def __init__(self, spark: SparkSession, reader):
        self.spark = spark
        self.csv_dataframes: List[DataFrame] = reader.read(".csv")

    def run_analysis(self):
        for dfs in self.csv_dataframes:
            prepared_dfs = run_preprocess(dfs)
            aggregate_by_15min_windows(prepared_dfs)
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
