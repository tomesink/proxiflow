import yaml
from typing import Dict, Any, cast


class Config:
    """
    A class for loading configuration data from a YAML file.

    :param file_path: The path to the YAML configuration file.
    :type file_path: str
    """

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.config = self.load_config(file_path)

    @staticmethod
    def load_config(file_path: str) -> Dict[str, Any]:
        """
        Load a YAML configuration file from the specified file path.

        :param file_path: The path to the YAML configuration file.
        :type file_path: str

        :returns: A dictionary containing the configuration values.
        :rtype: Dict

        :raises FileNotFoundError: If the specified file path does not exist.
        :raises ValueError: If the specified file is empty or cannot be parsed as YAML.
        :raises TypeError: If the loaded YAML data is not a dictionary with string keys.
        """
        try:
            with open(file_path, "r") as f:
                config = cast(Dict[str, Any], yaml.safe_load(f))
            if config is None:
                raise ValueError("Config file is empty")
            if not isinstance(config, dict) or not all(isinstance(k, str) for k in config.keys()):
                raise TypeError("The loaded YAML data is not a dictionary with string keys")
            return config
        except FileNotFoundError:
            raise FileNotFoundError("Config file not found")
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing config file: {str(e)}")

    @property
    def input_format(self) -> str:
        """
        Get the input file format configuration dictionary.

        :returns: A string containing the input file type
        :rtype: str

        :raises ValueError: If the "input_format" key is not present in the configuration dictionary.
        """
        try:
            return cast(str, self.config["input_format"])
        except KeyError:
            raise ValueError("input file format not found in config file")

    @property
    def output_format(self) -> str:
        """
        Get the output file format configuration dictionary.

        :returns: A string containing the output file type
        :rtype: str

        :raises ValueError: If the "output_format" key is not present in the configuration dictionary.
        """
        try:
            return cast(str, self.config["output_format"])
        except KeyError:
            raise ValueError("output file format not found in config file")

    @property
    def cleaning_config(self) -> Dict[str, Any]:
        """
        Get the data cleaning configuration values from the configuration dictionary.

        :returns: A dictionary containing the data cleaning configuration values.
        :rtype: Dict

        :raises ValueError: If the "data_cleaning" key is not present in the configuration dictionary.
        """
        try:
            return cast(Dict[str, Any], self.config["data_cleaning"])
        except KeyError:
            raise ValueError("data_cleaning config not found in config file")

    @property
    def normalization_config(self) -> Dict[str, Any]:
        """
        Get the data normalization configuration values from the configuration dictionary.

        :returns: A dictionary containing the data normalization configuration values.
        :rtype: Dict

        :raises ValueError: If the "data_normalization" key is not present in the configuration dictionary.
        """
        try:
            return cast(Dict[str, Any], self.config["data_normalization"])
        except KeyError:
            raise ValueError("data_normalization config not found in config file")

    @property
    def feature_engineering_config(self) -> Dict[str, Any]:
        """
        Get the feature engineering configuration values from the configuration dictionary.

        :returns: A dictionary containing the feature engineering configuration values.
        :rtype: Dict

        :raises ValueError: If the "feature_engineering" key is not present in the configuration dictionary.
        """
        try:
            return cast(Dict[str, Any], self.config["feature_engineering"])
        except KeyError:
            raise ValueError("feature_engineering config not found in config file")
