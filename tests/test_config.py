import pytest
from proxiflow.config import Config

CONFIG_FILE_PATH = "tests/data/config.yaml"

@pytest.fixture(scope="module")
def config():
    return Config(CONFIG_FILE_PATH)

class TestConfig:
    """
    Unit tests for the Config class.
    """
    
    def test_load_config(self, config):
        """
        Test loading a valid configuration file.

        Parameters:
        config (Config): A Config object with the loaded configuration values.

        Raises:
        AssertionError: If the loaded configuration is not a dictionary.
        """
        test_config = config.config
        assert isinstance(test_config, dict)
        
        # Test loading an invalid configuration file
        with pytest.raises(FileNotFoundError):
            Config("invalid_path.yaml")

    def test_cleaning_config(self, config):
        """
        Test getting the data cleaning configuration values from a Config object.

        Parameters:
        config (Config): A Config object with the loaded configuration values.

        Raises:
        AssertionError: If the cleaning configuration is not a dictionary or is missing expected keys.
        """
        cleaning_config = config.cleaning_config
        assert isinstance(cleaning_config, dict)
        assert "handle_missing_values" in cleaning_config
        assert "drop" in cleaning_config["handle_missing_values"]
        assert "mean" in cleaning_config["handle_missing_values"]
        # assert "mode" in cleaning_config["handle_missing_values"]
        assert "remove_duplicates" in cleaning_config
        assert cleaning_config["remove_duplicates"]


    def test_get_normalization_config(self, config):
        """
        Test getting the data normalization configuration values from a Config object.

        Parameters:
        config (Config): A Config object with the loaded configuration values.

        Raises:
        AssertionError: If the normalization configuration is not a dictionary or is missing expected keys.
        """
        normalization_config = config.normalization_config
        assert isinstance(normalization_config, dict)
        assert "min_max" in normalization_config
        assert "z_score" in normalization_config
        assert "log" in normalization_config


    def test_feature_engineering_config(self, config):
        """
        Test getting the feature engineering configuration values from a Config object.

        Parameters:
        config (Config): A Config object with the loaded configuration values.

        Raises:
        AssertionError: If the feature engineering configuration is not a dictionary or is missing expected keys or values.
        """
        feature_engineering_config = config.feature_engineering_config
        assert isinstance(feature_engineering_config, dict)
        assert len(feature_engineering_config) == 2
        assert "one_hot_encoding" in feature_engineering_config
        assert "feature_scaling" in feature_engineering_config
     
