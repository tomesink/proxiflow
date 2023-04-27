import polars as pl
from sklearn.impute import KNNImputer
from proxiflow.config import Config
from proxiflow.utils import generate_trace


class Cleaner:
    """
    A class for performing data preprocessing tasks such as cleaning, normalization, and feature engineering.
    """

    def __init__(self, config: Config):
        """
        Initialize a new Cleaner object with the specified configuration.

        :param config: A Config object containing the cleaning configuration values.
        :type config: Config
        """
        self.config = config.cleaning_config

    def clean_data(self, df: pl.DataFrame) -> pl.DataFrame:
        """
        Clean a polars DataFrame by removing duplicates and filling in missing values.

        :param df: The DataFrame to clean.
        :type df: polars.DataFrame

        :returns df: The cleaned DataFrame.
        :rtype: polars.DataFrame

        :raises ValueError: If the DataFrame is empty.
        """
        if df.shape[0] == 0:
            raise ValueError("Empty DataFrame, no missing values to fill.")

        cleaned_df = df.clone()
        # #Handle missing values. drop|mean|mode are mutually exclusive
        missing_values = self.config["handle_missing_values"]

        # Drop missing values
        if missing_values["drop"]:
            try:
                cleaned_df = self._drop_missing(cleaned_df)
            except Exception as e:
                trace = generate_trace(e, self._drop_missing)
                raise Exception(f"Trying to drop missing values: {trace}")
            return cleaned_df

        # Fill missing values with the mean of the column
        if missing_values["mean"]:
            try:
                cleaned_df = self._mean_missing(cleaned_df)
            except Exception as e:
                trace = generate_trace(e, self._mean_missing)
                raise Exception(f"Trying to fill missing values with the mean: {trace}")
            return cleaned_df

        # Fill missing values with KNN Imputer
        if missing_values["knn"]:
            try:
                cleaned_df = self._knn_impute_missing(cleaned_df)
            except Exception as e:
                trace = generate_trace(e, self._knn_impute_missing)
                raise Exception(f"Trying to fill missing values with KNN Imputer: {trace}")

        # NOTE: This is currently disabled because it randomly fails with:
        # Fill missing values with the mode of the column.
        # if missing_values["mode"]:
        #     cleaned_df = self.mode_missing(cleaned_df)
        #     return cleaned_df

        # Fill outliers with the median of the column
        if self.config["handle_outliers"]:
            try:
                cleaned_df = self._handle_outliers(cleaned_df)
            except Exception as e:
                trace = generate_trace(e, self._handle_outliers)
                raise Exception(f"Trying to fill outliers with the median: {trace}")

        # Handle duplicate rows
        if self.config["remove_duplicates"]:
            try:
                cleaned_df = self._remove_duplicates(cleaned_df)
            except Exception as e:
                trace = generate_trace(e, self._remove_duplicates)
                raise Exception(f"Trying to remove duplicate rows: {trace}")

        return cleaned_df

    def _remove_duplicates(self, df: pl.DataFrame) -> pl.DataFrame:
        """
        Remove duplicate rows from a polars DataFrame.

        :param df: The DataFrame to remove duplicates from.
        :type df: polars.DataFrame

        :returns: The DataFrame with duplicates removed.
        :rtype: polars.DataFrame
        """
        clone_df = df.clone()
        return clone_df.unique(keep="first")

    def _drop_missing(self, df: pl.DataFrame) -> pl.DataFrame:
        """
        Drop rows with missing values from a polars DataFrame.

        :param df: The DataFrame to drop rows from.
        :type df: polars.DataFrame

        :returns: The DataFrame with rows with missing values dropped.
        :rtype: polars.DataFrame
        """
        clone_df = df.clone()
        return clone_df.drop_nulls()

    def _mean_missing(self, df: pl.DataFrame) -> pl.DataFrame:
        """
        Fill missing values with the mean of the column.

        :param df: The DataFrame to fill missing values in.
        :type df: polars.DataFrame

        :returns: The DataFrame with missing values filled.
        :rtype: polars.DataFrame
        """
        clone_df = df.clone()
        for col in clone_df.columns:
            # Only Integers and Floats supported
            if clone_df[col].dtype == pl.Int64 or clone_df[col].dtype == pl.Float64:
                mean_s = clone_df[col].fill_null(strategy="mean")
                clone_df.replace(col, mean_s)

        return clone_df

    # TODO: Investigate why this randomly fails with:
    #  Error cleaning data: must specify either a fill 'value' or 'strategy'
    def _mode_missing(self, df: pl.DataFrame) -> pl.DataFrame:
        """
        Fill missing values with the mode of the column. Only Int64 and Str data types are supported.

        :param df: The DataFrame to fill missing values in.
        :type df: polars.DataFrame

        :returns: The DataFrame with missing values filled with mode or original null (in case of unsupported data type)
        :rtype: polars.DataFrame
        """
        clone_df = df.clone()
        for col in clone_df.columns:
            # Only Integers and String supported
            if clone_df[col].dtype == pl.Int64 or clone_df[col].dtype == pl.Utf8:
                mode = clone_df[col].mode()
                mode_s = clone_df[col].fill_null(value=mode[0])
                clone_df.replace(col, mode_s)

        return clone_df

    def _knn_impute_missing(self, df: pl.DataFrame) -> pl.DataFrame:
        """
        Fill missing values using KNN imputation.
        :param df: The DataFrame to fill missing values in.
        :type df: polars.DataFrame
        :returns: The DataFrame with missing values filled.
        :rtype: polars.DataFrame
        """
        clone_df = df.clone()
        # Convert the DataFrame to numpy array
        np_df = clone_df.to_numpy()

        # Initialize the KNN Imputer
        knn_imputer = KNNImputer(n_neighbors=5, weights="uniform")
        imputed_np_df = knn_imputer.fit_transform(np_df)

        # Convert the imputed numpy array back to polars DataFrame
        imputed_df = pl.DataFrame(imputed_np_df, schema=clone_df.schema)

        return imputed_df

    # Handle outliers with IQR method
    def _handle_outliers(self, df: pl.DataFrame) -> pl.DataFrame:
        """
        Handle outliers in a polars DataFrame by replacing them with median of the

        :param df: The DataFrame to handle outliers in.
        :type df: polars.DataFrame

        :returns: The DataFrame with outliers removed.
        :rtype: polars.DataFrame
        """
        clone_df = df.clone()

        for col in clone_df.columns:
            if clone_df[col].dtype == pl.Float64:
                # Get the first and third quartiles and the IQR
                q1 = clone_df[col].quantile(0.25)
                q3 = clone_df[col].quantile(0.75)
                iqr = q3 - q1
                # Identify the lower and upper bounds for outliers
                lower_bound = q1 - 1.5 * iqr
                upper_bound = q3 + 1.5 * iqr
                # Replace outliers with the median value of the series
                median = clone_df[col].median()
                serie = clone_df[col].apply(lambda x: median if x < lower_bound or x > upper_bound else x)
                clone_df.replace(col, serie)

        return clone_df
