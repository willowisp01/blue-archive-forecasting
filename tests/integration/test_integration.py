import pytest
import pickle

import utils.df_utils as df_utils
import utils.model_utils as model_utils

from statsmodels.tsa.deterministic import DeterministicProcess, CalendarFourier

def test_loading_data():
    '''
    Test that the data loading functions work correctly.
    '''
    # revenue = df_utils.load_revenue_data('data/revenue.csv')


    

