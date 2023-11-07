import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from my_scripts.Data_loader import Data_loader
from my_scripts import ts
from statsmodels.tsa.seasonal import seasonal_decompose, STL
from statsmodels.tsa.arima_model import ARIMA
import pmdarima as pm
import numpy as np
import calendar

borough_lst = ['Bronx', 'Brooklyn', 'Manhattan', 'Queens']


class Time_series_analysis(Data_loader):
    def __init__(self, raw_dir, output_dir, nyc_shapefile_dir, data, pred_time_range=None, if_st=True):
        Data_loader.__init__(self, raw_dir, output_dir, nyc_shapefile_dir)
        # noinspection PyCompatibility
        super().__init__(raw_dir, output_dir, nyc_shapefile_dir)
        self.data = data
        self.if_st = if_st
        self.pred_time_range = pred_time_range
        self.rmse_mean = None
        self.rmse_snaive = None
        self.rmse_arima = None

    def data_pivot(self, dt):
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

    def time_series(self, temp_df, select, item_title):
        fig1 = plt.figure(figsize=(10, 5))
        temp_df[select].plot(title=item_title, marker='o', ms=3, legend=False)
        plt.tight_layout()
        if self.if_st:
            st.pyplot(fig1)
        else:
            fig.show()

    def season_plot(self, temp_df, item_title, sample='M'):
        t_select = temp_df.columns[0]
        temp_df = temp_df.resample(sample).sum()
        temp_df.loc[:, 'year'] = temp_df.index.year
        temp_df.loc[:, 'month'] = temp_df.index.month

        yrs = np.sort(temp_df.year.unique())
        color_ids = np.linspace(0, 1, num=len(yrs))
        colors_to_use = plt.cm.plasma(color_ids)

        fig2 = plt.figure(figsize=(12, 8))

        for i, yr in enumerate(yrs):
            df_tmp = temp_df.loc[temp_df.year == yr, :]
            plt.plot(df_tmp.month, df_tmp[t_select], color=colors_to_use[i])
            plt.text(12.1, df_tmp[t_select][-1], str(yr), color=colors_to_use[i])
        plt.title('Season Plot: {}'.format(item_title))
        plt.xlim(0, 13)
        plt.xticks(np.arange(1, 13), calendar.month_abbr[1:13])
        if self.if_st:
            st.pyplot(fig2)
        else:
            plt.show()

    def seasonal_decompose_plot(self, temp_df, item_title, sample='M'):
        temp_df = temp_df.resample(sample).sum()
        temp_df_add = seasonal_decompose(temp_df.loc[:, temp_df.columns[0]],
                                         model='additive',
                                         extrapolate_trend='freq')
        # temp_df_add.plot();
        fig3, (ax0, ax1, ax2, ax3) = plt.subplots(4, 1, figsize=(12, 9))
        temp_df_add.observed.plot(ax=ax0)
        ax0.title.set_text('Seasonal Decompose Plot: {}'.format(item_title))
        temp_df_add.trend.plot(ax=ax1)
        ax1.set_ylabel('Trend')
        temp_df_add.seasonal.plot(ax=ax2)
        ax2.set_ylabel('Seasonal')
        temp_df_add.resid.plot(ax=ax3, lw=0, marker="o")
        ax3.axhline(y=0, color='black')
        ax3.set_ylabel('Resid')
        if self.if_st:
            st.pyplot(fig3)
        else:
            plt.show()

    def seasonal_naive_pred(self, temp_df, select, item_title,
                            sample='D',
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

        # Save the rmse of mean and snaive prediction
        self.rmse_mean = ts.rmse(test_set[select].values, mean_forecast)
        self.rmse_snaive = ts.rmse(test_set[select].values, snaive_forecast)

        # Plot the predictions and true values
        fig1 = lt.figure(figsize=(12, 8))
        ax = train_set[select].plot(
            title='Seasonal Naive Prediction: {}'.format(item_title), legend=False)
        test_set[select].plot(ax=ax, legend=False, style='--')
        mean_forecast.plot(ax=ax, legend=False, style='-')
        snaive_forecast.plot(ax=ax, legend=False, style='-')
        plt.legend(labels=['train', 'test', 'mean', 'snaive'], loc='lower right')
        if self.if_st:
            st.pyplot(fig1)
        else:
            plt.show()

        print('{0},mean: {1:.3f}'.format(ts.rmse.__name__, self.rmse_mean))
        print('{0},snaive: {1:.3f}'.format(ts.rmse.__name__, self.rmse_snaive))
        print('---')

        return mean_forecast, snaive_forecast

    def arima_pred(self, temp_df, select, item_title, sample='D', m=7, test_train_rate=1 / 10):
        temp_df = temp_df.resample(sample).sum()
        cut_point = int(len(temp_df) * test_train_rate)
        train_set = temp_df.iloc[:-cut_point, ]
        test_set = temp_df.iloc[-cut_point:, ]

        # Train the arima model on the train set
        arima_m1 = pm.auto_arima(train_set.values, seasonal=True, m=m, test='adf', suppress_warnings=True)

        # Use the trained arima model to do the prediction
        n_periods = len(test_set)
        fc, confint = arima_m1.predict(n_periods=n_periods, return_conf_int=True)

        # Save the rmse of arima
        self.rmse_arima = ts.rmse(test_set[select].values, arima_m1.predict(n_periods=len(test_set)))

        # Set the attributes for the prediction figure
        ff = pd.Series(fc, index=test_set.index)
        lower_series = pd.Series(confint[:, 0], index=test_set.index)
        upper_series = pd.Series(confint[:, 1], index=test_set.index)

        fig2 = plt.figure(figsize=(12, 8))
        plt.plot(train_set)
        plt.plot(ff, color='red', label='Forecast')
        plt.fill_between(lower_series.index, lower_series, upper_series, color='gray', alpha=.15)
        plt.plot(test_set, 'g--', label='True')
        plt.title(title='Arima Prediction: {}'.format(item_title))
        plt.legend()
        if self.if_st:
            st.pyplot(fig2)
        else:
            plt.show()

        print('{0},snaive: {1:.3f}'.format(ts.rmse.__name__, self.rmse_arima))
        print('---')

        return arima_m1


if __name__ == '__main__':
    raw_dir = '../data/green_raw/'
    output_dir = '../data/green.parquet'
    nyc_shapefile_dir = '../data/NYC_Shapefile/NYC.shp'
    # time_range = '2023-01-01_2023-07-31'

    # Initialize a data_loader
    data_loader = Data_loader.Data_loader(raw_dir=raw_dir, output_dir=output_dir,
                                          nyc_shapefile_dir=nyc_shapefile_dir)
    # Get the data
    df_new = data_loader.get_final_processed_df(time_range=time_range, export_final=False)

    dt = df_new.copy()

    # dt = df_new[(df_new['DATE'] >= '2023-01-01') & (df_new['DATE'] <= '2023-06-01')].reset_index(drop=True)
    filter_con = 'Counts'
    select = borough_lst[2]

    pivot_counts, pivot_fare = data_pivot(dt)
    item_title, temp_df = select_df(filter_con, select, pivot_counts, pivot_fare)

    # Set the period to analyze
    ts_ana_period = '2023-06-01_2023-07-31'
    time_ana = Time_series_analysis(whole_time=ts_ana_period, if_st=False)

    # 1.Time Series Analysis

    # 1)original time series
    time_series(temp_df)
    # 2)seasonal analysis
    season_plot(temp_df, sample='M')
    # 3)decompose analysis
    seasonal_decompose_plot(temp_df, sample='M')

    # 2.Prediction

    dt = df_new[(df_new['DATE'] >= '2023-01-01') & (df_new['DATE'] <= '2023-06-01')].reset_index(drop=True)
    filter_con = 'Counts'
    select = borough_lst[2]

    pivot_counts, pivot_fare = data_pivot(dt)
    item_title, temp_df = select_df(filter_con, select, pivot_counts, pivot_fare)

    # 1)snaive
    m, sn = seasonal_naive_pred(temp_df, sample='D', regular_period=7, test_train_rate=1 / 10)

    # 2)arima
    arima_m1 = arima_pred(temp_df, m=7, test_train_rate=1 / 10)
    print(arima_m1.summary())

    arima_m1.plot_diagnostics(figsize=(12, 8))

    arima_draw(temp_df)

    print('rmse:')
    print('mean', ts.rmse(test_set[select].values, m))
    print('snaive', ts.rmse(test_set[select].values, sn))
    print('arima', ts.rmse(test_set[select].values, arima_m1.predict(n_periods=len(test_set))))
