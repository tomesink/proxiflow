import pytest
import polars as pl
import numpy as np
from proxiflow.config import Config
from proxiflow.core import Normalizer
# from proxiflow.core.core_utils import check_columns

CONFIG_FILE_PATH = "tests/data/config.yaml"

@pytest.fixture(scope="module")
def config():
    return Config(CONFIG_FILE_PATH)


class TestNormalizer():
    """
    A test class for the Normalizer class in the proxiflow library.
    """

    def test_min_max_normalize(self, config):
        df = pl.DataFrame({
            'col1': [1, 2, 3, 4, 5],
            'col2': [6, 7, 8, 9, 10],
            'col3': [1.1, 2.2, 3.3, 4.4, 5.5]
        })
        expected = pl.DataFrame({
            'col1': [0.0, 0.25, 0.5, 0.75, 1.0],
            'col2': [0.0, 0.25, 0.5, 0.75, 1.0],
            'col3': [0.0, 0.25, 0.5, 0.75, 1.0]
        })
        normalizer = Normalizer(config)
        normalized_result = normalizer._min_max_normalize(df, ['col1', 'col2', 'col3'])
        normalized_result = normalized_result.to_numpy()
        expected = expected.to_numpy()
        np.testing.assert_allclose(normalized_result, expected, rtol=1e-5, atol=1e-8)

    def test_z_score_normalize(self, config):
        # Create test data
        df = pl.DataFrame({
            'A': [163, 120, 130, 108, 109],
            'B': [163, 153, 199, 188, 171],
            'C': [1.59, 1.81, 1.08, 1.57, 1.19]
        })
        
        # Create expected output
        expected = pl.DataFrame({
            'A': [1.834473, -0.297482, 0.198321, -0.892446, -0.842866],
            'B': [-0.708023, -1.308042, 1.452046, 0.792025, -0.228007],
            'C': [0.523362, 1.334205, -1.356319, 0.449649, -0.950897]
        })
        # Normalize the data using z-score
        normalizer = Normalizer(config)
        normalized_result = normalizer._z_score_normalize(df, ['A', 'B', 'C'])
        # Compare the result with the expected output
        normalized_result = normalized_result.to_numpy()
        expected = expected.to_numpy()
        np.testing.assert_allclose(normalized_result, expected, rtol=1e-5, atol=1e-8)


    def test_log_normalize(self, config):
        # Define the input DataFrame
        df = pl.DataFrame({
            'col1': [1, 2, 3, 4, 5],
            'col2': [6, 7, 8, 9, 10],
            'col3': [11, 12, 13, 14, 15]
        })
        # Define the expected output DataFrame
        expected_df = pl.DataFrame({
            'col1': [0.0, 0.405465, 0.693147, 0.916291, 1.098612],
            'col2': [1.252763, 1.386294, 1.504077, 1.609438, 1.704748],
            'col3': [1.791759, 1.871802, 1.94591, 2.014903, 2.079442]
        })
        # Create the Normalizer object and apply log normalization to the input DataFrame
        normalizer = Normalizer(config)
        normalized_result = normalizer._log_normalize(df, ['col1', 'col2', 'col3'])
        # Check that the output DataFrame is equal to the expected DataFrame
        np.testing.assert_allclose(normalized_result.to_numpy(), expected_df.to_numpy(), rtol=1e-5, atol=1e-8)
    
    # def test_check_columns(self, config):
    #     df = pl.DataFrame({
    #         'col1': [1, 2, 3],
    #         'col2': [4, 5, 6],
    #         'col3': [7, 8, 9]
    #     })
    #     normalizer = Normalizer(config)
    #     columns = ['col6', 'col5', 'col4']
    #     with pytest.raises(ValueError):
    #         normalizer._check_columns(df, [columns])
        
    #     columns = ['col1', 'col4']
    #     expected = ['col1']
    #     result = normalizer._check_columns(df, columns)
    #     assert expected == result


