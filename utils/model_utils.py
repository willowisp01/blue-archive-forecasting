from __future__ import annotations

import pandas as pd
import statsmodels

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