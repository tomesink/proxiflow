import polars as pl


def check_columns(df: pl.DataFrame, columns: list[str]) -> list[str]:
    # Check if columns exist in the DataFrame. If a column does not exist, remove it from the list.
    missing_columns = []
    for col in columns:
        if col not in df.columns:
            missing_columns.append(col)

    # If all columns are missing, raise an error
    if len(missing_columns) == len(columns):
        raise ValueError("All columns specified for normalization are missing in the DataFrame.")

    # If some columns are missing, remove them from the list
    if len(missing_columns) > 0:
        for col in missing_columns:
            columns.remove(col)

    return columns
