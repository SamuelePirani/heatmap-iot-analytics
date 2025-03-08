import os
import threading
from typing import Any, Dict

import yaml


class ConfigurationManager:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self.config: Dict[str, Any] = {}
        self._lock = threading.RLock()

    def load_config(self) -> Dict[str, Any]:
        with self._lock:
            with open(self.file_path) as file:
                self.config = yaml.safe_load(file)
            return self.config

    def save_config(self) -> None:
        with self._lock:
            with open(self.file_path, "w") as file:
                yaml.dump(self.config, file, sort_keys=False)

    def configure_data_paths(self) -> Dict[str, Any]:
        with self._lock:
            if not self.config:
                self.load_config()

            base_path = self.config.get("base_path", {})
            iot_data = os.path.join(os.getcwd(), base_path.get("iot_data_root", ""))
            geojson_data = os.path.join(os.getcwd(), base_path.get("geoJson_data_root", ""))

            self.config.setdefault("config_datapath", {})
            self.config["config_datapath"]["iot_data"] = iot_data
            self.config["config_datapath"]["geoJson_data"] = geojson_data

            self.save_config()
            return self.config

    # def get_config(self) -> Dict[str, Any]:
    #     with self._lock:
    #         if not self.config:
    #             self.load_config()
    #         return self.config
