from my_scripts import Visualization
import streamlit as st

vis = Visualization.Visualization()
data_path = '../data/green_sum_2022-01-01_2023-07-31_final.parquet'  # 根据您的数据位置进行修改

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
        "Passenger Analysis": vis.plot_passenger_analysis
    }

    choice = st.selectbox("Choose a Visualization:", list(options.keys()))

    if st.button("Show Visualization"):
        options[choice](data_path)

if __name__ == "__main__":
    main()
