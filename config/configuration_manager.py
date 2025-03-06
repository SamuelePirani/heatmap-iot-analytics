import os
import yaml
import threading

class SingletonMeta(type):
    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]

class ConfigurationManager(metaclass=SingletonMeta):

    def __init__(self, file_path):
        self.config_file = None
        self.config_path = file_path


    def setup_data_path_user(self):
        new_config = self.get_config()

        iot_datapath = os.path.join(os.getcwd(), new_config["base_path"]["iot_data_root"])
        geojson_datapath = os.path.join(os.getcwd(), new_config["base_path"]["geoJson_data_root"])

        new_config["config_datapath"]["iot_data"] = iot_datapath
        new_config["config_datapath"]["geoJson_data"] = geojson_datapath

        self.update_config(new_config)
    
    def get_config(self):
        if self.config_file is None:
            self.read_config(self.config_path)
        return self.config_file

    def read_config(self, file_path):
       with open(file_path, 'r') as file:
            self.config_file = yaml.safe_load(file)

    def update_config(self, new_config):
        with open(self.config_path, 'w') as file:
            yaml.dump(new_config, file, default_flow_style=False, sort_keys=False)
        self.config_file = new_config