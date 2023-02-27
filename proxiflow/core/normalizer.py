import polars as pl
from proxiflow.config import Config

class Normalizer:
    """
    A class for performing data normalizing tasks. 
    """

    def __init__(self, config: Config):
        """
        Initialize a new Normalizer object with the specified configuration.

        :param config: A Config object containing the cleaning configuration values.
        :type config: Config
        """
        self.config = config.normalization_config


    def normalize(self, df: pl.DataFrame) -> pl.DataFrame:
        """
        Normalize the specified DataFrame using the specified configuration.

        :param df: The DataFrame to normalize.
        :type df: polars.DataFrame
        :return: The normalized DataFrame.
        :rtype: polars.DataFrame
        """
        normalized_df = df.clone()
        # Apply min-max normalization
        min_max_cols = self.config["min_max"]["columns"]
        if min_max_cols:
            # Normalize the specified columns
            normalized_df = self.min_max_normalize(normalized_df, min_max_cols)
        

        return normalized_df


    def min_max_normalize(self, df: pl.DataFrame, columns: list[str]) -> pl.DataFrame:
        """
        Applies min-max normalization to the specified columns of the given DataFrame.

        :param df: The DataFrame to normalize.
        :type df: polars.DataFrame
        :param columns: The columns to normalize.
        :type columns: List[str]
        :return: The normalized DataFrame.
        :rtype: polars.DataFrame
        """
        clone_df = df.clone()
        # Check if columns exist in the DataFrame. If a column does not exist, remove it from the list.
        for col in columns:
            if not col in clone_df.columns:
                columns.remove(col)
        # If no columns exist, return the original DataFrame
        if len(columns) == 0:
            return clone_df
        
        # Select the specified columns
        selected_df= clone_df.select(columns)

        for col in selected_df.columns:
            # We can not subtract strings, so we only normalize numeric columns
            if clone_df[col].dtype == pl.Int64 or clone_df[col].dtype == pl.Float64:
                # Get the min and max values of the column
                min_val = selected_df[col].min()
                max_val = selected_df[col].max()
                # Normalize the column
                min_max = (df[col] - min_val) / (max_val - min_val)
                clone_df.replace(col, min_max)

        return clone_df