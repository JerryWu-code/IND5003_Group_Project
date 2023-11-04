from my_scripts import Visualization, Data_loader
import streamlit as st

# Set path
raw_dir = 'data/green_raw/'
output_dir = 'data/green.parquet'
nyc_shapefile_dir = 'data/NYC_Shapefile/NYC.shp'


# @st.cache(allow_output_mutation=True)  # buffer the output
@st.cache_data  # buffer the output
def load_data(time_range):
    data_loader = Data_loader.Data_loader(raw_dir=raw_dir, output_dir=output_dir,
                                          nyc_shapefile_dir=nyc_shapefile_dir)
    df = data_loader.get_final_processed_df(time_range=time_range, export_final=False)
    return df


def main():
    st.title("Data Visualization")
    min_date = datetime(2020, 1, 1)
    max_date = datetime(2023, 7, 31)
    time_range = st.slider("Select the time range:",
                           min_value=min_date,
                           max_value=max_date,
                           value=(min_date, max_date),
                           format='YYYY-MM-DD')
    start_date, end_date = time_range
    time_range_formatted = f"{start_date.strftime('%Y-%m-%d')}_{end_date.strftime('%Y-%m-%d')}"
    df = load_data(time_range_formatted)

    #time_range = "2022-01-01_2023-07-31"
    # Load data with caching
    #df = load_data(time_range)
    vis = Visualization.Visualization(raw_dir, output_dir, nyc_shapefile_dir, data=df, if_st=True)

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
        "Regional Analysis": vis.region_analysis,
        "Interactive Regional Analysis": vis.plotly_region_interactgraph
    }

    choice = st.selectbox("Choose a Visualization:", list(options.keys()))

    if st.button("Show Visualization"):
        if choice == "Regional Analysis":
            options[choice](area_range='zip')  # (filter_con)
        elif choice == "Interactive Regional Analysis":
            options[choice](area_range='zip', target='Fare')  # (filter_con)
        else:
            options[choice]()


if __name__ == "__main__":
    main()
