import pandas as pd
import requests

def load_revenue() -> pd.DataFrame:
    '''
    Loads revenue into dataframes from excel files.

    Returns
    -------
    pd.DataFrame
        The revenue dataframe.
    '''
    reddit_data = pd.read_excel('./data/reddit-monthly-revenue-report.xlsx', engine='openpyxl').iloc[:, :3]
    ennead_data = pd.read_excel('./data/revenue-ennead-cc-revenue-report.xlsx', engine='openpyxl')
    revenue = pd.concat([reddit_data, ennead_data], ignore_index=True)
    return revenue

def load_banners() -> tuple[pd.DataFrame, pd.DataFrame]:
    '''
    Attempts to load fresh banner information from an API.

    If unsuccessful, loads a serialized df of banner info.

    Returns
    -------
    pd.DataFrame, pd.DataFrame
        The banner dataframes for EN and JP regions respectively.
    '''

    try:
        # raise Exception("Simulated API failure for testing purposes.")
        banner_en = requests.get('https://api.ennead.cc/buruaka/banner').json()
        all_banners_en = banner_en['ended'] + banner_en['current'] + banner_en['upcoming']
        all_banners_en = pd.DataFrame(all_banners_en)

        all_banners_en['startAt'] = pd.to_datetime(all_banners_en['startedAt'], unit='ms')
        all_banners_en['endAt'] = pd.to_datetime(all_banners_en['endedAt'], unit='ms')
        all_banners_en = all_banners_en.sort_values(by='startAt')

        banner_jp = requests.get('https://api.ennead.cc/buruaka/banner?region=japan').json()
        all_banners_jp = banner_jp['ended'] + banner_jp['current'] + banner_jp['upcoming']
        all_banners_jp = pd.DataFrame(all_banners_jp)

        all_banners_jp['startAt'] = pd.to_datetime(all_banners_jp['startedAt'], unit='ms')
        all_banners_jp['endAt'] = pd.to_datetime(all_banners_jp['endedAt'], unit='ms')
        all_banners_jp = all_banners_jp.sort_values(by='startAt')

        # serialize data (in case API goes down in the future)
        all_banners_en.to_pickle('./data/fixtures/all_banners_en.pkl')
        all_banners_jp.to_pickle('./data/fixtures/all_banners_jp.pkl')

    except Exception as e:
        print(Exception, ": ", e)
        print("Serialized banner data will be used instead.")
        all_banners_en = pd.read_pickle('./data/fixtures/all_banners_en.pkl')
        all_banners_jp = pd.read_pickle('./data/fixtures/all_banners_jp.pkl')
        
    return all_banners_en, all_banners_jp

def load_story_jp() -> pd.DataFrame:
    '''
    Loads story data for the JP region.

    Returns
    -------
    pd.DataFrame
        The story dataframe for the JP region.
    '''
    story_jp = pd.read_excel('./data/story-jp.xlsx').iloc[:, :5]
    return story_jp

def load_events() -> tuple[pd.DataFrame, pd.DataFrame]:
    '''
    Loads event data for both EN and JP regions.
    
    Returns
    -------
    pd.DataFrame, pd.DataFrame
        The event dataframes for EN and JP regions respectively.
    '''
    event_en = pd.read_excel('./data/event-en.xlsx')
    event_jp = pd.read_excel('./data/event-jp.xlsx').iloc[:, :5]
    return event_en, event_jp

def categorize_banners(banners_df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    '''
    Categorizes banners by gacha type.

    A dict with keys 'fes', 'pickup', and 'limited' is created. 
    They point to their respective dataframes.

    Parameters
    ----------
    banners_df : pd.DataFrame
        The dataframe containing banner information.

    Returns
    -------
    dict[str, pd.DataFrame]
        A dictionary categorizing banners by gacha type, with keys 'fes', 'pickup', and 'limited'.
    '''
    
    fes_banners_jp = banners_df[banners_df['gachaType'] == 'FesGacha']
    pickup_banners_jp = banners_df[banners_df['gachaType'] == 'PickupGacha']
    limited_banners_jp = banners_df[banners_df['gachaType'] == 'LimitedGacha']

    return {'fes': fes_banners_jp, 
            'pickup': pickup_banners_jp, 
            'limited': limited_banners_jp}