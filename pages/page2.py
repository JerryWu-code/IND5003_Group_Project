import pyarrow.parquet as pq
data_path = './data/green_sum_2022-01-01_2023-07-31_final.parquet'

data = pq.read_table(data_path).to_pandas()
# print(data)