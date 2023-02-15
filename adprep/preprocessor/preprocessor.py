import polars as pl
from adprep.config import Config

class Preprocessor:
    """
    A class for performing data preprocessing tasks such as cleaning, normalization, and feature engineering.
    """

    def __init__(self, config: Config):
        """
        Initialize a new Preprocessor object with the specified configuration.

        Parameters:
        config (Config): A Config object containing the cleaning configuration values.
        """
        self.config = config

    @classmethod
    def clean_data(self, df: pl.DataFrame) -> pl.DataFrame:
        """
        Clean a polars DataFrame by removing duplicates and filling in missing values.

        Parameters:
        df (pl.DataFrame): The DataFrame to clean.

        Returns:
        pl.DataFrame: The cleaned DataFrame.
        """
        cleaning_config = self.config.cleaning_config

        # Handle duplicate rows
        if cleaning_config["remove_duplicates"]:
            print("Removing duplicates...")
            # df = self.remove_duplicates(df)

        # Handle missing values
        # if cleaning_config["handle_missing_values"]:
        #     if "drop" in cleaning_config["handle_missing_values"]:
        #         df = df.drop_nulls()
        #     if "mean" in cleaning_config["handle_missing_values"]:
        #         df = df.fill_nulls(pl.col("*"), pl.mean)
        #     if "mode" in cleaning_config["handle_missing_values"]:
        #         df = df.fill_nulls(pl.col("*"), pl.mode)

        # return df

    @staticmethod
    def remove_duplicates(self, df: pl.DataFrame) -> pl.DataFrame:
        """
        Remove duplicate rows from a polars DataFrame.

        Parameters:
        df (pl.DataFrame): The DataFrame to remove duplicates from.

        Returns:
        pl.DataFrame: The DataFrame with duplicates removed.
        """
        return df.unique(keep='first')

