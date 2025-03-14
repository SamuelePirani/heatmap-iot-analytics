import logging
from functools import reduce
from typing import List
from pyspark.sql import DataFrame
from pyspark.sql.functions import col, min, max, window, mean, round
from concurrent.futures import ThreadPoolExecutor
from src.analysis.analysis_preprocessor import run_preprocess
from geojson import load

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
    return (agg_df.withColumn("Start", col("window.start"))
            .withColumn("End", col("window.end")).drop("window"))


def aggregate_by_minute_window(dfs: List[DataFrame], minutes: int, room_map):
    logger.info(f"Start aggregation for {minutes} minute window - Room {dfs[0].select('ID_Room').first()}")
    aggregated_list = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(aggregate_single_dataframe, df, minutes) for df in dfs]
        for future in futures:
            try:
                aggregated_list.append(future.result())
            except Exception as e:
                logger.warning(f"Error during aggregation: {e}")
    if not aggregated_list:
        raise ValueError("No aggregations were performed due to errors or invalid data.")
    result = reduce(lambda left, right: left.join(right, on=["Id_Room", "Start", "End"], how="outer"), aggregated_list)
    logger.info(f"Aggregation for {minutes} minutes is completed")
    try:
        result = result.withColumn("Id_Room", col("Id_Room").cast("string"))
        result = result.replace(room_map, subset=['Id_Room'])
    except Exception as e:
        logger.error(f"Error during room name replacement: {e}")
    return result


def update_rooms_to_analyze(rooms_to_analyze, room_map, geojson_filename):
    with open(f'./data/geojson/{geojson_filename}', "r") as f:
        geojson_data = load(f)
        for feature in geojson_data["features"]:
            if not feature["geometry"]["type"] == "Point":
                continue
            hotel_room = feature["properties"]["hotel_room_id"]
            room_map[str(hotel_room)] = feature['properties']['room']
            rooms_to_analyze.add(hotel_room)
        f.close()
    return rooms_to_analyze, room_map


def save_to_mongodb(intervals_analyzed, client):
    db = client.sensor_analysis
    logger.info("Starting MongoDB insertion")

    for interval, dataframes in intervals_analyzed.items():
        collection = db[f"interval_{interval}"]
        documents = []

        logger.info(f"Processing interval: {interval}")

        for dataframe in dataframes:
            rows = dataframe.collect()
            for row in rows:
                entry = {
                    "start": row["Start"],
                    "end": row["End"],
                    "room_name": row["Id_Room"],
                    "sensors": []
                }

                for sensor in ["co2", "humidity", "light", "pir", "temperature"]:
                    mean_key, min_key, max_key = f"{sensor}_mean", f"{sensor}_min", f"{sensor}_max"
                    if row[mean_key] is not None:
                        entry["sensors"].append({
                            "type": sensor,
                            "mean": row[mean_key],
                            "min": row[min_key],
                            "max": row[max_key]
                        })

                documents.append(entry)

        if documents:
            collection.insert_many(documents)
            logger.info(f"Inserted {len(documents)} documents for interval {interval} into MongoDB")

    logger.info("Finished MongoDB insertion")


class Analyzer:
    def __init__(self, reader) -> None:
        self.dataframe_groups: List[List[DataFrame]] = reader.read(".csv")

    def run_analysis(self, intervals: List[int], client) -> None:
        self.dataframe_groups = run_preprocess(self.dataframe_groups)
        rooms_to_analyze, room_map = update_rooms_to_analyze(
            set(),
            dict(),
            'FirstFloor.geojson'
        )
        rooms_to_analyze, room_map = update_rooms_to_analyze(
            rooms_to_analyze,
            room_map,
            'SecondFloor.geojson'
        )
        intervals_analyzed = dict()
        for interval in intervals:
            intervals_analyzed[interval] = []
        for group in self.dataframe_groups:
            if group[0].select("Id_Room").first()["Id_Room"] not in rooms_to_analyze:
                continue
            for interval in intervals:
                aggregated = aggregate_by_minute_window(group, interval, room_map)
                intervals_analyzed[interval].append(aggregated)
        save_to_mongodb(intervals_analyzed, client)
