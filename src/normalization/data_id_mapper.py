import logging
import os

import pandas as pd

logger = logging.getLogger(__name__)


class DataIdMapper:
    def __init__(self, root_folder: str) -> None:
        self.root_folder = root_folder

    @staticmethod
    def _has_id_column(df: pd.DataFrame, id_num: str) -> bool:
        return id_num in df.columns

    def _normalize_file(self, file_path: str) -> None:
        try:
            df = pd.read_csv(file_path)
            id_num = os.path.basename(os.path.dirname(file_path))
            if not self._has_id_column(df, id_num):
                df.insert(0, id_num, id_num)
                df.to_csv(file_path, index=False)
                logger.info(f"Normalized file: {file_path}")
            else:
                logger.info(f"File already normalized: {file_path}")
        except Exception as e:
            logger.error(f"Error normalizing file {file_path}: {e}")
            raise

    def read_csv_files(self) -> list:
        csv_files = []
        for subdir, _, files in os.walk(self.root_folder):
            for file in files:
                if file.endswith(".csv"):
                    csv_files.append(os.path.join(subdir, file))
        return csv_files

    def normalize_all(self) -> None:
        csv_files = self.read_csv_files()
        if not csv_files:
            logger.warning(f"No CSV files found under {self.root_folder}")
            return

        for file_path in csv_files:
            self._normalize_file(file_path)
