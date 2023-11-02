from my_scripts import Visualization
import streamlit as st

data_path = 'data/green_sum_final.parquet'
vis = Visualization.Visualization(data_path=data_path, if_st=True)

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
        # "Regional Analysis": vis.region_analysis(df_merge_geo, proj),
        # "Interactive Regional Analysis": plotly_region_interactgraph(df_merge_geo, target='Fare')
    }


    choice = st.selectbox("Choose a Visualization:", list(options.keys()))

    if st.button("Show Visualization"):
        options[choice]()  # (filter_con)

if __name__ == "__main__":
    main()
