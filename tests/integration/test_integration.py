import pytest
import pickle

from utils import cleaning_utils
import utils.dataloader_utils as dataloader_utils
import utils.df_utils as df_utils
import utils.model_utils as model_utils
import utils

from statsmodels.tsa.deterministic import DeterministicProcess, CalendarFourier
from sklearn.metrics import mean_absolute_error

def test_loading_data():
    '''
    Test that the data loading functions work correctly together.
    '''
    # Test revenue loading
    revenue = dataloader_utils.load_revenue()
    assert not revenue.empty

    expected_columns = ['Date', 'JP', 'Global']
    assert all(col in revenue.columns for col in expected_columns)

    # Test banner loading
    all_banners_en, all_banners_jp = dataloader_utils.load_banners()
    assert not all_banners_en.empty
    assert not all_banners_jp.empty

    expected_columns = ['id', 'gachaType', 'startedAt', 'endedAt', 'rateups', 'startAt', 'endAt']
    assert all(col in all_banners_en.columns for col in expected_columns)
    assert all(col in all_banners_jp.columns for col in expected_columns)

    # Test story loading
    story_jp = dataloader_utils.load_story_jp()
    assert not story_jp.empty

    expected_columns = ['Volume', 'Full Name', 'Chapter', 'Part', 'Release Date']
    assert all(col in story_jp.columns for col in expected_columns)

    # Test event loading
    event_en, event_jp = dataloader_utils.load_events()
    assert not event_en.empty
    assert not event_jp.empty

    expected_columns = ['Name (EN)', 'Start date', 'End date', 'Notes']
    assert all(col in event_en.columns for col in expected_columns)
    assert all(col in event_jp.columns for col in expected_columns)

def test_cleaning_data():
    '''
    Test that the data cleaning functions work correctly together.
    '''
    revenue = pickle.load(open('./data/fixtures/integration_testing/test_cleaning/revenue.pkl', 'rb'))
    revenue = cleaning_utils.drop_global_data_from_revenue(revenue)
    assert 'Global' not in revenue.columns

    story_jp = pickle.load(open('./data/fixtures/integration_testing/test_cleaning/story_jp.pkl', 'rb'))
    story_jp = cleaning_utils.impute_story_part(story_jp)
    assert story_jp['Part'].isnull().sum() == 0

    event_jp = pickle.load(open('./data/fixtures/integration_testing/test_cleaning/event_jp.pkl', 'rb'))
    event_jp = cleaning_utils.remove_rerun_prefix(event_jp)
    event_jp = cleaning_utils.mark_duplicates_as_rerun(event_jp)
    event_jp = cleaning_utils.group_all_operation_events_together(event_jp)

    expected_columns = ['Name (EN)', 'Name (JP)', 'Start date', 'End date', 'Notes']
    assert all(col in event_jp.columns for col in expected_columns)

def test_feature_engineering():
    '''
    Test that the feature engineering functions work correctly together.
    '''
    revenue = pickle.load(open('./data/fixtures/integration_testing/test_feature_engineering/revenue.pkl', 'rb'))
    assert not revenue.empty

    revenue = df_utils.create_fourier_features(revenue)
    for i in range(1, 5):
        assert f'sin({i},freq=YE-DEC)' in revenue.columns
        assert f'cos({i},freq=YE-DEC)' in revenue.columns

    assert revenue.shape[1] == 17

def test_model_training():
    '''
    Test that the model training functions work correctly together.
    '''
    revenue = pickle.load(open('./data/fixtures/integration_testing/test_model_training/revenue.pkl', 'rb'))
    X_train, y_train, X_test, y_test = model_utils.prepare_train_test_split(revenue)
    dp = DeterministicProcess(index=y_train.index, order=1)
    window_size = 7
    trend_model = model_utils.fit_spline_trend_model(y_train, window_size, plot=False, save=False)

    train_residuals = y_train - trend_model.predict(dp.in_sample())
    test_residuals = y_test - trend_model.predict(dp.out_of_sample(steps=6))

    revenue_2 = model_utils.create_XGB_features(revenue)
    X_train2 = revenue_2.iloc[:-6].drop(columns=['JP'])
    X_test2 = revenue_2.iloc[-6:].drop(columns=['JP'])

    y_train2 = train_residuals.iloc[X_train2.index]
    y_test2 = test_residuals

    xgb_model = model_utils.fit_XGB_residual_model(X_train2, y_train2)

    final_pred = model_utils.final_prediction(trend_model, xgb_model, X_test2, dp)

    assert len(final_pred) == 6

    mae_final = mean_absolute_error(y_test, final_pred)

    assert mae_final < 3000000 # just to make sure that MAE is not ridiculous 




    



    


    

