import polars as pl
import scipy.stats as stats
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
        min_max_cols = self.config["min_max"]
        if min_max_cols:
            # Normalize the specified columns
            normalized_df = self._min_max_normalize(normalized_df, min_max_cols)
        
        # Apply z-score normalization
        z_score_cols = self.config["z_score"]
        if z_score_cols:
            # Normalize the specified columns
            normalized_df = self._z_score_normalize(normalized_df, z_score_cols)

        # Apply log normalization
        log_cols = self.config["log"]
        if log_cols:
            # Normalize the specified columns
            normalized_df = self._log_normalize(normalized_df, log_cols)

        return normalized_df


    def _min_max_normalize(self, df: pl.DataFrame, columns: list[str]) -> pl.DataFrame:
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
        columns = self._check_columns(clone_df, columns)
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
    
    # Function for z-score normalization
    def _z_score_normalize(self, df: pl.DataFrame, columns: list[str]) -> pl.DataFrame:
        """
        Applies z-score normalization to the specified columns of the given DataFrame.

        :param df: The DataFrame to normalize.
        :type df: polars.DataFrame
        :param columns: The columns to normalize.
        :type columns: List[str]
        :return: The normalized DataFrame.
        :rtype: polars.DataFrame
        """
        clone_df = df.clone()
        columns = self._check_columns(clone_df, columns)
        # If no columns exist, return the original DataFrame
        if len(columns) == 0:
            return clone_df
        # Select the specified columns
        selected_df= clone_df.select(columns)

        for col in selected_df.columns:
            if clone_df[col].dtype == pl.Int64 or clone_df[col].dtype == pl.Float64:
                values = clone_df[col].to_list()
                z_score = stats.zscore(values)
                clone_df.replace(col, pl.Series(z_score))

        return clone_df
    
    # Function for log normalization
    def _log_normalize(self, df: pl.DataFrame, columns: list[str]) -> pl.DataFrame:
        """
        Applies log normalization to the specified columns of the given DataFrame.

        :param df: The DataFrame to normalize.
        :type df: polars.DataFrame
        :param columns: The columns to normalize.
        :type columns: List[str]
        :return: The normalized DataFrame.
        :rtype: polars.DataFrame
        """
        clone_df = df.clone()
        columns = self._check_columns(clone_df, columns)
       
         # If no columns exist, return the original DataFrame
        if len(columns) == 0:
            return clone_df
        # Select the specified columns
        selected_df= clone_df.select(columns)

        for col in selected_df.columns:
            if clone_df[col].dtype == pl.Int64 or clone_df[col].dtype == pl.Float64:
                norm = (1 + clone_df[col]) / 2
                log = norm.log()
                clone_df.replace(col, log)

        return clone_df

    def _check_columns(self, df: pl.DataFrame, columns: list[str]) -> list[str]:
        # Check if columns exist in the DataFrame. If a column does not exist, remove it from the list.
        missing_columns = []
        for col in columns:
            if not col in df.columns:
                missing_columns.append(col)

        # If all columns are missing, raise an error
        if len(missing_columns) == len(columns):
            raise ValueError("All columns specified for normalization are missing in the DataFrame.")
        
        # If some columns are missing, remove them from the list
        if len(missing_columns) > 0:
            for col in missing_columns:
                columns.remove(col)
        
        return columns