from src.normalization.data_normalizer import DataNormalizer

try:
    data_normalizer = DataNormalizer("data\IotData")
    csv_data = data_normalizer.read_data()
    data_normalizer.write_data(csv_data)
except Exception as e:
    print(f"Error: {e}")
