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
        url = f'https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={self.api_key}'
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
        base_url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lng}&sensor=true&key={self.api_key}"
        response = requests.get(base_url)
        data = response.json()
        postal_code = next((item['long_name']
                            for item in data['results'][0]['address_components']
                            if 'postal_code' in item['types']), None)
        return postal_code


class Preprocessing:
    def __init__(self):
        pass


class Visualization:
    def __init__(self):
        pass
        
    def plot_top_zones(self, data_path):
        data = pq.read_table(data_path).to_pandas()
        
        # Top 10 pickup zones
        top_pickup_zones = data['PU_Zone'].value_counts().head(10)

        # Top 10 dropoff zones
        top_dropoff_zones = data['DO_Zone'].value_counts().head(10)

        plt.figure(figsize=(14, 6))

        # Plotting the top pickup zones
        plt.subplot(1, 2, 1)
        sns.barplot(x=top_pickup_zones.values, y=top_pickup_zones.index, palette="viridis")
        plt.title('Top 10 Pickup Zones')
        plt.xlabel('Number of Pickups')

        # Plotting the top dropoff zones
        plt.subplot(1, 2, 2)
        sns.barplot(x=top_dropoff_zones.values, y=top_dropoff_zones.index, palette="viridis")
        plt.title('Top 10 Dropoff Zones')
        plt.xlabel('Number of Dropoffs')

        plt.tight_layout()
        plt.show()
    def plot_pickups_by_hour(self, data_path):
        data = pq.read_table(data_path).to_pandas()
        
        # Convert 'lpep_pickup_datetime' to datetime format
        data['PU_time'] = pd.to_datetime(data['PU_time'])

        # Extract the hour from the pickup datetime
        data['pickup_hour'] = data['PU_time'].dt.hour

        # Plot the number of pickups for each hour of the day
        plt.figure(figsize=(12, 6))
        sns.countplot(data=data, x='pickup_hour', palette="viridis")
        plt.title('Number of Pickups for Each Hour of the Day')
        plt.xlabel('Hour of the Day')
        plt.ylabel('Number of Pickups')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show()
     def plot_order_fare_by_hour(self, data_path):
        data = pq.read_table(data_path).to_pandas()

        # Convert 'lpep_pickup_datetime' to datetime format if not done before
        if data['PU_time'].dtype != 'datetime64[ns]':
            data['PU_time'] = pd.to_datetime(data['PU_time'])

        # Extract the hour from the pickup datetime if not done before
        if 'pickup_hour' not in data.columns:
            data['pickup_hour'] = data['PU_time'].dt.hour

        grouped_data = data.groupby('pickup_hour').agg({
            'total_amount': 'sum',
            'DATE': 'count'
        }).reset_index()

        grouped_data.rename(columns={'total_amount': 'total_fare', 'DATE': 'order_count'}, inplace=True)

        fig, ax1 = plt.subplots(figsize=(15, 8))

        line1, = ax1.plot(grouped_data["pickup_hour"], grouped_data["order_count"], 'b-', label="Order Count", marker="o")
        ax1.set_xlabel('Hour of the Day')
        ax1.set_ylabel('Order Count', color='b')
        ax1.tick_params('y', colors='b')

        ax2 = ax1.twinx()
        line2, = ax2.plot(grouped_data["pickup_hour"], grouped_data["total_fare"], 'g-', label="Total Fare", marker="o")
        ax2.set_ylabel('Total Fare', color='g')
        ax2.tick_params('y', colors='g')

        plt.title("Total Order Count and Total Fare for Each Hour", fontsize=16)

        ax1.legend(handles=[line1, line2], loc="upper left")

        plt.show()
    def plot_order_fare_by_weekday(self, data_path):
        data = pq.read_table(data_path).to_pandas()

        data['weekday'] = pd.to_datetime(data['DATE']).dt.dayofweek

        grouped_weekday_data = data.groupby('weekday').agg({
            'total_amount': 'mean',
            'DATE': 'count'
        }).reset_index()

        grouped_weekday_data.rename(columns={'total_amount': 'avg_fare', 'DATE': 'order_count'}, inplace=True)

        fig, ax1 = plt.subplots(figsize=(15, 8))

        weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        bars1 = ax1.bar(weekdays, grouped_weekday_data["order_count"], color='b', label="Average Order Count", alpha=0.6)
        ax1.set_xlabel('Day of the Week')
        ax1.set_ylabel('Average Order Count', color='b')
        ax1.tick_params('y', colors='b')

        ax2 = ax1.twinx()
        line2, = ax2.plot(weekdays, grouped_weekday_data["avg_fare"], 'g-', label="Average Fare", marker="o")
        ax2.set_ylabel('Average Fare', color='g')
        ax2.tick_params('y', colors='g')

        plt.title("Average Order Count and Average Fare for Each Day of the Week", fontsize=16)

        ax1.legend(loc="upper left")
        ax2.legend(loc="upper right")

        plt.show()
    def plot_24hr_analysis(self, data_path):
        data = pq.read_table(data_path).to_pandas()

        if 'weekday' not in data.columns:
            data['weekday'] = pd.to_datetime(data['DATE']).dt.dayofweek

        data['day_type'] = data['weekday'].apply(lambda x: 'Weekday' if x < 5 else 'Weekend')

        grouped_daytype_data = data.groupby(['day_type', 'pickup_hour']).agg({
            'total_amount': 'mean',
            'distance': 'mean',
            'DATE': 'count'
        }).reset_index()

        grouped_daytype_data.rename(columns={'total_amount': 'avg_fare', 'distance': 'avg_distance', 'DATE': 'order_count'}, inplace=True)

        fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(20, 12))
        fig.suptitle("24-hour Analysis for Weekdays vs. Weekends", fontsize=20)

        def plot_daytype_analysis(ax, data, day_type, metric, ylabel):
            subset = data[data['day_type'] == day_type]
            ax.plot(subset['pickup_hour'], subset[metric], marker="o")
            ax.set_title(f"{day_type} - {ylabel}")
            ax.set_xlabel("Hour of the Day")
            ax.set_ylabel(ylabel)

        plot_daytype_analysis(axes[0, 0], grouped_daytype_data, 'Weekday', 'order_count', 'Order Count')
        plot_daytype_analysis(axes[0, 1], grouped_daytype_data, 'Weekday', 'avg_fare', 'Average Fare')
        plot_daytype_analysis(axes[0, 2], grouped_daytype_data, 'Weekday', 'avg_distance', 'Average Distance (in miles)')

        plot_daytype_analysis(axes[1, 0], grouped_daytype_data, 'Weekend', 'order_count', 'Order Count')
        plot_daytype_analysis(axes[1, 1], grouped_daytype_data, 'Weekend', 'avg_fare', 'Average Fare')
        plot_daytype_analysis(axes[1, 2], grouped_daytype_data, 'Weekend', 'avg_distance', 'Average Distance (in miles)')

        plt.tight_layout()
        plt.subplots_adjust(top=0.9)
        plt.show()
    def plot_rain_analysis(self, data_path):
        data = pq.read_table(data_path).to_pandas()

        # Grouping data again to include 'total_amount'
        daily_data = data.groupby('DATE').agg({
            'distance': 'mean',
            'total_amount': 'mean',
            'DATE': 'count',
            'Rainfall': 'mean'
        }).rename(columns={'DATE': 'order_count'})

        # Categorize Rainfall into 'rain' and 'normal'
        daily_data['rain_status'] = daily_data['Rainfall'].apply(lambda x: 'rain' if x >= 0.5 else 'normal')

        # Plotting using seaborn
        fig, ax = plt.subplots(3, 1, figsize=(15, 15))

        # Rain Status vs Average Order Count
        sns.violinplot(x=daily_data['rain_status'], y=daily_data['order_count'], ax=ax[0], palette="coolwarm", inner="quartile")
        ax[0].set_title('Rain Status vs Average Order Count')
        ax[0].set_xlabel('Rain Status')
        ax[0].set_ylabel('Average Order Count')

        # Rain Status vs Average Distance
        sns.violinplot(x=daily_data['rain_status'], y=daily_data['distance'], ax=ax[1], palette="coolwarm", inner="quartile")
        ax[1].set_title('Rain Status vs Average Distance')
        ax[1].set_xlabel('Rain Status')
        ax[1].set_ylabel('Average Distance (miles)')

        # Rain Status vs Average Fare Amount
        sns.violinplot(x=daily_data['rain_status'], y=daily_data['total_amount'], ax=ax[2], palette="coolwarm", inner="quartile")
        ax[2].set_title('Rain Status vs Average Fare Amount')
        ax[2].set_xlabel('Rain Status')
        ax[2].set_ylabel('Average Fare Amount ($)')

        plt.tight_layout()
        plt.show()
    def plot_trip_type_analysis(self, data_path):
        data = pq.read_table(data_path).to_pandas()

        # Classify each order as short or long based on the distance threshold
        data['trip_type'] = data['distance'].apply(lambda x: 'short' if x <= 10 else 'long')

        # Ensure PU_time column is of string type
        data['PU_time'] = data['PU_time'].astype(str)

        # Extract hour from PU_time and group by hour and trip_type to get counts
        hourly_counts = data.groupby([data['PU_time'].str.slice(11, 13), 'trip_type']).size().unstack(fill_value=0).reset_index()
        hourly_counts.columns.name = None  # Remove the column index name
        hourly_counts.rename(columns={'PU_time': 'hour'}, inplace=True)

        hourly_counts['total'] = hourly_counts['short'] + hourly_counts['long']
        hourly_counts['short_proportion'] = hourly_counts['short'] / hourly_counts['total']
        hourly_counts['long_proportion'] = hourly_counts['long'] / hourly_counts['total']

# Convert DATE column to datetime format and extract day of the week
        data['day_of_week'] = pd.to_datetime(data['DATE']).dt.day_name()

# Group by day_of_week and trip_type to get counts
        daily_counts = data.groupby(['day_of_week', 'trip_type']).size().unstack(fill_value=0).reset_index()
        daily_counts.columns.name = None  # Remove the column index name

# Reorder the days of the week
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        daily_counts['day_of_week'] = pd.Categorical(daily_counts['day_of_week'], categories=day_order, ordered=True)
        daily_counts.sort_values('day_of_week', inplace=True)

# Calculate proportions for plotting
        daily_counts['total'] = daily_counts['short'] + daily_counts['long']
        daily_counts['short_proportion'] = daily_counts['short'] / daily_counts['total']
        daily_counts['long_proportion'] = daily_counts['long'] / daily_counts['total']

# Set up the figure with two subplots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 12))

# Plot hourly proportions
        ax1.bar(hourly_counts['hour'], hourly_counts['short_proportion'], label='Short Trips', color='blue', alpha=0.7)
        ax1.bar(hourly_counts['hour'], hourly_counts['long_proportion'], bottom=hourly_counts['short_proportion'], label='Long Trips', color='red', alpha=0.7)
        ax1.set_xlabel('Hour of Day')
        ax1.set_ylabel('Proportion')
        ax1.set_title('Proportion of Short and Long Trips by Hour')
        ax1.legend()

# Plot only the long trips proportion by day of week
        ax2.bar(daily_counts['day_of_week'], daily_counts['long_proportion'], label='Long Trips', color='red', alpha=0.7)
        ax2.set_xlabel('Day of Week')
        ax2.set_ylabel('Proportion of Long Trips')
        ax2.set_title('Proportion of Long Trips by Day of Week')
        ax2.legend()

        plt.tight_layout()
        plt.show()
    def plot_top_zones_trip_type(self, data_path):
        data = pq.read_table(data_path).to_pandas()
        # Group by PU_Zone and calculate the counts for short and long trips
        pu_counts = data.groupby(['PU_Zone', 'trip_type']).size().unstack(fill_value=0).reset_index()
        pu_counts.columns.name = None  # Remove the column index name
        pu_counts.sort_values(by='long', ascending=False, inplace=True)
        # Group by DO_Zone and calculate the counts for short and long trips
        do_counts = data.groupby(['DO_Zone', 'trip_type']).size().unstack(fill_value=0).reset_index()
        do_counts.columns.name = None  # Remove the column index name
        do_counts.sort_values(by='long', ascending=False, inplace=True)

# Get the top 10 zones for both pickup and dropoff for long trips
        top_pu_zones = pu_counts.head(10)
        top_do_zones = do_counts.head(10)

# Set up the figure with two subplots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 14))

# Plot for top pickup zones
        ax1.barh(top_pu_zones['PU_Zone'], top_pu_zones['long'], color='red', alpha=0.7, label='Long Trips')
        ax1.barh(top_pu_zones['PU_Zone'], top_pu_zones['short'], left=top_pu_zones['long'], color='blue', alpha=0.7, label='Short Trips')
        ax1.set_xlabel('Number of Trips')
        ax1.set_title('Top 10 Pickup Zones for Long Trips')
        ax1.legend()
        ax1.invert_yaxis()  # Invert y-axis for better visualization

# Plot for top dropoff zones
        ax2.barh(top_do_zones['DO_Zone'], top_do_zones['long'], color='red', alpha=0.7, label='Long Trips')
        ax2.barh(top_do_zones['DO_Zone'], top_do_zones['short'], left=top_do_zones['long'], color='blue', alpha=0.7, label='Short Trips')
        ax2.set_xlabel('Number of Trips')
        ax2.set_title('Top 10 Dropoff Zones for Long Trips')
        ax2.legend()
        ax2.invert_yaxis()  # Invert y-axis for better visualization

        plt.tight_layout()
        plt.show()
        
    def plot_trip_type_factors(self, data_path):
        data = pq.read_table(data_path).to_pandas()
        passenger_counts = data.groupby(['passenger_count', 'trip_type']).size().unstack(fill_value=0).reset_index()
        passenger_counts.columns.name = None  # Remove the column index name

# Calculate proportions for plotting
        passenger_counts['total'] = passenger_counts['short'] + passenger_counts['long']
        passenger_counts['short_proportion'] = passenger_counts['short'] / passenger_counts['total']
        passenger_counts['long_proportion'] = passenger_counts['long'] / passenger_counts['total']

# Group by RatecodeID and calculate the counts for short and long trips
        ratecode_counts = data.groupby(['RatecodeID', 'trip_type']).size().unstack(fill_value=0).reset_index()
        ratecode_counts.columns.name = None  # Remove the column index name

# Calculate proportions for plotting
        ratecode_counts['total'] = ratecode_counts['short'] + ratecode_counts['long']
        ratecode_counts['short_proportion'] = ratecode_counts['short'] / ratecode_counts['total']
        ratecode_counts['long_proportion'] = ratecode_counts['long'] / ratecode_counts['total']

# Group by payment_type and calculate the counts for short and long trips
        payment_counts = data.groupby(['payment_type', 'trip_type']).size().unstack(fill_value=0).reset_index()
        payment_counts.columns.name = None  # Remove the column index name

# Calculate proportions for plotting
        payment_counts['total'] = payment_counts['short'] + payment_counts['long']
        payment_counts['short_proportion'] = payment_counts['short'] / payment_counts['total']
        payment_counts['long_proportion'] = payment_counts['long'] / payment_counts['total']

# Mapping the RateCodeID and Payment_type values to their actual meanings
        ratecode_map = {
            1: 'Standard rate',
            2: 'JFK',
            3: 'Newark',
            4: 'Nassau or Westchester',
            5: 'Negotiated fare',
            6: 'Group ride'
        }

        payment_map = {
            1: 'Credit card',
            2: 'Cash',
            3: 'No charge',
            4: 'Dispute',
            5: 'Unknown',
            6: 'Voided trip'
        }

# Replace the values in the dataframes
        passenger_counts['passenger_count'] = passenger_counts['passenger_count'].astype(str)
        ratecode_counts['RatecodeID'] = ratecode_counts['RatecodeID'].map(ratecode_map)
        payment_counts['payment_type'] = payment_counts['payment_type'].map(payment_map)

        ratecode_counts = ratecode_counts.dropna(subset=['RatecodeID'])
        payment_counts = payment_counts.dropna(subset=['payment_type'])

# Set up the figure with three subplots
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(14, 18))

# Plot for passenger_count
        ax1.bar(passenger_counts['passenger_count'], passenger_counts['short_proportion'], label='Short Trips', color='blue', alpha=0.7)
        ax1.bar(passenger_counts['passenger_count'], passenger_counts['long_proportion'], bottom=passenger_counts['short_proportion'], label='Long Trips', color='red', alpha=0.7)
        ax1.set_xlabel('Passenger Count')
        ax1.set_ylabel('Proportion')
        ax1.set_title('Proportion of Trips by Passenger Count')
        ax1.legend()

# Plot for RatecodeID
        ax2.bar(ratecode_counts['RatecodeID'], ratecode_counts['short_proportion'], label='Short Trips', color='blue', alpha=0.7)
        ax2.bar(ratecode_counts['RatecodeID'], ratecode_counts['long_proportion'], bottom=ratecode_counts['short_proportion'], label='Long Trips', color='red', alpha=0.7)
        ax2.set_xlabel('RatecodeID')
        ax2.set_ylabel('Proportion')
        ax2.set_title('Proportion of Trips by RatecodeID')
        ax2.legend()
        ax2.tick_params(axis='x', rotation=45)

# Plot for payment_type
        ax3.bar(payment_counts['payment_type'], payment_counts['short_proportion'], label='Short Trips', color='blue', alpha=0.7)
        ax3.bar(payment_counts['payment_type'], payment_counts['long_proportion'], bottom=payment_counts['short_proportion'], label='Long Trips', color='red', alpha=0.7)
        ax3.set_xlabel('Payment Type')
        ax3.set_ylabel('Proportion')
        ax3.set_title('Proportion of Trips by Payment Type')
        ax3.legend()
        ax3.tick_params(axis='x', rotation=45)

        plt.tight_layout()

        plt.show()
    def plot_passenger_analysis(self, data_path):
        data = pq.read_table(data_path).to_pandas()
        
        grouped_passenger_data = data.groupby('passenger_count').agg({
            'total_amount': 'mean',
            'DATE': 'count'
        }).reset_index()

        grouped_passenger_data.rename(columns={'total_amount': 'avg_fare', 'DATE': 'order_count'}, inplace=True)

        fig, ax1 = plt.subplots(figsize=(15, 8))

        bars1 = ax1.bar(grouped_passenger_data['passenger_count'].astype(str), grouped_passenger_data["order_count"], color='b', label="Order Count", alpha=0.6)
        ax1.set_xlabel('Number of Passengers')
        ax1.set_ylabel('Order Count', color='b')
        ax1.tick_params('y', colors='b')

        ax2 = ax1.twinx()
        line2, = ax2.plot(grouped_passenger_data['passenger_count'].astype(str), grouped_passenger_data["avg_fare"], 'g-', label="Average Fare", marker="o")
        ax2.set_ylabel('Average Fare', color='g')
        ax2.tick_params('y', colors='g')

        plt.title("Order Count and Average Fare by Number of Passengers", fontsize=16)

        ax1.legend(loc="upper left")
        ax2.legend(loc="upper right")

        plt.show()

class Prediction:
    def __init__(self):
        pass


if __name__ == "__main__":
    # Aggregate raw data to a time-ranged file
    data_loader = Data_loader()
    time_range = "2022-01-01_2023-07-31"
    new_file_dir = data_loader.raw_data_agg(time_range)

    # Preprocessing

    # Visualization

    # Prediction
