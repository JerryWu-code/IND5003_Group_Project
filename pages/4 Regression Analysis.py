from my_scripts import Regression, Data_loader
import streamlit as st

# Set path
raw_dir = 'data/green_raw/'
output_dir = 'data/green.parquet'
nyc_shapefile_dir = 'data/NYC_Shapefile/NYC.shp'
# Clear all caches
st.experimental_set_query_params(clear_cache=True)


# @st.cache_data  # buffer the output
@st.cache_data(allow_output_mutation=True)
def load_data(time_range):
    data_loader = Data_loader.Data_loader(raw_dir=raw_dir, output_dir=output_dir,
                                          nyc_shapefile_dir=nyc_shapefile_dir)
    df = data_loader.get_final_processed_df(time_range=time_range, export_final=False)
    return df


def main():
    st.title("Regression Analysis")

    time_range = "2022-01-01_2022-12-31"
    # Clear all caches before loading new data
    st.experimental_clear_cache()
    # Load data with caching
    df = load_data(time_range)

    reg = Regression.Regression(raw_dir, output_dir, nyc_shapefile_dir, data=df, if_st=True)
    feature_columns = ['AVG_T', 'pickup_hour', 'passenger_count', 'distance', 'Rainfall']
    target_column = 'total_amount'
    options = {
        "Decision Tree": reg.decision_tree_regression,
        "XGBoost": reg.xgboost_regression,
        "Gradient Boosting": reg.GB_regression,
    }

    choice = st.selectbox("Choose a Regression Model:", list(options.keys()))

    if st.button("Show Analysis Results"):
        options[choice](feature_columns, target_column)


if __name__ == "__main__":
    main()
