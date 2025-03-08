import logging
from functools import reduce
from typing import List
from pyspark.sql import DataFrame
from pyspark.sql.functions import col, min, max, window, mean, round
from concurrent.futures import ThreadPoolExecutor
from src.analysis.analysis_preprocessor import run_preprocess

logger = logging.getLogger(__name__)
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)


def aggregate_single_dataframe(df: DataFrame, minutes: int) -> DataFrame:
    value_columns = [col_name for col_name in df.columns if col_name.startswith("Value_")]
    if not value_columns:
        raise ValueError("No valid value columns found in the DataFrame.")

    agg_expressions = []
    for value_column in value_columns:
        base_name = value_column.split("_")[1]
        agg_expressions.extend([
            round(mean(value_column), 3).alias(f"{base_name}_mean"),
            min(value_column).alias(f"{base_name}_min"),
            max(value_column).alias(f"{base_name}_max")
        ])

    agg_df = df.groupBy(
        col("Id_Room"),
        window(col("timestamp"), f"{minutes} minutes")
    ).agg(*agg_expressions)

    return agg_df.withColumn("Start", col("window.start")).withColumn("End", col("window.end")).drop("window")

def aggregate_by_minute_window(dfs: List[DataFrame], minutes: int):
    logger.info(f"Start aggregation for {minutes} minute window - Room {dfs[0].select('ID_Room').first()}")
    aggregated_list = []

    # Usa il ThreadPoolExecutor per parallelizzare l'aggregazione di ogni DataFrame
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(aggregate_single_dataframe, df, minutes) for df in dfs]
        for future in futures:
            try:
                aggregated_list.append(future.result())
            except Exception as e:
                logger.warning(f"Error during aggregation: {e}")

    # Unisci tutti i risultati
    if not aggregated_list:
        raise ValueError("No aggregations were performed due to errors or invalid data.")
    result = reduce(lambda left, right: left.join(right, on=["Id_Room", "Start", "End"], how="outer"), aggregated_list)
    logger.info(f"Aggregation for {minutes} minutes - Complete")
    return result

    """"
    aggregated_list = []
    logger.info(f"Start aggregation for {minutes} minute window - Room {dfs[0].select('ID_Room').first()}")
    for df in dfs:
        value_column = next((col_name for col_name in df.columns if col_name.startswith("Value_")), None)
        if not value_column:
            logger.warning("No value column found in one of the dataframes; skipping aggregation for this DataFrame.")
            continue
        agg_df = df.groupBy(col("ID_Room"), window(col("Timestamp"), f"{minutes} minutes")).agg(
            round(mean(value_column), 3).alias(value_column.split("_")[1] + " mean"),
            min(value_column).alias(value_column.split("_")[1] + " min"),
            max(value_column).alias(value_column.split("_")[1] + " max")).orderBy("window")
        aggregated_list.append(agg_df)
    if not aggregated_list:
        raise ValueError("Aggregation could not be performed because no valid value columns were found.")
    result = reduce(lambda left, right: left.join(right, on=["ID_Room", "window"], how="outer"), aggregated_list)
    result = result.withColumn("Start", col("window.start")).withColumn("End", col("window.end")).drop("window")
    column_order = ["ID_Room", "Start", "End"] + [c for c in result.columns if c not in ["ID_Room", "Start", "End"]]
    logger.info(f"Aggregation for {minutes} minutes - Complete")
    return result.select(*column_order)
    """""


class Analyzer:
    def __init__(self, reader) -> None:
        self.dataframe_groups: List[List[DataFrame]] = reader.read(".csv")

    def run_analysis(self, intervals: List[int]) -> None:
        self.dataframe_groups = run_preprocess(self.dataframe_groups)
        for group in self.dataframe_groups:
            for interval in intervals:
                try:
                    aggregated_df = aggregate_by_minute_window(group, interval)
                except Exception as e:
                    logger.error(f"Error aggregating data for interval {interval} minutes: {e}")
