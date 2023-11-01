import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re


class Data_loader:
    def __init__(self):
        pass

    def raw_data_agg(self, raw_dir, output_dir, time_range=False):  # from "2019-01_2023-07"
        """
        :param raw_dir: set the raw data directory
        :param output_dir: set the output file directory and front-part name
        :param time_range: set the time_range of the data, and the default value is False(no filter)
        :return: path of new_file: export and get the name of output file with the time_range label
        """
        result = pd.DataFrame()
        file_lst = []

        for root, dirs, files in os.walk(raw_dir):
            for file_name in files:
                if file_name.endswith('.parquet'):
                    file_lst.append(file_name)
                    path = raw_dir + file_name
                    data = pq.read_table(path).to_pandas()
                    result = pd.concat([result, data])

        if not time_range:
            result.to_parquet(output_dir, index=False)
        else:
            start = time_range.split("_")[0]
            end = time_range.split("_")[1]
            output_dir = output_dir + "_{}".format(time_range)
            df = data[(data['lpep_pickup_datetime'] >= start) &
                      (end >= data['lpep_pickup_datetime'])].reset_index(drop=True)
            df.to_parquet(output_dir, index=False)

        return output_dir


class Preprocessing:
    def __init__(self):
        pass


class Visualization:
    def __init__(self):
        pass


class Prediction:
    def __init__(self):
        pass


if __name__ == "__main__":
    # Aggregate raw data to a time-ranged file
    data_loader = Data_loader()
    raw_dir = 'data/green_raw/'
    output_dir = 'data/green_sum.parquet'
    time_range = "2022-01_2023-07"
    new_file_dir = data_loader.raw_data_agg(raw_dir, output_dir, time_range)

    # Preprocessing

    # Visualization

    # Prediction
