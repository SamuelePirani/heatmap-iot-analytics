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


def aggregate_by_minute_window(dfs: List[DataFrame], minutes: int):
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
    return result


def store_single_geojson_to_db(rooms_map, floor, mongo_client, data_path):
    logger.info(f"Creating {floor} GeoJSON")
    path = data_path + f"/{floor}.geojson"
    with open(path, "r") as f:
        geojson_data = load(f)
        for feature in geojson_data["features"]:
            if not feature["geometry"]["type"] == "Point":
                continue
            room_id = feature["properties"]["room_id"]
            logger.info("\tRoom ID: " + str(room_id))
            dfs = rooms_map[room_id]
            feature["properties"]["data"] = []
            for i in range(0, 2):
                feature["properties"]["data"].append(
                    {
                        '30' if i == 0 else '60': dfs[i].drop("Id_Room").toJSON().collect()
                    }
                )
                logger.info(f"\t\tInterval {30 if i == 0 else 60} for room {room_id} has been added to geojson")
    logger.info("Geojson for " + floor + " has been created")
    db = mongo_client["geojson_db"]
    collection = db[f"{floor}_geojson"]

    collection.delete_many({})
    collection.insert_one({"type": "FeatureCollection", "features": geojson_data["features"]})

    logger.info(f"GeoJSON for {floor} successfully saved to MongoDB")


def store_geojson_to_db(rooms_map, mongo_client, data_path):
    store_single_geojson_to_db(rooms_map, 'FirstFloor', mongo_client, data_path)
    store_single_geojson_to_db(rooms_map, 'SecondFloor', mongo_client, data_path)


def update_rooms_to_analyze(rooms_to_analyze, geojson_filename):
    with open(f'./data/geojson/{geojson_filename}', "r") as f:
        geojson_data = load(f)
        for feature in geojson_data["features"]:
            if not feature["geometry"]["type"] == "Point":
                continue
            rooms_to_analyze.append(feature["properties"]["room_id"])
    f.close()
    return rooms_to_analyze


class Analyzer:
    def __init__(self, reader) -> None:
        self.dataframe_groups: List[List[DataFrame]] = reader.read(".csv")

    def run_analysis(self, intervals: List[int], client, data_path) -> None:
        self.dataframe_groups = run_preprocess(self.dataframe_groups)
        rooms_to_analyze = []
        rooms_to_analyze = update_rooms_to_analyze(
            update_rooms_to_analyze(rooms_to_analyze, 'FirstFloor.geojson'),
            'SecondFloor.geojson'
        )
        d = dict()
        for group in self.dataframe_groups:
            if group[0].select("Id_Room").first()["Id_Room"] not in rooms_to_analyze:
                continue
            windows = []
            room_id = None
            for interval in intervals:
                aggregated = aggregate_by_minute_window(group, interval)
                if not room_id:
                    room_id = aggregated.first()["Id_Room"]
                windows.append(aggregated)
            d[room_id] = windows
        logger.info("Updating geojson with analyzed data")
        store_geojson_to_db(d, client, data_path)
