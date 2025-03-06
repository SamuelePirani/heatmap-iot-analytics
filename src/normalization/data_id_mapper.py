import os

import pandas as pd


def check_column(file, id_num):
    return id_num in file.columns


def write_data(data_files):
    for path_csv in data_files:
        df = pd.read_csv(path_csv)
        id_num = os.path.basename(os.path.dirname(path_csv))
        if not check_column(df, id_num):
            df.insert(0, id_num, id_num)
            df.to_csv(path_csv, index=False)
            print(f"Document: [{path_csv}] - Operation Success")
        else:
            print(f"Document: [{path_csv}] - Already normalized")


class DataIdMarker:
    def __init__(self, rootFolder):
        self.rootFolder = rootFolder

    def read_data(self):
        csv_files = []
        for subdir, dirs, files in os.walk(self.rootFolder):
            for file in files:
                if file.endswith(".csv"):
                    file_path = os.path.join(subdir, file)
                    csv_files.append(file_path)
        return csv_files
