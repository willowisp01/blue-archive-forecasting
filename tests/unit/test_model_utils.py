import numpy as np
import pandas as pd
import pandas.testing as pdt
import utils.model_utils as model_utils

def test_prepare_train_test_split():
    df = pd.DataFrame(
        {'Date': pd.date_range(start='2021-01-01', periods=12, freq='MS'),
        'JP': np.arange(1000, 2200, 100),
        'Feature1': np.arange(10, 22),
        'Feature2': np.arange(20, 32)},
        index=np.arange(12))
    
    X_train, y_train, X_test, y_test = model_utils.prepare_train_test_split(df)

    expected_X_train = df.iloc[:-6].drop(columns=['Date', 'JP'])
    expected_y_train = df.iloc[:-6]['JP']
    expected_X_test = df.iloc[-6:].drop(columns=['Date', 'JP'])
    expected_y_test = df.iloc[-6:]['JP']

    pdt.assert_frame_equal(X_train.reset_index(drop=True), expected_X_train.reset_index(drop=True))
    pdt.assert_series_equal(y_train.reset_index(drop=True), expected_y_train.reset_index(drop=True))
    pdt.assert_frame_equal(X_test.reset_index(drop=True), expected_X_test.reset_index(drop=True))
    pdt.assert_series_equal(y_test.reset_index(drop=True), expected_y_test.reset_index(drop=True))


def test_drop_columns_residual():
    df = pd.DataFrame(
        {'Date': pd.to_datetime('2021-11-01 00:00:00'),
        'JP': 3000000.0,
        'Pickup Banner Count': 4,
        'Limited Banner Count': 1,
        'Fes Banner Count': 0,
        'Original Count': 1,
        'Collaboration Event Count': 1,
        'Operation Count': 1,
        'Rerun Count': 0,
        'sin(1,freq=YE-DEC)': -0.8674563547295971,
        'cos(1,freq=YE-DEC)': 0.4975132889071803,
        'sin(2,freq=YE-DEC)': -0.863142128049911,
        'cos(2,freq=YE-DEC)': -0.5049610547215212,
        'sin(3,freq=YE-DEC)': 0.008606996888690521,
        'cos(3,freq=YE-DEC)': -0.9999629591162655,
        'sin(4,freq=YE-DEC)': 0.8717063187093227,
        'cos(4,freq=YE-DEC)': -0.4900286664290578},
        index=[0])
    
    result_df = model_utils.drop_columns_residual(df)

    columns_dropped = ['Rerun Count', 
                        'Operation Count', 
                        'Collaboration Event Count',
                        'Limited Banner Count',
                        'sin(1,freq=YE-DEC)',
                        'cos(1,freq=YE-DEC)',
                        'sin(3,freq=YE-DEC)',
                        'cos(3,freq=YE-DEC)',
                        'sin(4,freq=YE-DEC)',
                        'Date']
    
    assert all(col not in result_df.columns for col in columns_dropped)
    assert len(df) == len(result_df)

def test_make_lags():
    df = pd.DataFrame(
        {'Date': pd.to_datetime(['2021-11-01', '2021-11-02', '2021-11-03', '2021-11-04', '2021-11-05']),
        'JP': [3000000.0, 3200000.0, 3100000.0, 3300000.0, 3400000.0]},
        index=[0, 1, 2, 3, 4])
    
    lags = [1, 2]
    result_df = model_utils.make_lags(df, lags)

    expected_lag1 = pd.Series([np.nan, 3000000.0, 3200000.0, 3100000.0, 3300000.0])
    expected_lag2 = pd.Series([np.nan, np.nan, 3000000.0, 3200000.0, 3100000.0])

    pdt.assert_series_equal(result_df['lag1'], expected_lag1, check_names=False)
    pdt.assert_series_equal(result_df['lag2'], expected_lag2, check_names=False)
    pdt.assert_series_equal(df['JP'], result_df['JP'], check_names=False)

def test_make_rolling_stats():
    df = pd.DataFrame(
        {'Date': pd.to_datetime(['2021-11-01', '2021-11-02', '2021-11-03', '2021-11-04', '2021-11-05']),
        'JP': [1.0, 2.0, 3.0, 4.0, 5.0]},
        index=[0, 1, 2, 3, 4])
    
    window_size = 3
    result_df = model_utils.make_rolling_stats(df, window_size)

    # expected_rolling_mean = pd.Series([np.nan, np.nan, 2.0, 3.0, 4.0])
    expected_rolling_std = pd.Series([np.nan, np.nan, np.nan, 1.0, 1.0])

    # pdt.assert_series_equal(result_df['rolling_mean'], expected_rolling_mean, check_names=False)
    pdt.assert_series_equal(result_df[f'rolling_std_{window_size}'], expected_rolling_std, check_names=False)
    pdt.assert_series_equal(df['JP'], result_df['JP'], check_names=False)

