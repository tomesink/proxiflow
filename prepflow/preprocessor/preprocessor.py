import polars as pl
from prepflow.config import Config


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

    def clean_data(self, df: pl.DataFrame) -> pl.DataFrame:
        """
        Clean a polars DataFrame by removing duplicates and filling in missing values.

        Parameters:
        df (pl.DataFrame): The DataFrame to clean.

        Returns:
        pl.DataFrame: The cleaned DataFrame.

        Raises:
        ValueError: If the DataFrame is empty.
        """
        if df.shape[0] == 0:
            raise ValueError("Empty DataFrame, no missing values to fill.")

        cleaning_config = self.config.cleaning_config
        cleaned_df = df.clone()

        # Handle duplicate rows
        if cleaning_config["remove_duplicates"]:
            cleaned_df = self.remove_duplicates(cleaned_df)

        # #Handle missing values. drop|mean|mode are mutually exclusive
        missing_values = cleaning_config["handle_missing_values"]

        # Drop missing values
        if missing_values["drop"]:
            cleaned_df = self.drop_missing(cleaned_df)
            return cleaned_df

        # Fill missing values with the mean of the column
        if missing_values["mean"]:
            cleaned_df = self.mean_missing(cleaned_df)
            return cleaned_df

        # Fill missing values with the mode of the column.
        if missing_values["mode"]:
            cleaned_df = self.mode_missing(cleaned_df)
            return cleaned_df

        return cleaned_df

    def remove_duplicates(self, df: pl.DataFrame) -> pl.DataFrame:
        """
        Remove duplicate rows from a polars DataFrame.

        Parameters:
        df (pl.DataFrame): The DataFrame to remove duplicates from.

        Returns:
        pl.DataFrame: The DataFrame with duplicates removed.
        """
        clone_df = df.clone()
        return clone_df.unique(keep="first")

    def drop_missing(self, df: pl.DataFrame) -> pl.DataFrame:
        """
        Drop rows with missing values from a polars DataFrame.

        Parameters:
        df (pl.DataFrame): The DataFrame to drop rows from.

        Returns:
        pl.DataFrame: The DataFrame with rows with missing values dropped.
        """
        clone_df = df.clone()
        return clone_df.drop_nulls()

    def mean_missing(self, df: pl.DataFrame) -> pl.DataFrame:
        """
        Fill missing values with the mean of the column.

        Parameters:
        df (pl.DataFrame): The DataFrame to fill missing values in.

        Returns:
        pl.DataFrame: The DataFrame with missing values filled.
        """
        clone_df = df.clone()
        for col in clone_df.columns:
            # Only Integers and Floats supported
            if clone_df[col].dtype == pl.Int64 or clone_df[col].dtype == pl.Float64:
                mean = clone_df[col].mean()
                mean_s = clone_df[col].fill_null(mean)
                clone_df.replace(col, mean_s)

        return clone_df


    def mode_missing(self, df: pl.DataFrame) -> pl.DataFrame:
        """
        Fill missing values with the mode of the column. Only Int64 and Str data types are supported.

        Parameters:
        df (pl.DataFrame): The DataFrame to fill missing values in.

        Returns:
        pl.DataFrame: The DataFrame with missing values filled with mode or original null (in case of unsupported data type)
        """
        clone_df = df.clone()
        for col in clone_df.columns:
            # Only Integers and String supported
            if clone_df[col].dtype == pl.Int64 or clone_df[col].dtype == pl.Utf8:
                mode = clone_df[col].mode()
                mode_s = clone_df[col].fill_null(mode[0])
                clone_df.replace(col, mode_s)

        return clone_df
