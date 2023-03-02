import pytest
import polars as pl
import numpy as np
from proxiflow.config import Config
from proxiflow.core import Engineer

CONFIG_FILE_PATH = "tests/data/config.yaml"

@pytest.fixture(scope="module")
def config():
    return Config(CONFIG_FILE_PATH)


class TestEngineer():
    """
    A test class for the Engineer class in the proxiflow library.
    """
    def test_one_hot_encode(self, config):
        # Create a sample DataFrame with categorical columns
        df = pl.DataFrame({
            'category1': ['a', 'b', 'a', 'c', 'c', 'a'],
            'category2': ['x', 'y', 'y', 'z', 'x', 'y'],
            'num1': [1, 2, 3, 4, 5, 6],
            'num2': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
        })
        expected = pl.DataFrame({
            'category1': ['a', 'b', 'a', 'c', 'c', 'a'],
            'category2_x': [1, 0, 0, 0, 1, 0],
            'category2_y': [0, 1, 1, 0, 0, 1],
            'category2_z': [0, 0, 0, 1, 0, 0],
            'num1': [1, 2, 3, 4, 5, 6],
            'num2': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
        })
        engineer = Engineer(config)
        engineered_result = engineer.one_hot_encode(df, ['category2'])
        assert expected.frame_equal(engineered_result)