import pandas as pd
import utils.df_utils as df_utils

def test_group_into_monthly_count():
    pickup_banners_jp = pd.DataFrame(
        {'id': {416: 50004, 415: 50005, 414: 50011, 413: 50001, 412: 50013},
        'gachaType': 
            {416: 'PickupGacha',
            415: 'PickupGacha',
            414: 'PickupGacha',
            413: 'PickupGacha',
            412: 'PickupGacha'},
        'startedAt': 
            {416: 1612425600000,
            415: 1613026800000,
            414: 1614234600000,
            413: 1615091400000,
            412: 1615437000000},
        'endedAt': 
            {416: 1613023199000,
            415: 1614232860000,
            414: 1615435200000,
            413: 1619668800000,
            412: 1616040000000},
        'rateups': 
            {416: ['シロコ', 'ホシノ'],
            415: ['マシロ'],
            414: ['イズナ', 'シズコ'],
            413: ['チェリノ'],
            412: ['ハルナ']},
        'startAt': 
            {416: pd.to_datetime('2021-02-04 08:00:00'),
            415: pd.to_datetime('2021-02-11 07:00:00'),
            414: pd.to_datetime('2021-02-25 06:30:00'),
            413: pd.to_datetime('2021-03-07 04:30:00'),
            412: pd.to_datetime('2021-03-11 04:30:00')},
        'endAt': 
            {416: pd.to_datetime('2021-02-11 05:59:59'),
            415: pd.to_datetime('2021-02-25 06:01:00'),
            414: pd.to_datetime('2021-03-11 04:00:00'),
            413: pd.to_datetime('2021-04-29 04:00:00'),
            412: pd.to_datetime('2021-03-18 04:00:00')}},
        index=[416, 415, 414, 413, 412])
    
    revenue = pd.DataFrame(
        {'Date': {
            0: pd.to_datetime('2021-01-01 00:00:00'),
            1: pd.to_datetime('2021-02-01 00:00:00'),
            2: pd.to_datetime('2021-03-01 00:00:00'),
            3: pd.to_datetime('2021-04-01 00:00:00'),
            4: pd.to_datetime('2021-05-01 00:00:00')},
        'JP': {
            0: 1.0,
            1: 2.0,
            2: 3.0,
            3: 4.0,
            4: 5.0
        }},
        index=[0, 1, 2, 3, 4]
    )
    
    result_df = df_utils.group_into_monthly_count(pickup_banners_jp, revenue)
    print()

    # Index 414 extends into march, so March should have 3 pickup banners. 
    # This logic applies for other grouping functions as well.
    expected_counts = [0, 3, 3, 1, 0]

    assert result_df['Banner Count'].tolist() == expected_counts

def test_group_event_into_monthly_count():
    original_events_jp = pd.DataFrame(
        {'Name (EN)': {
            0: 'Cherry Blossom Festival Commotion! ~Flowers in the Sky, Ninja on the Ground~',
            1: 'Revolutionary Ivan Kupala: Moustache, Pudding and Red Winter',
            2: "Summer Sky's Wishlist",
            3: "～Emergency Special Order of the Disciplinary committee Officer～ President Hina's Summer Vacation!",
            4: 'Catch in Neverland'},
        'Name (JP)': {
            0: '桜花爛漫お祭り騒ぎ！~空に徒花 地に忍び~',
            1: '革命のイワン・クパーラ 髭とプリンとレッドウィンター',
            2: '夏空のウィッシュリスト',
            3: '～風紀委員会行政官緊急特務命令～\u3000ヒナ委員長のなつやすみっ！',
            4: 'ネバーランドでつかまえて'},
        'Start date': {
            0: pd.to_datetime('2021-02-25 00:00:00'),
            1: pd.to_datetime('2021-04-29 00:00:00'),
            2: pd.to_datetime('2021-06-30 00:00:00'),
            3: pd.to_datetime('2021-07-29 00:00:00'),
            4: pd.to_datetime('2021-08-26 00:00:00')},
        'End date': {
            0: pd.to_datetime('2021-03-11 00:00:00'),
            1: pd.to_datetime('2021-05-13 00:00:00'),
            2: pd.to_datetime('2021-07-15 00:00:00'),
            3: pd.to_datetime('2021-08-12 00:00:00'),
            4: pd.to_datetime('2021-09-09 00:00:00')},
        'Notes': {
            0: 'Original',
            1: 'Original',
            2: 'Original',
            3: 'Original',
            4: 'Original'}},
            index=[0, 1, 2, 3, 4]
        )
    
    revenue = pd.DataFrame(
        {'Date': {
            0: pd.to_datetime('2021-01-01 00:00:00'),
            1: pd.to_datetime('2021-02-01 00:00:00'),
            2: pd.to_datetime('2021-03-01 00:00:00'),
            3: pd.to_datetime('2021-04-01 00:00:00'),
            4: pd.to_datetime('2021-05-01 00:00:00'),
            5: pd.to_datetime('2021-06-01 00:00:00'),
            6: pd.to_datetime('2021-07-01 00:00:00'),
            7: pd.to_datetime('2021-08-01 00:00:00'),
            8: pd.to_datetime('2021-09-01 00:00:00'),
            9: pd.to_datetime('2021-10-01 00:00:00')},
        'JP': {
            0: 1.0,
            1: 2.0,
            2: 3.0,
            3: 4.0,
            4: 5.0,
            5: 6.0,
            6: 7.0,
            7: 8.0,
            8: 9.0,
            9: 10.0
        }},
        index=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    )

    result_df = df_utils.group_event_into_monthly_count(original_events_jp, revenue)
    assert result_df['Event Count'].tolist() == [0, 1, 1, 1, 1, 1, 2, 2, 1, 0]
    
