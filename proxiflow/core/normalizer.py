import polars as pl
import scipy.stats as stats
from proxiflow.config import Config
from proxiflow.utils import generate_trace
from .core_utils import check_columns

from typing import Dict, Any, List, Union, cast


class Normalizer:
    """
    A class for performing data normalizing tasks.
    """

    def __init__(self, config: Config):
        """
        Initialize a new Normalizer object with the specified configuration.

        :param config: A Config object containing the normalization configuration values.
        :type config: Config
        """
        self.config: Dict[str, Any] = config.normalization_config

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
        min_max_cols: List[str] = self.config["min_max"]
        if min_max_cols:
            # Normalize the specified columns
            try:
                normalized_df = self._min_max_normalize(normalized_df, min_max_cols)
            except Exception as e:
                trace: str = generate_trace(e, self._min_max_normalize)
                raise Exception(f"Trying min-max normalization: {trace}")

        # Apply z-score normalization
        z_score_cols: List[str] = self.config["z_score"]
        if z_score_cols:
            # Normalize the specified columns
            try:
                normalized_df = self._z_score_normalize(normalized_df, z_score_cols)
            except Exception as e:
                trace = generate_trace(e, self._z_score_normalize)
                raise Exception(f"Trying z-score normalization: {trace}")

        # Apply log normalization
        log_cols: List[str] = self.config["log"]
        if log_cols:
            # Normalize the specified columns
            try:
                normalized_df = self._log_normalize(normalized_df, log_cols)
            except Exception as e:
                trace = generate_trace(e, self._log_normalize)
                raise Exception(f"Trying log normalization: {trace}")

        return normalized_df

    def _min_max_normalize(self, df: pl.DataFrame, columns: List[str]) -> pl.DataFrame:
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
        columns = check_columns(clone_df, columns)
        # If no columns exist, return the original DataFrame
        if len(columns) == 0:
            return clone_df
        # Select the specified columns
        selected_df = clone_df.select(columns)

        for col in selected_df.columns:
            # We can not subtract strings, so we only normalize numeric columns
            if clone_df[col].dtype == pl.Int64 or clone_df[col].dtype == pl.Float64:
                # Get the min and max values of the column
                min_val = cast(Union[int, float], selected_df[col].min())
                max_val = cast(Union[int, float], selected_df[col].max())
                if max_val - min_val == 0:
                    raise ValueError(f"Error normalizing min-max column {col}: division by zero")
                # Normalize the column
                min_max = (df[col] - min_val) / (max_val - min_val)
                clone_df.replace(col, min_max)

        return clone_df

    def _z_score_normalize(self, df: pl.DataFrame, columns: List[str]) -> pl.DataFrame:
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
        columns = check_columns(clone_df, columns)

        if len(columns) == 0:
            return clone_df

        selected_df = clone_df.select(columns)

        for col in selected_df.columns:
            if clone_df[col].dtype == pl.Int64 or clone_df[col].dtype == pl.Float64:
                # Get the values of the column. Filter out None values
                values = list(filter(lambda x: x is not None, clone_df[col].to_list()))
                z_score = stats.zscore(values)
                clone_df.replace(col, pl.Series(z_score))

        return clone_df

    def _log_normalize(self, df: pl.DataFrame, columns: List[str]) -> pl.DataFrame:
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
        columns = check_columns(clone_df, columns)

        if len(columns) == 0:
            return clone_df

        selected_df = clone_df.select(columns)

        for col in selected_df.columns:
            if clone_df[col].dtype == pl.Int64 or clone_df[col].dtype == pl.Float64:
                norm = (1 + clone_df[col]) / 2
                log = norm.log()
                clone_df.replace(col, log)

        return clone_df
