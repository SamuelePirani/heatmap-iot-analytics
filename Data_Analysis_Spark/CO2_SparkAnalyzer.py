from pyspark.sql.functions import col, from_unixtime, to_date, avg, min, max, window
from pyspark.sql import SparkSession


class CO2_Analyzer(object):
    
    def __init__(self, spark, reader):
        self.spark_session = spark
        self.csv_dfs = reader.read("co2.csv")

    def prepare_data(self, df):
        return df.withColumn("Timestamp", from_unixtime(col("Timestamp")).cast("timestamp"))

    def extract_day(self, df):
        df = df.withColumn("day", to_date(col("Timestamp")))
        return df.select("day").distinct().collect()


    def run_analysis(self):
        self.csv_dfs = [self.prepare_data(df) for df in self.csv_dfs]
        for file in self.csv_dfs:
            for day in self.extract_day(file):
                day_str = day["day"].strftime("%Y-%m-%d")  # Converti il giorno in stringa

                # Filtra per il giorno specifico
                df_day = file.filter(to_date(col("Timestamp")) == day["day"])

                # Aggregazione per intervallo di 15 minuti
                df_15min = df_day.groupBy(window(col("Timestamp"), "15 minutes")) \
                .agg(
                avg("Value_co2").alias("Average value"),
                min("Value_co2").alias("Minimum value"),
                max("Value_co2").alias("Maximum value")
                )\
                .orderBy("window")
                df_15min.show(truncate=False)
               





