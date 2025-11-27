import pytest
import pickle

import utils.dataloader_utils as dataloader_utils
import utils.df_utils as df_utils
import utils.model_utils as model_utils
import utils

from statsmodels.tsa.deterministic import DeterministicProcess, CalendarFourier

def test_loading_data():
    '''
    Test that the data loading functions work correctly.
    '''
    revenue = dataloader_utils.load_revenue()
    assert not revenue.empty
    


    

