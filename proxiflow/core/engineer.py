import polars as pl
from proxiflow.config import Config

class Engineer:
    """
    A class for performing feature engineering tasks. 
    """
    def __init__(self, config: Config):
        """
        Initialize a new Engineer object with the specified configuration.

        :param config: A Config object containing the feature engineering configuration values.
        :type config: Config
        """
        self.config = config.feature_engineering_config

    def engineer(self, df: pl.DataFrame) -> pl.DataFrame:
        """
        Perform feature engineering on the specified DataFrame using the specified configuration.

        :param df: The DataFrame to perform feature engineering on.
        :type df: polars.DataFrame
        :return: The DataFrame with the new features.
        :rtype: polars.DataFrame
        """
        engineered_df = df.clone()
        # Apply feature engineering

        if self.config["one_hot_encoding"]:
            # Perform feature engineering on the specified columns
            engineered_df = self.one_hot_encode(engineered_df, self.config["one_hot_encoding"])

        return engineered_df
    

    def one_hot_encode(self, df: pl.DataFrame, columns: list[str]) -> pl.DataFrame:
        """
        One-hot encode the specified columns of the given DataFrame.

        :param df: The DataFrame to one-hot encode.
        :type df: polars.DataFrame
        :param columns: The columns to one-hot encode.
        :type columns: List[str]
        :return: The one-hot encoded DataFrame.
        :rtype: polars.DataFrame
        """
        return df.to_dummies(columns=columns)
