import pytest
import polars as pl
import numpy as np
from proxiflow.config import Config
from proxiflow.core import Cleaner

CONFIG_FILE_PATH = "tests/data/config.yaml"
DATA_FILE_PATH = "tests/data/input.csv"

@pytest.fixture(scope="module")
def config():
    return Config(CONFIG_FILE_PATH)

@pytest.fixture(scope="module")
def data():
    return pl.read_csv(DATA_FILE_PATH)

class TestCleaner:
    """
    A test class for the Cleaner class in the proxiflow library.
    """
    def test_clean_data_with_empty_dataframe(self, config):
        """
        Test that an empty DataFrame raises a ValueError when cleaned.

        Parameters:
        config (Config): The Config object to use for testing.

        Returns:
        None

        Raises:
        AssertionError: If the test fails.
        """
        with pytest.raises(ValueError):
            flow = Cleaner(config)
            flow.clean_data(pl.DataFrame())

    def test_remove_duplicates(self, data, config):
        """
        Test the remove_duplicates method of the Cleaner class.

        Parameters:
        data (pl.DataFrame): The DataFrame to use for testing.
        config (Config): The Config object to use for testing.

        Returns:
        None

        Raises:
        AssertionError: If the test fails.
        """
        cleaner = Cleaner(config)
        cleaned_data = cleaner.remove_duplicates(data)
        assert cleaned_data.shape[0] == data.unique().shape[0]

    def test_drop_missing(self, config):
        """
        Test the drop_missing method of the Cleaner class.

        Parameters:
        config (Config): The Config object to use for testing.

        Returns:
        None

        Raises:
        AssertionError: If the test fails.
        """
        cleaner = Cleaner(config)
        df_with_nulls = pl.DataFrame({'a': [None]*10, 'b': [None]*10})
        cleaned_data = cleaner.drop_missing(df_with_nulls)
        assert cleaned_data.shape[0] == df_with_nulls.shape[0] - 10

    def test_mean_missing(self, config):
        """
        Test the mean_missing method of the Cleaner class.

        Parameters:
        config (Config): The Config object to use for testing.

        Returns:
        None

        Raises:
        AssertionError: If the test fails.
        """
        cleaner = Cleaner(config)
        df_with_nulls= pl.DataFrame({
            "A": [1, 2, 3, None],
            "B": [4.0, 5.0, None, 7.0]
        })
        cleaned_data = cleaner.mean_missing(df_with_nulls)
        expected_df= pl.DataFrame({
            "A": [1, 2, 3, 2],
            "B": [4.0, 5.0, 5.333333, 7.0]
        })
        cleaned_arr = cleaned_data.to_numpy()
        expected_arr = expected_df.to_numpy()
        np.testing.assert_allclose(cleaned_arr, expected_arr, rtol=1e-5, atol=1e-8)

    def test_mode_missing(self, config):
        """
        Test the mode_missing method of the Cleaner class.

        Parameters:
        data (pl.DataFrame): The DataFrame to use for testing.
        config (Config): The Config object to use for testing.

        Returns:
        None

        Raises:
        AssertionError: If the test fails.
        """
        pass
        # cleaner = Cleaner(config)
        # df_with_nulls = pl.DataFrame({
        #     "A": [1, 2, 2, 2, 4, None],
        #     "B": ["One","One", "Five", "Two", None, "Three"]
        # })
        # cleaned_data = cleaner.mode_missing(df_with_nulls)
        # expected_df =  pl.DataFrame({
        #     "A": [1, 2, 2, 2, 4, 2],
        #     "B": ["One","One", "Five", "Two", "One", "Three"]
        # })
        # assert expected_df.frame_equal(cleaned_data)