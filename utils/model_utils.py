from __future__ import annotations

from sklearn.preprocessing import SplineTransformer
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from statsmodels.tsa.deterministic import CalendarFourier, DeterministicProcess
from xgboost import XGBRegressor

import joblib
import pandas as pd
import statsmodels
import seaborn as sns
import matplotlib.pyplot as plt

def prepare_train_test_split(revenue):
    revenue = revenue.copy()

    revenue_train = revenue.iloc[:-6] # everything before 6 months for training
    revenue_test = revenue.iloc[-6:] # last 6 months for testing

    X_train = revenue_train.drop(columns=['Date', 'JP'])
    y_train = revenue_train['JP']

    X_test = revenue_test.drop(columns=['Date', 'JP'], errors='ignore')
    y_test = revenue_test['JP']

    return X_train, y_train, X_test, y_test

def drop_columns_residual(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Drop columns that are not needed for residual analysis.
    Does not drop the target column yet (this is needed to make lags later)

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame.

    Returns
    -------
    pd.DataFrame
        The DataFrame with specified columns dropped.
    '''
    columns_to_drop = ['Rerun Count', 
                        'Operation Count', 
                        'Collaboration Event Count',
                        'Limited Banner Count',
                        'sin(1,freq=YE-DEC)',
                        'cos(1,freq=YE-DEC)',
                        'sin(3,freq=YE-DEC)',
                        'cos(3,freq=YE-DEC)',
                        'sin(4,freq=YE-DEC)'
                        ]
    
    df2 = df.copy()
    df2 = df2.drop(columns=['Date'])
    df2 = df2.drop(columns=columns_to_drop)
    return df2

def make_lags(df: pd.DataFrame, lags: list) -> pd.DataFrame:
    '''
    Create lagged features for the target variable.

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame containing the target variable.
    lags : list
        A list of integers representing the lag periods.
        (e.g. lag1, lag6, etc.)

    Returns
    -------
    pd.DataFrame
        The DataFrame with lagged features added.
    '''
    df_copy = df.copy()
    for i in lags:
        df_copy[f'lag{i}'] = df_copy['JP'].shift(i)
    return df_copy

def make_rolling_stats(df: pd.DataFrame, window_size: int) -> pd.DataFrame:
    '''
    Creates rolling statistics of window_size, such as rolling
    std and mean.

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame.
    window_size : int
        The size of the rolling window.

    Returns
    -------
    pd.DataFrame
        The dataframe with rolling statistics added.
    '''
    df_copy = df.copy()
    # df_copy[f'rolling_mean_{window_size}'] = df_copy['JP'].shift(1).rolling(window=window_size).mean()
    
    # shift by 1 to avoid data leakage
    df_copy[f'rolling_std_{window_size}'] = df_copy['JP'].shift(1).rolling(window=window_size).std()
    return df_copy


def fit_spline_trend_model(y_train, window_size=7, plot=True, save=True):

    linear_regressor = LinearRegression()

    trend = y_train.rolling(window=window_size, center=True).mean()

    dp = DeterministicProcess(index=y_train.index, order=1)
    time_index = dp.in_sample() # points to fit for trend (which is a time index)

    # remove first few and last rows to align with rolling mean
    time_index_aligned = time_index.iloc[(window_size//2):-(window_size//2)] 
    time_index_aligned_array = time_index_aligned.to_numpy().reshape(-1, 1).astype(int)
    time_index_aligned_array

    # spline transformer with 2 knots
    spline_transformer = SplineTransformer(degree=1, n_knots=7, knots='quantile',
                                        include_bias=False, extrapolation='continue')

    trend_model = make_pipeline(spline_transformer, linear_regressor)
    trend_model.fit(time_index_aligned_array, trend.dropna())

    if save:
        joblib.dump(trend_model, 'data/saved_models/trend_model.joblib')

    if plot:
        sns.lineplot(trend_model.predict(time_index), label='Spline Trend')
        sns.lineplot(y_train, label='Actual Revenue')
        plt.title('Revenue vs Spline Trend (Training Set)')
        plt.show()

    return trend_model

def create_XGB_features(revenue):
    revenue = revenue.copy()

    # Drop uninformative columns
    revenue = drop_columns_residual(revenue)

    # Add lag features
    lags = [6]
    revenue = make_lags(revenue, lags)

    # Add rolling statistics
    revenue = make_rolling_stats(revenue, window_size=4)
    
    # Drop rows with NaN values
    revenue = revenue.dropna()

    return revenue


def fit_XGB_residual_model(X_train, y_train, save=True):

    xgb_model = XGBRegressor(
        n_estimators=40,
        # max_depth=6,
        learning_rate=0.1
    )

    xgb_model.fit(X_train, y_train)

    if save:
        joblib.dump(xgb_model, 'data/saved_models/xgb_residual_model.joblib')

    return xgb_model

def final_prediction(trend_model, residual_model, X_test2: pd.DataFrame, dp: statsmodels.tsa.deterministic.DeterministicProcess) -> pd.DataFrame:
    '''
    Make the final prediction for next 6 months of data
    by combining both trend and residual predictions. 

    Parameters
    ----------
    trend_model
        The trend model used for prediction.
    residual_model
        The residual model used for prediction.
    X_test2 : pd.DataFrame
        The test data for the residual model.
    dp : DeterministicProcess
        The DeterministicProcess, to be used for out-of-sample prediction.

    Returns
    -------
    pd.DataFrame
        A DataFrame containg the final prediction of revenue.
    '''

    trend_pred = trend_model.predict(dp.out_of_sample(steps=6))
    residual_pred = residual_model.predict(X_test2)
    final_pred = trend_pred + residual_pred
    return final_pred