import pandas as pd
from scipy.signal import periodogram
from statsmodels.tsa.deterministic import CalendarFourier, DeterministicProcess

def create_fourier_features(revenue):
    fourier = CalendarFourier(freq="YE", order=4)

    revenue_copy = revenue.copy()
    revenue_copy = revenue_copy.set_index('Date').asfreq('MS')

    dp = DeterministicProcess(
        index=revenue_copy.index,
        constant=False,
        order=0,
        seasonal=False,
        additional_terms=[fourier],
        drop=True,
    )
    X = dp.in_sample()
    
    revenue = revenue.merge(X, left_on='Date', right_index=True) # similar to SQL inner join

    return revenue

def group_into_monthly_count(banners: pd.DataFrame, revenue: pd.DataFrame) -> pd.DataFrame:
    '''
    Group the banner events into monthly counts.

    For example, if 3 banners occur during March 2023, the 
    result will have a row for March 2023 with a count of 3.

    Parameters
    ----------
    banners : pd.DataFrame
        The input DataFrame containing banner event data.

    revenue : pd.DataFrame
        The revenue DataFrame.

    Returns
    -------
    pd.DataFrame
        A DataFrame with monthly counts of banner events.
    '''
    
    monthly_count = pd.DataFrame(revenue['Date'])
    monthly_count['Banner Count'] = 0
    for banner in banners.iterrows():
        start_month = banner[1]['startAt'].to_period('M').to_timestamp()
        end_month = banner[1]['endAt'].to_period('M').to_timestamp()
        if start_month == end_month:
            if start_month in monthly_count['Date'].values:
                monthly_count.loc[monthly_count['Date'] == start_month, 'Banner Count'] += 1
        else:
            if start_month in monthly_count['Date'].values:
                monthly_count.loc[monthly_count['Date'] == start_month, 'Banner Count'] += 1
            if end_month in monthly_count['Date'].values:
                monthly_count.loc[monthly_count['Date'] == end_month, 'Banner Count'] += 1

    return monthly_count

def group_event_into_monthly_count(events: pd.DataFrame, revenue: pd.DataFrame) -> pd.DataFrame:
    '''
    Group events into monthly counts.

    For example, if 3 events occur during March 2023, the 
    result will have a row for March 2023 with a count of 3.

    Parameters
    ----------
    events : pd.DataFrame
        The input DataFrame containing event data.

    revenue : pd.DataFrame
        The revenue DataFrame.

    Returns
    -------
    pd.DataFrame
        A DataFrame with monthly counts of events.
    '''
    
    monthly_count = pd.DataFrame(revenue['Date'])
    monthly_count['Event Count'] = 0
    for event in events.iterrows():
        start_month = event[1]['Start date'].to_period('M').to_timestamp()
        end_month = event[1]['End date'].to_period('M').to_timestamp()
        if start_month == end_month:
            if start_month in monthly_count['Date'].values:
                monthly_count.loc[monthly_count['Date'] == start_month, 'Event Count'] += 1
        else:
            if start_month in monthly_count['Date'].values:
                monthly_count.loc[monthly_count['Date'] == start_month, 'Event Count'] += 1
            if end_month in monthly_count['Date'].values:
                monthly_count.loc[monthly_count['Date'] == end_month, 'Event Count'] += 1

    return monthly_count