from my_scripts import Regression, Data_loader, Time_series_analysis
import streamlit as st
import datetime

# Set path
raw_dir = 'data/green_raw/'
output_dir = 'data/green.parquet'
nyc_shapefile_dir = 'data/NYC_Shapefile/NYC.shp'
borough_lst = ['Bronx', 'Brooklyn', 'Manhattan', 'Queens']
target_lst = ['Counts', 'Fare']


# @st.cache(allow_output_mutation=True)  # buffer the output
@st.cache_data  # buffer the output
def load_data(time_range):
    data_loader = Data_loader.Data_loader(raw_dir=raw_dir, output_dir=output_dir,
                                          nyc_shapefile_dir=nyc_shapefile_dir)
    df = data_loader.get_final_processed_df(time_range=time_range, export_final=False)
    return df


def main():
    st.title("Time Series Prediction")

    if 'loaded_data' not in st.session_state:
        st.session_state['loaded_data'] = None
        st.session_state['time_range'] = None

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

    # Convert selected dates to the required string format
    pred_time_range = "{0}_{1}".format(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))

    if st.button('Load Data'):
        st.session_state['time_range'] = pred_time_range
        # Load data with caching
        st.session_state['loaded_data'] = load_data(pred_time_range)

    if st.session_state['loaded_data'] is not None:
        # Load data with caching
        df = st.session_state['loaded_data']
        # Initialize the object
        vis = Time_series_analysis.Time_series_analysis(raw_dir, output_dir, nyc_shapefile_dir,
                                                        pred_time_range=pred_time_range,
                                                        data=df,
                                                        if_st=True)
        options = {
            "Seasonal Naive Prediction": vis.seasonal_naive_pred,
            "Arima Naive Prediction": vis.arima_pred
        }

        options_sample = {
            'Day': 'D',
            '1 Week': 'W',
            '2 Week': '2W',
            '3 Week': '3W',
            'Month': 'M',
            'Quarter': 'Q',
        }

        choice = st.selectbox("Choose a Visualization:", list(options.keys()))
        choice_borough = st.selectbox("Choose a Borough:", list(borough_lst))
        choice_type = st.selectbox("Choose a Target:", list(target_lst))
        choice_rate = st.selectbox("Choose a rate of test set over sum:", [0.1, 0.2, 0.3])
        choice_period = st.selectbox("Choose a Regular Period:", [1, 2, 3, 4, 5, 6, 7, 30, 90])
        choice_sample = st.selectbox("Choose a Analysis sample-rate:", list(options_sample.keys()))

        if st.button("Show Visualization"):
            filter_con = choice_type
            select = choice_borough
            pivot_counts, pivot_fare = vis.data_pivot(df)
            item_title, temp_df = vis.select_df(filter_con, select, pivot_counts, pivot_fare)

            if choice == "Seasonal Naive Prediction":
                options[choice](temp_df, select, item_title,
                                sample=options_sample[choice_sample],
                                regular_period=choice_period,
                                test_train_rate=choice_rate)  # (filter_con)
            elif choice == "Arima Naive Prediction":
                options[choice](temp_df, select, item_title, sample=options_sample[choice_sample], m=choice_period,
                                test_train_rate=choice_rate)  # (filter_con)

    else:
        st.write('Please select a date range and click "Load Data" to view visualizations.')


if __name__ == "__main__":
    main()
