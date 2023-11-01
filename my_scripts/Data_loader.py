import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
import os
import tqdm
import requests
import pyarrow.parquet as pq


class Data_loader:
    def __init__(self):
        self.raw_dir = 'data/green_raw/'
        self.output_dir = 'data/green_sum.parquet'
        self.api_key = None

    def raw_data_agg(self, time_range=False):
        """
        Attention!!
        Whole data we've collected ranging from "2019-01_2023-07", you can't select data out of this range!!!
        Export and get the name of output file with the time_range label, and get the dataframe of the output.

        :param time_range: set the pick-up time_range of the data, and the default value is False(no filter)
        :return: tuple(output_dir, result)
                 output_dir: path of new_file
                 result: dataframe of the output in selected time_range
        """
        result = pd.DataFrame()
        file_lst = []

        total_files = sum(
            [len(files) for root, dirs, files in os.walk(self.raw_dir) if
             any(fname.endswith('.parquet') for fname in files)])
        with tqdm.tqdm(total=total_files) as pbar:
            for root, dirs, files in os.walk(self.raw_dir):
                for file_name in files:
                    if file_name.endswith('.parquet'):
                        file_lst.append(file_name)
                        path = self.raw_dir + file_name
                        data = pq.read_table(path).to_pandas()
                        result = pd.concat([result, data])
                        pbar.update(1)

        if not time_range:
            result.to_parquet(self.output_dir, index=False)
        else:
            start = time_range.split("_")[0]
            end = time_range.split("_")[1]
            self.output_dir = self.output_dir.split('.')[0] + "_{}.".format(time_range) + self.output_dir.split('.')[1]
            result = result[(result['lpep_pickup_datetime'] >= start) &
                            (end >= result['lpep_pickup_datetime'])].reset_index(drop=True)
            result.to_parquet(self.output_dir, index=False)

        print("Extract the data ranging from {0} to {1}. \nOutput to this path: {2}".format(
            start, end, self.output_dir))

        return self.output_dir, result

    # noinspection PyAttributeOutsideInit
    def set_google_api(self, api_key):
        self.api_key = api_key

    def fahrenheit_to_celsius(self, fahrenheit):
        celsius = (fahrenheit - 32) * 5 / 9
        return round(celsius, 1)

    def get_address(self, name):
        address = name + ', New York'
        url = 'https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}'.format(address, self.api_key)
        response = requests.get(url)
        data = response.json()

        if data['status'] == 'OK':
            latitude = data['results'][0]['geometry']['location']['lat']
            longitude = data['results'][0]['geometry']['location']['lng']
            return latitude, longitude
        else:
            print('Can\'t find {}.'.format(name))
            return None, None

    def LatLong_to_Zipcode(self, LatLong):
        lat = LatLong[0]
        lng = LatLong[1]
        base_url = "https://maps.googleapis.com/maps/api/geocode/json?latlng={0},{1}&sensor=true&key={2}".format(
            lat, lng, self.api_key)
        response = requests.get(base_url)
        data = response.json()
        postal_code = next((item['long_name']
                            for item in data['results'][0]['address_components']
                            if 'postal_code' in item['types']), None)
        return postal_code


if __name__ == "__main__":
    # Aggregate raw data to a time-ranged file
    data_loader = Data_loader()
    time_range = "2022-01-01_2023-07-31"
    new_file_dir = data_loader.raw_data_agg(time_range)

    # Preprocessing

    # Visualization

    # Prediction
