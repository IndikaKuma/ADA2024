# content of test_sysexit.py
import os
import pytest
import pandas as pd

# content of test_class.py
import diabetes_predictor


class TestDiabetesPredictor:

    @pytest.fixture(scope="session", autouse=True)
    def execute_before_any_test(self):
        os.environ["MODEL_NAME"] = "testResources/model.h5"

    # your setup code goes here, executed ahead of the first test
    def test_predict_single_record(self):
        with open('testResources/prediction_request.json') as json_file:
            data = pd.read_json(json_file)
        dp = diabetes_predictor.DiabetesPredictor()
        status = dp.predict_single_record(data)
        assert bool(status[0]) is not None
       # assert bool(status[0]) is False
