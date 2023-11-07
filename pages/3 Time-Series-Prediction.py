from my_scripts import Regression, Data_loader, Time_series_analysis
import streamlit as st
import datetime

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
    st.title("Time Series Prediction")

    # Define the minimum and maximum dates available for selection
    min_date = datetime.date(2019, 1, 1)
    max_date = datetime.date(2023, 7, 31)

    # Create a slider for the user to select a date range
    start_date, end_date = st.slider(
        "Select the date range for the prediction:",
        min_value=min_date,
        max_value=max_date,
        value=(min_date, max_date)  # Default range
    )

    # Load data with caching
    time_range = "2019-01-01_2023-07-31"
    df = load_data(time_range)

    # Convert selected dates to the required string format
    pred_time_range = "{0}_{1}".format(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))

    # Initialize the object
    vis = Time_series_analysis.Time_series_analysis(raw_dir, output_dir, nyc_shapefile_dir,
                                                    pred_time_range=pred_time_range, data=df, if_st=True)

    if st.button('Load Data'):
        st.session_state['time_range'] = time_range
        # Load data with caching
        st.session_state['loaded_data'] = load_data(time_range)

    # time_range = "2022-01-01_2023-07-31"
    # Load data with caching
    if st.session_state['loaded_data'] is not None:
        df = st.session_state['loaded_data']
        # df = load_data(time_range)
        vis = Visualization.Visualization(raw_dir, output_dir, nyc_shapefile_dir, pred_time_range=None, data=df,
                                          if_st=True)
        options = {
            "Time Series": vis.region_analysis,
            "Interactive Regional Analysis": vis.plotly_region_interactgraph
        }

        choice = st.selectbox("Choose a Visualization:", list(options.keys()))

        if st.button("Show Visualization"):
            if choice == "Regional Analysis":
                options[choice](area_range='zip')  # (filter_con)
            elif choice == "Interactive Regional Analysis":
                options[choice](area_range='zip', target='Fare')  # (filter_con)

    else:
        st.write('Please select a date range and click "Load Data" to view visualizations.')


if __name__ == "__main__":
    main()
