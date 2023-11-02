import streamlit as st
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import re
import os
import pyarrow.parquet as pq
import geopandas as gpd
import geoplot as gplt
import geoplot.crs as gcrs
import folium
from folium.plugins import HeatMap
from my_scripts import Data_loader


class Visualization:
    def __init__(self, data_path, if_st=True):
        da = Data_loader
        self.if_st = if_st
        self.data = pq.read_table(data_path).to_pandas()
        # self.df_merge_geo_zip, self.df_merge_geo_borough, self.proj = da.load_merged_geodata(self.data)

    def plot_top_zones(self, filter_con=None):
        data = self.data
        data['trip_type'] = data['distance'].apply(lambda x: 'short' if x <= 10 else 'long')

        # Top 10 pickup zones
        top_pickup_zones = data['PU_Zone'].value_counts().head(10)

        # Top 10 dropoff zones
        top_dropoff_zones = data['DO_Zone'].value_counts().head(10)

        fig, axes = plt.subplots(1, 2, figsize=(12, 6))

        # 绘制顶部上车区域的条形图
        sns.barplot(x=top_pickup_zones.values, y=top_pickup_zones.index, palette="viridis", ax=axes[0])
        axes[0].set_title('Top 10 Pickup Zones')
        axes[0].set_xlabel('Number of Pickups')

        # 绘制顶部下车区域的条形图
        sns.barplot(x=top_dropoff_zones.values, y=top_dropoff_zones.index, palette="viridis", ax=axes[1])
        axes[1].set_title('Top 10 Dropoff Zones')
        axes[1].set_xlabel('Number of Dropoffs')

        plt.tight_layout()
        if self.if_st:
            st.pyplot(fig)
        else:
            plt.show()

    def plot_pickups_by_hour(self, filter_con=None):
        data = self.data

        # Convert 'lpep_pickup_datetime' to datetime format
        data['PU_time'] = pd.to_datetime(data['PU_time'])

        # Extract the hour from the pickup datetime
        data['pickup_hour'] = data['PU_time'].dt.hour

        # Plot the number of pickups for each hour of the day
        fig = plt.figure(figsize=(12, 6))
        sns.countplot(data=data, x='pickup_hour', palette="viridis")
        plt.title('Number of Pickups for Each Hour of the Day')
        plt.xlabel('Hour of the Day')
        plt.ylabel('Number of Pickups')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()

        if self.if_st:
            st.pyplot(fig)
        else:
            plt.show()

    def plot_order_fare_by_hour(self, filter_con=None):
        data = self.data

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

        line1, = ax1.plot(grouped_data["pickup_hour"], grouped_data["order_count"], 'b-', label="Order Count",
                          marker="o")
        ax1.set_xlabel('Hour of the Day')
        ax1.set_ylabel('Order Count', color='b')
        ax1.tick_params('y', colors='b')

        ax2 = ax1.twinx()
        line2, = ax2.plot(grouped_data["pickup_hour"], grouped_data["total_fare"], 'g-', label="Total Fare", marker="o")
        ax2.set_ylabel('Total Fare', color='g')
        ax2.tick_params('y', colors='g')

        plt.title("Total Order Count and Total Fare for Each Hour", fontsize=16)

        ax1.legend(handles=[line1, line2], loc="upper left")

        if self.if_st:
            st.pyplot(fig)
        else:
            plt.show()

    def plot_order_fare_by_weekday(self, filter_con=None):
        data = self.data

        data['weekday'] = pd.to_datetime(data['DATE']).dt.dayofweek

        grouped_weekday_data = data.groupby('weekday').agg({
            'total_amount': 'mean',
            'DATE': 'count'
        }).reset_index()

        grouped_weekday_data.rename(columns={'total_amount': 'avg_fare', 'DATE': 'order_count'}, inplace=True)

        fig, ax1 = plt.subplots(figsize=(15, 8))

        weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        ax1.bar(weekdays, grouped_weekday_data["order_count"], color='b', label="Average Order Count",
                alpha=0.6)
        ax1.set_xlabel('Day of the Week')
        ax1.set_ylabel('Average Order Count', color='b')
        ax1.tick_params('y', colors='b')

        ax2 = ax1.twinx()
        ax2.plot(weekdays, grouped_weekday_data["avg_fare"], 'g-', label="Average Fare", marker="o")
        ax2.set_ylabel('Average Fare', color='g')
        ax2.tick_params('y', colors='g')

        plt.title("Average Order Count and Average Fare for Each Day of the Week", fontsize=16)

        ax1.legend(loc="upper left")
        ax2.legend(loc="upper right")

        if self.if_st:
            st.pyplot(fig)
        else:
            plt.show()

    def plot_24hr_analysis(self, filter_con=None):
        data = self.data
        data['PU_time'] = pd.to_datetime(data['PU_time'])
        data['pickup_hour'] = data['PU_time'].dt.hour

        if 'weekday' not in data.columns:
            data['weekday'] = pd.to_datetime(data['DATE']).dt.dayofweek

        data['day_type'] = data['weekday'].apply(lambda x: 'Weekday' if x < 5 else 'Weekend')

        grouped_daytype_data = data.groupby(['day_type', 'pickup_hour']).agg({
            'total_amount': 'mean',
            'distance': 'mean',
            'DATE': 'count'
        }).reset_index()

        grouped_daytype_data.rename(
            columns={'total_amount': 'avg_fare', 'distance': 'avg_distance', 'DATE': 'order_count'}, inplace=True)

        fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(20, 12))
        fig.suptitle("24-hour Analysis for Weekdays vs. Weekends", fontsize=20)

        def plot_daytype_analysis(ax, data, day_type, metric, ylabel):
            subset = data[data['day_type'] == day_type]
            ax.plot(subset['pickup_hour'], subset[metric], marker="o")
            ax.set_title("{0} - {1}".format(day_type, ylabel))
            ax.set_xlabel("Hour of the Day")
            ax.set_ylabel(ylabel)

        plot_daytype_analysis(axes[0, 0], grouped_daytype_data, 'Weekday', 'order_count', 'Order Count')
        plot_daytype_analysis(axes[0, 1], grouped_daytype_data, 'Weekday', 'avg_fare', 'Average Fare')
        plot_daytype_analysis(axes[0, 2], grouped_daytype_data, 'Weekday', 'avg_distance',
                              'Average Distance (in miles)')

        plot_daytype_analysis(axes[1, 0], grouped_daytype_data, 'Weekend', 'order_count', 'Order Count')
        plot_daytype_analysis(axes[1, 1], grouped_daytype_data, 'Weekend', 'avg_fare', 'Average Fare')
        plot_daytype_analysis(axes[1, 2], grouped_daytype_data, 'Weekend', 'avg_distance',
                              'Average Distance (in miles)')

        plt.tight_layout()
        plt.subplots_adjust(top=0.9)

        if self.if_st:
            st.pyplot(fig)
        else:
            plt.show()

    def plot_rain_analysis(self, filter_con=None):
        data = self.data

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
        sns.violinplot(x=daily_data['rain_status'], y=daily_data['order_count'], ax=ax[0], palette="coolwarm",
                       inner="quartile")
        ax[0].set_title('Rain Status vs Average Order Count')
        ax[0].set_xlabel('Rain Status')
        ax[0].set_ylabel('Average Order Count')

        # Rain Status vs Average Distance
        sns.violinplot(x=daily_data['rain_status'], y=daily_data['distance'], ax=ax[1], palette="coolwarm",
                       inner="quartile")
        ax[1].set_title('Rain Status vs Average Distance')
        ax[1].set_xlabel('Rain Status')
        ax[1].set_ylabel('Average Distance (miles)')

        # Rain Status vs Average Fare Amount
        sns.violinplot(x=daily_data['rain_status'], y=daily_data['total_amount'], ax=ax[2], palette="coolwarm",
                       inner="quartile")
        ax[2].set_title('Rain Status vs Average Fare Amount')
        ax[2].set_xlabel('Rain Status')
        ax[2].set_ylabel('Average Fare Amount ($)')

        plt.tight_layout()
        if self.if_st:
            st.pyplot(fig)
        else:
            plt.show()

    def plot_trip_type_analysis(self, filter_con=None):
        data = self.data

        # Classify each order as short or long based on the distance threshold
        data['trip_type'] = data['distance'].apply(lambda x: 'short' if x <= 10 else 'long')

        # Ensure PU_time column is of string type
        data['PU_time'] = data['PU_time'].astype(str)

        # Extract hour from PU_time and group by hour and trip_type to get counts
        hourly_counts = data.groupby([data['PU_time'].str.slice(11, 13), 'trip_type']).size().unstack(
            fill_value=0).reset_index()
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
        ax1.bar(hourly_counts['hour'], hourly_counts['long_proportion'], bottom=hourly_counts['short_proportion'],
                label='Long Trips', color='red', alpha=0.7)
        ax1.set_xlabel('Hour of Day')
        ax1.set_ylabel('Proportion')
        ax1.set_title('Proportion of Short and Long Trips by Hour')
        ax1.legend()

        # Plot only the long trips proportion by day of week
        ax2.bar(daily_counts['day_of_week'], daily_counts['long_proportion'], label='Long Trips', color='red',
                alpha=0.7)
        ax2.set_xlabel('Day of Week')
        ax2.set_ylabel('Proportion of Long Trips')
        ax2.set_title('Proportion of Long Trips by Day of Week')
        ax2.legend()

        plt.tight_layout()
        if self.if_st:
            st.pyplot(fig)
        else:
            plt.show()

    def plot_top_zones_trip_type(self, filter_con=None):
        data = self.data
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
        ax1.barh(top_pu_zones['PU_Zone'], top_pu_zones['short'], left=top_pu_zones['long'], color='blue', alpha=0.7,
                 label='Short Trips')
        ax1.set_xlabel('Number of Trips')
        ax1.set_title('Top 10 Pickup Zones for Long Trips')
        ax1.legend()
        ax1.invert_yaxis()  # Invert y-axis for better visualization

        # Plot for top dropoff zones
        ax2.barh(top_do_zones['DO_Zone'], top_do_zones['long'], color='red', alpha=0.7, label='Long Trips')
        ax2.barh(top_do_zones['DO_Zone'], top_do_zones['short'], left=top_do_zones['long'], color='blue', alpha=0.7,
                 label='Short Trips')
        ax2.set_xlabel('Number of Trips')
        ax2.set_title('Top 10 Dropoff Zones for Long Trips')
        ax2.legend()
        ax2.invert_yaxis()  # Invert y-axis for better visualization

        plt.tight_layout()
        if self.if_st:
            st.pyplot(fig)
        else:
            plt.show()

    def plot_trip_type_factors(self, filter_con=None):
        data = self.data
        data['trip_type'] = data['distance'].apply(lambda x: 'short' if x <= 10 else 'long')

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
        ax1.bar(passenger_counts['passenger_count'], passenger_counts['short_proportion'], label='Short Trips',
                color='blue', alpha=0.7)
        ax1.bar(passenger_counts['passenger_count'], passenger_counts['long_proportion'],
                bottom=passenger_counts['short_proportion'], label='Long Trips', color='red', alpha=0.7)
        ax1.set_xlabel('Passenger Count')
        ax1.set_ylabel('Proportion')
        ax1.set_title('Proportion of Trips by Passenger Count')
        ax1.legend()

        # Plot for RatecodeID
        ax2.bar(ratecode_counts['RatecodeID'], ratecode_counts['short_proportion'], label='Short Trips', color='blue',
                alpha=0.7)
        ax2.bar(ratecode_counts['RatecodeID'], ratecode_counts['long_proportion'],
                bottom=ratecode_counts['short_proportion'], label='Long Trips', color='red', alpha=0.7)
        ax2.set_xlabel('RatecodeID')
        ax2.set_ylabel('Proportion')
        ax2.set_title('Proportion of Trips by RatecodeID')
        ax2.legend()
        ax2.tick_params(axis='x', rotation=45)

        # Plot for payment_type
        ax3.bar(payment_counts['payment_type'], payment_counts['short_proportion'], label='Short Trips', color='blue',
                alpha=0.7)
        ax3.bar(payment_counts['payment_type'], payment_counts['long_proportion'],
                bottom=payment_counts['short_proportion'], label='Long Trips', color='red', alpha=0.7)
        ax3.set_xlabel('Payment Type')
        ax3.set_ylabel('Proportion')
        ax3.set_title('Proportion of Trips by Payment Type')
        ax3.legend()
        ax3.tick_params(axis='x', rotation=45)

        plt.tight_layout()

        if self.if_st:
            st.pyplot(fig)
        else:
            plt.show()

    def plot_passenger_analysis(self, filter_con=None):
        data = self.data

        grouped_passenger_data = data.groupby('passenger_count').agg({
            'total_amount': 'mean',
            'DATE': 'count'
        }).reset_index()

        grouped_passenger_data.rename(columns={'total_amount': 'avg_fare', 'DATE': 'order_count'}, inplace=True)

        fig, ax1 = plt.subplots(figsize=(15, 8))

        ax1.bar(grouped_passenger_data['passenger_count'].astype(str), grouped_passenger_data["order_count"],
                color='b', label="Order Count", alpha=0.6)
        ax1.set_xlabel('Number of Passengers')
        ax1.set_ylabel('Order Count', color='b')
        ax1.tick_params('y', colors='b')

        ax2 = ax1.twinx()
        ax2.plot(grouped_passenger_data['passenger_count'].astype(str), grouped_passenger_data["avg_fare"],
                 'g-', label="Average Fare", marker="o")
        ax2.set_ylabel('Average Fare', color='g')
        ax2.tick_params('y', colors='g')

        plt.title("Order Count and Average Fare by Number of Passengers", fontsize=16)

        ax1.legend(loc="upper left")
        ax2.legend(loc="upper right")

        if self.if_st:
            st.pyplot(fig)
        else:
            plt.show()

    def NYC_Heatmap_hailing_counts(self, filter_con=None):
        data = self.data
        NYC_center = [40.7127753, -74.0059728]
        san_map = folium.Map(location=NYC_center, zoom_start=12)
        heatdata = data['PU_LatLong']
        HeatMap(heatdata).add_to(san_map)
        if self.if_st:
            st.write(san_map)
        else:
            return san_map

    def region_analysis(self, df_merge_geo, proj, filter_con=None):
        def plot_state_to_ax(column, ax, df_draw_avg):
            gplt.choropleth(df_draw_avg.loc[:, [column, 'geometry']],
                            hue=column,
                            cmap='viridis',  # rainbow
                            linewidth=1.0,
                            ax=ax)
            gplt.polyplot(nyc_boroughs, edgecolor='black', linewidth=1, ax=ax)

        region_column = [i for i in list(df_merge_geo.columns) if i.startswith("PU")][0]
        df_draw_avg = df_merge_geo.set_index(region_column).loc[:, ["Frequency", 'Fare', 'geometry']]

        fig, axes = plt.subplots(1, 2, figsize=(12, 6), subplot_kw={'projection': proj})
        plt.suptitle('Green Taxi by {}, NYC'.format(region_column.split('_')[1]), fontsize=16)

        plot_state_to_ax('Frequency', axes[0], df_draw_avg)
        axes[0].set_title('Regional Frequency in NYC')

        plot_state_to_ax('Fare', axes[1], df_draw_avg)
        axes[1].set_title('Regional Fare in NYC')

        if self.if_st:
            # st.write(san_map)
            st.pyplot(fig)
        else:
            plt.show()

    def plotly_region_interactgraph(self, df_merge_geo, target='Fare', filter_con=None):  # or set "Frequency"
        region_column = [i for i in list(df_merge_geo.columns) if i.startswith("PU")][0]
        df_draw_avg = df_merge_geo.set_index(region_column).loc[:, ["Frequency", 'Fare', 'geometry']]

        color_scale = px.colors.sequential.Rainbow
        # Good: "Rainbow", "Plasma", Ugly:"Viridis", "Cividis" (Jerry thinks so lolll~)

        fig = px.choropleth_mapbox(df_draw_avg,
                                   geojson=df_draw_avg.geometry,
                                   locations=df_draw_avg.index,
                                   color=target,
                                   color_continuous_scale=color_scale,
                                   range_color=(df_draw_avg[target].min(), df_draw_avg[target].max()),
                                   center={"lat": 40.7128, "lon": -74.0059},
                                   mapbox_style="carto-darkmatter",  # carto-darkmatter, open-street-map
                                   zoom=8.8)
        fig.update_layout(title_text='{0}-Region {1} Distribution'.format(
            region_column.split('_')[1], target), title_x=0.5)

        if self.if_st:
            st.plotly_chart(fig)
        else:
            fig.show()


if __name__ == "__main__":
    data_path = '../data/green_sum_final.parquet'
    vis = Visualization(data_path=data_path, if_st=False)
    vis.plot_24hr_analysis(data_path)
