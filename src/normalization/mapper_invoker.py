from src.normalization.data_id_mapper import Data_Id_Marker

try:
    data_normalizer = Data_Id_Marker("data\IotData")
    csv_data = data_normalizer.read_data()
    data_normalizer.write_data(csv_data)
except Exception as e:
    print(f"Error: {e}")
