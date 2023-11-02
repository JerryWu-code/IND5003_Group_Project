from my_scripts import Visualization, Data_loader
import streamlit as st

# Set path
raw_dir = 'data/green_raw/'
output_dir = 'data/green.parquet'
nyc_shapefile_dir = 'data/NYC_Shapefile/NYC.shp'

# Initialize a data_loader
data_loader = Data_loader.Data_loader(raw_dir=raw_dir, output_dir=output_dir,
                                      nyc_shapefile_dir=nyc_shapefile_dir)
# Set time range
time_range = "2022-01-01_2023-07-31"

# Get the data
df = data_loader.get_final_processed_df(time_range=time_range, export_final=False)
vis = Visualization.Visualization(data=df, if_st=True)

def main():
    st.title("Data Visualization App")

    # 下拉菜单的选项和相应的函数映射
    options = {
        "Top Zones": vis.plot_top_zones,
        "Pickups by Hour": vis.plot_pickups_by_hour,
        "Order and Fare by Hour": vis.plot_order_fare_by_hour,
        "Order and Fare by Weekday": vis.plot_order_fare_by_weekday,
        "24-hour Analysis": vis.plot_24hr_analysis,
        "Rain Analysis": vis.plot_rain_analysis,
        "Trip Type Analysis": vis.plot_trip_type_analysis,
        "Top Zones by Trip Type": vis.plot_top_zones_trip_type,
        "Factors affecting Trip Type": vis.plot_trip_type_factors,
        "Passenger Analysis": vis.plot_passenger_analysis,
        "NYC_Hailing_Counts_Heatmap": vis.NYC_Heatmap_hailing_counts,
        "Regional Analysis": vis.region_analysis(df_merge_geo, proj),
        "Interactive Regional Analysis": plotly_region_interactgraph(df_merge_geo, target='Fare')
    }


    choice = st.selectbox("Choose a Visualization:", list(options.keys()))

    if st.button("Show Visualization"):
        options[choice]()  # (filter_con)

if __name__ == "__main__":
    main()
