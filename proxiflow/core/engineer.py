import polars as pl
from proxiflow.config import Config
from .core_utils import check_columns
from proxiflow.utils import generate_trace


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
        print(self.config)

    def execute(self, df: pl.DataFrame) -> pl.DataFrame:
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
            try:
                engineered_df = self.one_hot_encode(engineered_df, self.config["one_hot_encoding"])
            except Exception as e:
                trace = generate_trace(e, self.one_hot_encode)
                raise Exception(f"Trying one-hot encoding: {trace}")

        feature_scaling = self.config["feature_scaling"]
        if feature_scaling:
            # Perform feature scaling on the specified columns
            try:
                engineered_df = self.feature_scaling(
                    engineered_df, feature_scaling["columns"], feature_scaling["degree"]
                )
            except Exception as e:
                trace = generate_trace(e, self.feature_scaling)
                raise Exception(f"Trying polynomial feature scaling: {trace}")

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
        clone_df = df.clone()
        columns = check_columns(clone_df, columns)
        if len(columns) == 0:
            return clone_df

        return clone_df.to_dummies(columns=columns)

    def feature_scaling(self, df: pl.DataFrame, columns: list[str], degree: int) -> pl.DataFrame:
        """
        Creates polynomial features of the given degree for the specified columns of the given DataFrame.

        :param df: The DataFrame to create polynomial features for.
        :type df: polars.DataFrame
        :param columns: The columns to make features from.
        :type columns: List[str]
        :param degree: The degree of the polynomial features to create.
        :type degree: int
        :return: The DataFrame with polynomial features.
        :rtype: polars.DataFrame
        """
        clone_df = df.clone()

        if not columns:
            return clone_df

        columns = check_columns(clone_df, columns)
        # Add polynomial features for each column
        for col in columns:
            # We can not square root strings
            if clone_df[col].dtype == pl.Int64 or clone_df[col].dtype == pl.Float64:
                # Create a new column for each degree of the polynomial
                degrees = range(2, degree + 1)
                # Use list comprehension to generate the new columns
                new_cols = [(pl.col(col) ** i).alias(f"{col}_{i}") for i in degrees]
                # Combine the new columns with the original DataFrame
                clone_df = clone_df.with_columns(*new_cols)

        return clone_df
