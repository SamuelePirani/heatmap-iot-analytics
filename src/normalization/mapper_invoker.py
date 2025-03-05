from src.normalization.data_id_mapper import DataIdMarker, write_data

try:
    data_normalizer = DataIdMarker("data\IotData")
    csv_data = data_normalizer.read_data()
    write_data(csv_data)
except Exception as e:
    print(f"Error: {e}")
