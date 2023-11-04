import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
from my_scripts import ts, Data_loader


class Time_series_analysis:
    def __init__(self, df, whole_time, if_st=True):
        self.whole_time = whole_time
        self.data = df
        self.df_counts, self_df_fare = self.load_time_series_data(whole_time)

        pass

    def load_time_series_data(self):
        start = time_range.split("_")[0]
        end = time_range.split("_")[1]
        dt = self.data[(self.data['DATE'] >= start) & (self.data['DATE'] <= end)].reset_index(drop=True)
        dt['PU_Day_Count'] = dt.groupby(
            by=['DATE', 'PU_Borough'])['VendorID'].transform('count')
        dt['PU_Day_Avg_Fare'] = dt.groupby(
            by=['DATE', 'PU_Borough'])['total_amount'].transform(
            lambda x: round(np.average(x), 2))

        return df_counts, df_fare

    def plot_time_series(self):
        pass

    def plot_time_series_with_seasonal_decomposition_with_trend_with_seasonality_adjustment(self):
        pass


if __name__ == '__main__':
    raw_dir = '../data/green_raw/'
    output_dir = '../data/green.parquet'
    nyc_shapefile_dir = '../data/NYC_Shapefile/NYC.shp'
    time_range = '2023-01-01_2023-07-31'

    # Initialize a data_loader
    data_loader = Data_loader.Data_loader(raw_dir=raw_dir, output_dir=output_dir,
                                          nyc_shapefile_dir=nyc_shapefile_dir)
    # Get the data
    df = data_loader.get_final_processed_df(time_range=time_range, export_final=False)

    # Set the period to analyze
    ts_ana_period = '2023-06-01_2023-07-31'
    time_ana = Time_series_analysis(whole_time=ts_ana_period, if_st=False)

