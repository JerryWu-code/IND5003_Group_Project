import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
from my_scripts import ts, Data_loader


class Time_series_analysis:
    def __init__(self, df, whole_time, if_st=True):
        self.whole_time = whole_time
        self.data = df
        self.df_counts, self_df_fare = self.load_time_series_data(whole_time)

        pass

    def load_time_series_data(self):
        start = time_range.split("_")[0]
        end = time_range.split("_")[1]
        dt = self.data[(self.data['DATE'] >= start) & (self.data['DATE'] <= end)].reset_index(drop=True)
        dt['PU_Day_Count'] = dt.groupby(
            by=['DATE', 'PU_Borough'])['VendorID'].transform('count')
        dt['PU_Day_Avg_Fare'] = dt.groupby(
            by=['DATE', 'PU_Borough'])['total_amount'].transform(
            lambda x: round(np.average(x), 2))

        return df_counts, df_fare

    from statsmodels.tsa.seasonal import seasonal_decompose, STL
    from statsmodels.tsa.statespace.tools import diff
    from statsmodels.tsa.stattools import acf
    from my_scripts import ts
    from statsmodels.tsa.arima_model import ARIMA
    from statsmodels.tsa.api import ExponentialSmoothing, SimpleExpSmoothing, Holt
    import pmdarima as pm

    borough_lst = ['Bronx', 'Brooklyn', 'Manhattan', 'Queens']

    def data_pivot(dt):
        dt['DATE'] = pd.to_datetime(dt['DATE'])

        dt = dt[dt['PU_Borough'].isin(borough_lst)].reset_index(
            drop=True).set_index('DATE', drop=True).copy()

        dt_bydate_counts = dt.groupby(
            by=['DATE', 'PU_Borough'])['VendorID'].count().reset_index()
        pivot_counts = dt_bydate_counts.pivot_table(index='DATE',
                                                    columns='PU_Borough',
                                                    values='VendorID',
                                                    aggfunc='sum')

        dt_bydate_fare = dt.groupby(
            by=['DATE', 'PU_Borough'])['total_amount'].apply(
            lambda x: round(np.average(x), 2)).reset_index()
        pivot_fare = dt_bydate_fare.pivot_table(index='DATE',
                                                columns='PU_Borough',
                                                values='total_amount',
                                                aggfunc='sum')
        return pivot_counts, pivot_fare

    def select_df(self, filter_con, select, pivot_counts, pivot_fare):
        if filter_con == 'Fare':
            item_name = 'Taxi Average Fare'
            temp_df = pd.DataFrame(pivot_fare.loc[:, select])
            temp_df.index.name = None
        elif filter_con == 'Counts':
            item_name = 'Taxi Hailing Counts'
            temp_df = pd.DataFrame(pivot_counts.loc[:, select])
            temp_df.index.name = None

        item_title = '{1}, {0} in NYC'.format(select, item_name)

        return item_title, temp_df

    def time_series(self, temp_df):
        fig = plt.figure(figsize=(10, 5))
        temp_df[select].plot(title=item_title, marker='o', ms=3, legend=False)
        plt.tight_layout()
        plt.show()

    def season_plot(self, temp_df, sample='M'):
        t_select = temp_df.columns[0]
        temp_df = temp_df.resample(sample).sum()
        temp_df.loc[:, 'year'] = temp_df.index.year
        temp_df.loc[:, 'month'] = temp_df.index.month

        yrs = np.sort(temp_df.year.unique())
        color_ids = np.linspace(0, 1, num=len(yrs))
        colors_to_use = plt.cm.plasma(color_ids)

        plt.figure(figsize=(12, 8))

        for i, yr in enumerate(yrs):
            df_tmp = temp_df.loc[temp_df.year == yr, :]
            plt.plot(df_tmp.month, df_tmp[t_select], color=colors_to_use[i])
            plt.text(12.1, df_tmp[t_select][-1], str(yr), color=colors_to_use[i])
        plt.title('Season Plot: {}'.format(item_title))
        plt.xlim(0, 13)
        plt.xticks(np.arange(1, 13), calendar.month_abbr[1:13])
        plt.show()

    def seasonal_decompose_plot(self, temp_df, sample='M'):
        temp_df = temp_df.resample(sample).sum()
        temp_df_add = seasonal_decompose(temp_df.loc[:, temp_df.columns[0]],
                                         model='additive',
                                         extrapolate_trend='freq')
        # temp_df_add.plot();
        fig, (ax0, ax1, ax2, ax3) = plt.subplots(4, 1, figsize=(12, 9))
        temp_df_add.observed.plot(ax=ax0)
        ax0.title.set_text('Seasonal Decompose Plot: {}'.format(item_title))
        temp_df_add.trend.plot(ax=ax1)
        ax1.set_ylabel('Trend')
        temp_df_add.seasonal.plot(ax=ax2)
        ax2.set_ylabel('Seasonal')
        temp_df_add.resid.plot(ax=ax3, lw=0, marker="o")
        ax3.axhline(y=0, color='black')
        ax3.set_ylabel('Resid')
        plt.show()

    def seasonal_naive_pred(self, temp_df,
                            sample='M',
                            regular_period=7,
                            test_train_rate=1 / 10):  # 7~Week 90~Season 365~year
        temp_df = temp_df.resample(sample).sum()
        cut_point = int(len(temp_df) * test_train_rate)
        train_set = temp_df.iloc[
                    :-cut_point,
                    ]
        test_set = temp_df.iloc[
                   -cut_point:,
                   ]

        # Obtain the forecast from the training set
        mean_forecast = ts.meanf(train_set[select], cut_point)
        snaive_forecast = ts.snaive(train_set[select], cut_point, regular_period)

        # Plot the predictions and true values
        plt.figure(figsize=(12, 8))
        ax = train_set[select].plot(
            title='Seasonal Naive Prediction: {}'.format(item_title), legend=False)
        test_set[select].plot(ax=ax, legend=False, style='--')
        mean_forecast.plot(ax=ax, legend=False, style='-')
        snaive_forecast.plot(ax=ax, legend=False, style='-')
        plt.legend(labels=['train', 'test', 'mean', 'snaive'], loc='lower right')
        plt.show()
        for x in [ts.rmse]:  # , ts.mae, ts.smape]:
            print('{0},mean: {1:.3f}'.format(
                x.__name__, x(test_set[select].values, mean_forecast.values)))
            print('{0},snaive: {1:.3f}'.format(
                x.__name__, x(test_set[select].values, snaive_forecast.values)))
            print('---')
        return mean_forecast, snaive_forecast

    def arima_pred(self, temp_df, sample='D', m=7, test_train_rate=1 / 10):
        temp_df = temp_df.resample(sample).sum()
        cut_point = int(len(temp_df) * test_train_rate)
        train_set = temp_df.iloc[:-cut_point, ]
        test_set = temp_df.iloc[-cut_point:, ]

        arima_m1 = pm.auto_arima(train_set.values, seasonal=True, m=7, test='adf', suppress_warnings=True)

        return arima_m1

    def arima_draw(self, temp_df):
        temp_df = temp_df.resample('D').sum()
        cut_point = int(len(temp_df) * 0.1)
        train_set = temp_df.iloc[:-cut_point, ]
        test_set = temp_df.iloc[-cut_point:, ]
        print('rmse arima:', ts.rmse(test_set[select].values, arima_m1.predict(n_periods=len(test_set))))

        n_periods = len(test_set)
        fc, confint = arima_m1.predict(n_periods=n_periods, return_conf_int=True)

        ff = pd.Series(fc, index=test_set.index)
        lower_series = pd.Series(confint[:, 0], index=test_set.index)
        upper_series = pd.Series(confint[:, 1], index=test_set.index)

        plt.figure(figsize=(12, 8))
        plt.plot(train_set)
        plt.plot(ff, color='red', label='Forecast')
        plt.fill_between(lower_series.index, lower_series, upper_series, color='gray', alpha=.15)
        plt.plot(test_set, 'g--', label='True')
        plt.legend();


if __name__ == '__main__':
    raw_dir = '../data/green_raw/'
    output_dir = '../data/green.parquet'
    nyc_shapefile_dir = '../data/NYC_Shapefile/NYC.shp'
    time_range = '2023-01-01_2023-07-31'

    # Initialize a data_loader
    data_loader = Data_loader.Data_loader(raw_dir=raw_dir, output_dir=output_dir,
                                          nyc_shapefile_dir=nyc_shapefile_dir)
    # Get the data
    df = data_loader.get_final_processed_df(time_range=time_range, export_final=False)

    # Set the period to analyze
    ts_ana_period = '2023-06-01_2023-07-31'
    time_ana = Time_series_analysis(whole_time=ts_ana_period, if_st=False)
