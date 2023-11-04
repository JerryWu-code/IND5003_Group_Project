import streamlit as st
import pandas as pd
import os
import tqdm
import requests
import pyarrow.parquet as pq
import geopandas as gpd
import geoplot as gplt
import geoplot.crs as gcrs
import numpy as np


class Data_loader:
    def __init__(self, raw_dir, output_dir, nyc_shapefile_dir):

        # rela_path = '{0}data/'.format(self.raw_dir.split('data/')[0])
        # path1 = rela_path + 'Location/Area_LatLong_Zipcode.csv'

        self.raw_dir = raw_dir
        self.output_dir = output_dir
        self.nyc_shapefile_dir = nyc_shapefile_dir
        self.api_key = None

    def raw_data_agg(self, time_range=None, export_raw=False):
        """
        Attention!!
        Whole data we've collected ranging from "2019-01_2023-07", you can't select data out of this range!!!
        Export and get the name of output file with the time_range label, and get the dataframe of the output.

        :param export_raw: whether you choose to export or not
        :param time_range: set the pick-up time_range of the data, and the default value is False(no filter)
        :return: tuple(output_dir, result)
                 output_dir: path of new_file
                 result: dataframe of the output in selected time_range
        """
        result = pd.DataFrame()
        file_lst = []

        whole_files = [sorted(files) for root, dirs, files in os.walk(self.raw_dir) if
                       any(fname.endswith('.parquet') for fname in files)][0]

        start_index = whole_files.index('green_tripdata_{}.parquet'.format(time_range.split('_')[0][:7]))
        end_index = whole_files.index('green_tripdata_{}.parquet'.format(time_range.split('_')[1][:7])) + 1

        run_files = whole_files[start_index:end_index]
        num_run_files = len(run_files)

        with tqdm.tqdm(total=num_run_files) as pbar:
            for file_name in run_files:
                if file_name.endswith('.parquet'):
                    file_lst.append(file_name)
                    path = self.raw_dir + file_name
                    data = pq.read_table(path).to_pandas()
                    result = pd.concat([result, data])
                    pbar.update(1)
        print("Finish loading raw data!")

        if not time_range:
            if export_raw:
                result.to_parquet(self.output_dir, index=False)
                print("Extract the data ranging from 2019-01-01 to 2023-07-31. \nOutput to this path: {0}".format(
                    self.output_dir))
        else:
            start = time_range.split("_")[0]
            end = time_range.split("_")[1]
            result = result[(result['lpep_pickup_datetime'] >= start) &
                            (end >= result['lpep_pickup_datetime'])].reset_index(drop=True)
            if export_raw:
                self.output_dir = "{}_{}.par{}".format(self.output_dir.split('.par')[0], time_range,
                                                       self.output_dir.split('.par')[1])
                result.to_parquet(self.output_dir, index=False)
                print("Extract the raw taxi data ranging from {0} to {1}. \nOutput to this path: {2}".format(
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

    def load_merged_geodata(self, df_new):
        df_new_borough = df_new[-(df_new['PU_Borough'] == 'EWR')].reset_index(drop=True).copy()
        nyc_boroughs = gpd.read_file(gplt.datasets.get_path('nyc_boroughs'))
        proj = gcrs.AlbersEqualArea(central_latitude=40.7128, central_longitude=-74.0059)

        zipcode_gdf = gpd.read_file(self.nyc_shapefile_dir)

        # group borough data
        df_group_area_zip = df_new_borough.groupby(by='PU_Zcode')[[
            'PU_Day_Count', 'PU_Day_Avg_Fare'
        ]].mean().reset_index()
        df_group_area_zip = df_group_area_zip.rename(columns={
            'PU_Day_Count': 'Frequency',
            'PU_Day_Avg_Fare': 'Fare'
        })
        df_merge_geo_zip = pd.merge(df_group_area_zip,
                                    zipcode_gdf,
                                    left_on='PU_Zcode',
                                    right_on='ZCTA5CE20',
                                    how='left').dropna(axis=0)

        # group zipcode data
        df_group_area_borough = df_new_borough.groupby(by='PU_Borough')[[
            'PU_Day_Count', 'PU_Day_Avg_Fare'
        ]].mean().reset_index()
        df_group_area_borough = df_group_area_borough.rename(columns={
            'PU_Day_Count': 'Frequency',
            'PU_Day_Avg_Fare': 'Fare'
        })
        df_merge_geo_borough = pd.merge(df_group_area_borough,
                                        nyc_boroughs,
                                        left_on='PU_Borough',
                                        right_on='BoroName',
                                        how='left')

        # tranform them into GeoDataFrame
        df_merge_geo_zip = gpd.GeoDataFrame(df_merge_geo_zip, geometry='geometry')
        df_merge_geo_borough = gpd.GeoDataFrame(df_merge_geo_borough, geometry='geometry')

        return df_merge_geo_zip, df_merge_geo_borough, proj, nyc_boroughs

    def get_final_processed_df(self, time_range, export_final=False):
        rela_path = '{0}data/'.format(self.raw_dir.split('data/')[0])
        # 1.Aggregate selected raw taxi data
        _, df = self.raw_data_agg(time_range=time_range, export_raw=False)
        df = df.drop(columns=['ehail_fee'])

        # 2.Merge location data
        path1 = rela_path + 'Location/Area_LatLong_Zipcode.csv'
        df_loc_new = pd.read_csv(path1)
        no_loc_con = ((df['PULocationID'].isin([264, 265])) |
                      (df['DOLocationID'].isin([264, 265])))
        df = df[-no_loc_con]
        df = pd.merge(df, df_loc_new, left_on='PULocationID', right_on='LocationID', how='left')
        df = df.rename(
            columns={'Borough': 'PU_Borough', 'Zone': 'PU_Zone', 'LatLong': 'PU_LatLong', 'Zipcode': 'PU_Zcode'})
        df = pd.merge(df, df_loc_new, left_on='DOLocationID', right_on='LocationID', how='left')
        df = df.rename(
            columns={'Borough': 'DO_Borough', 'Zone': 'DO_Zone', 'LatLong': 'DO_LatLong', 'Zipcode': 'DO_Zcode'})
        df = df.drop(columns=['LocationID_x', 'LocationID_y', 'PULocationID', 'DOLocationID'])

        # 3.Merge weather data
        path2 = rela_path + 'Weather/3503035.csv'
        df_weather = pd.read_csv(path2)
        df_weather = df_weather.loc[:, ['DATE', 'PRCP', 'TMAX', 'TMIN']]
        df_weather['AVG_T'] = (df_weather['TMAX'] + df_weather['TMIN']) / 2
        df_weather['TMIN'] = df_weather['TMIN'].apply(self.fahrenheit_to_celsius)
        df_weather['TMAX'] = df_weather['TMAX'].apply(self.fahrenheit_to_celsius)
        df_weather['AVG_T'] = df_weather['AVG_T'].apply(self.fahrenheit_to_celsius)
        df['DATE'] = df['lpep_pickup_datetime'].apply(lambda x: str(x)[:10])
        df = pd.merge(df, df_weather, on='DATE', how='left')

        df['PU_Day_Count'] = df.groupby(
            by=['DATE', 'PU_Zcode'])['VendorID'].transform('count')
        df['PU_Day_Avg_Fare'] = df.groupby(
            by=['DATE', 'PU_Zcode'])['total_amount'].transform(
            lambda x: round(np.average(x), 2))

        # 4.Add new features, rename and reorganize
        df_new = df[[
            'DATE', 'VendorID', 'lpep_pickup_datetime', 'lpep_dropoff_datetime',
            'store_and_fwd_flag', 'RatecodeID', 'passenger_count', 'trip_distance',
            'fare_amount', 'extra', 'mta_tax', 'tip_amount', 'tolls_amount',
            'improvement_surcharge', 'total_amount', 'payment_type', 'trip_type',
            'congestion_surcharge', 'PRCP', 'TMAX', 'TMIN', 'AVG_T', 'PU_Day_Count',
            'PU_Day_Avg_Fare', 'PU_Borough', 'DO_Borough', 'PU_Zone', 'DO_Zone',
            'PU_LatLong', 'DO_LatLong', 'PU_Zcode', 'DO_Zcode'
        ]].copy()
        df_new = df_new.rename(
            columns={
                'lpep_pickup_datetime': 'PU_time',
                'lpep_dropoff_datetime': 'DO_time',
                'trip_distance': 'distance',
                'PRCP': 'Rainfall'
            })
        df_new["PU_LatLong"] = df_new["PU_LatLong"].apply(eval)
        df_new["DO_LatLong"] = df_new["DO_LatLong"].apply(eval)

        # 5.A bit more processing for visualization
        df_new['trip_type'] = df_new['distance'].apply(lambda x: 'short' if x <= 10 else 'long')
        df_new['PU_time'] = pd.to_datetime(df_new['PU_time'])
        df_new['pickup_hour'] = df_new['PU_time'].dt.hour
        df_new['weekday'] = pd.to_datetime(df_new['DATE']).dt.dayofweek
        df_new['day_type'] = df_new['weekday'].apply(lambda x: 'Weekday' if x < 5 else 'Weekend')

        # Finally we just use df_new
        if export_final:
            print(self.output_dir)
            self.output_dir = "{}_{}_final.par{}".format(self.output_dir.split('.par')[0], time_range,
                                                         self.output_dir.split('.par')[1])
            df_new.to_parquet(self.output_dir, index=False)
            start = time_range.split("_")[0]
            end = time_range.split("_")[1]
            print("Extract the final merged data ranging from {0} to {1}. \nOutput to this path: {2}".format(
                start, end, self.output_dir))

        print("Finish loading the processed final data!")

        return df_new


if __name__ == "__main__":
    # Set path
    raw_dir = '../data/green_raw/'
    output_dir = '../data/green.parquet'
    nyc_shapefile_dir = '../data/NYC_Shapefile/NYC.shp'

    # Initialize a data_loader
    data_loader = Data_loader(raw_dir=raw_dir, output_dir=output_dir, nyc_shapefile_dir=nyc_shapefile_dir)

    # Set time range
    time_range = "2022-08-01_2023-07-31"
    # _, df_raw = data_loader.raw_data_agg(time_range=time_range, export_raw=True)
    df = data_loader.get_final_processed_df(time_range=time_range, export_final=False)

    df_merge_geo_zip, df_merge_geo_borough, proj, _ = data_loader.load_merged_geodata(df)
