import pytest
import polars as pl
from adprep.config import Config
from adprep.preprocessor import Preprocessor

CONFIG_FILE_PATH = "tests/data/config.yaml"
DATA_FILE_PATH = "tests/data/input.csv"

@pytest.fixture(scope="module")
def config():
    return Config(CONFIG_FILE_PATH)

@pytest.fixture(scope="module")
def data():
    return pl.read_csv(DATA_FILE_PATH)

class TestPreprocessor:
    def test_clean_data_with_empty_dataframe(self, config):
        with pytest.raises(ValueError):
            preprocessor = Preprocessor(config)
            preprocessor.clean_data(pl.DataFrame())

    def test_remove_duplicates(self, data, config):
        preprocessor = Preprocessor(config)
        cleaned_data = preprocessor.remove_duplicates(data)
        assert cleaned_data.shape[0] == data.unique().shape[0]

    def test_drop_missing(self, data, config):
        preprocessor = Preprocessor(config)
        df_with_nulls = data.clone().shift(1).apply(lambda s: None if s["a"] > 0 else s)
        cleaned_data = preprocessor.drop_missing(df_with_nulls)
        assert cleaned_data.shape[0] == data.shape[0] - 1

    def test_mean_missing(self, data, config):
        preprocessor = Preprocessor(config)
        df_with_nulls = data.clone().shift(1).apply(lambda s: None if s["a"] > 0 else s)
        cleaned_data = preprocessor.mean_missing(df_with_nulls)
        assert cleaned_data.column("a").null_count() == 0

    def test_mode_missing(self, data, config):
        preprocessor = Preprocessor(config)
        df_with_nulls = data.clone().shift(1).apply(lambda s: None if s["a"] > 0 else s)
        cleaned_data = preprocessor.mode_missing(df_with_nulls)
        assert cleaned_data.column("a").null_count() == 0

    def test_clean_data(self, data):
        preprocessor = Preprocessor(config)
        cleaned_data = preprocessor.clean_data(data)
        assert cleaned_data.shape == data.shape