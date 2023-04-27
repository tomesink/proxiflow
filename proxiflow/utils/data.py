import polars as pl
from typing import Optional


def load_data(data_file: str, input_file_format: str) -> Optional[pl.DataFrame]:
    """
    Load a CSV file and return a polars DataFrame.

    :param data_file: The path to the CSV file to load.
    :type data_file: str

    :returns: The DataFrame containing the CSV data.
    :rtype: polars.DataFrame

    :raises FileNotFoundError: If the specified file path does not exist.
    :raises ValueError: If the specified file is empty or cannot be parsed as a CSV file.
    """
    try:
        if input_file_format == "csv":
            df = pl.read_csv(data_file)
            if df.shape[0] == 0:
                raise ValueError("Data file is empty")
            return df
        return None
    except FileNotFoundError:
        raise FileNotFoundError("Data file not found")
    except Exception as e:
        raise ValueError(f"Error loading data file: {str(e)}")


def write_data(data: pl.DataFrame, output_file: str, output_file_format: str) -> None:
    """
    Writes a given DataFrame to a CSV file.

    :param data: The DataFrame to be written.
    :type data: polars.DataFrame
    :param output_file: The file path to save the data.
    :type output_file: str

    :returns: None

    :raises Exception: If there is an error while writing the data.
    """
    try:
        if output_file_format == "csv":
            data.write_csv(file=output_file)
    except Exception as e:
        raise Exception(f"Error writing data to {output_file}: {str(e)}")
