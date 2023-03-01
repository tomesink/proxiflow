import click
import polars as pl

from .config import Config
from .utils.logger import get_logger
from .core import Cleaner, Normalizer


def load_data(data_file: str, input_file_format: str) -> pl.DataFrame:
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
            # Attempt to load the CSV file
            df = pl.read_csv(data_file)
            if df.shape[0] == 0:
                raise ValueError("Data file is empty")
            return df
    except FileNotFoundError:
        # If the file is not found, raise a FileNotFoundError
        raise FileNotFoundError("Data file not found")
    except Exception as e:
        # If there is an error loading the CSV file, raise a ValueError with the error message
        raise ValueError(f"Error loading data file: {str(e)}")


# Data writer
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
            data.write_csv(output_file, sep=",")
    except Exception as e:
        raise Exception(f"Error writing data to {output_file}: {str(e)}")


@click.group(invoke_without_command=True, no_args_is_help=True)
@click.option(
    "--config-file",
    "-c",
    required=True,
    type=click.Path(exists=True),
    help="Path to configuration file",
)
@click.option(
    "--input-file",
    "-i",
    required=True,
    type=click.Path(exists=True),
    help="Path to input data file",
)
@click.option(
    "--output-file",
    "-o",
    required=True,
    type=click.Path(exists=False),
    help="Path to output data file",
)
@click.pass_context
@click.version_option()
def main(ctx, config_file, input_file, output_file):
    # Set up logger
    logger = get_logger(__name__)

    # Load configuration
    config = Config(config_file)

    # Load data
    try:
        data = load_data(input_file, input_file_format=config.input_format)
    except FileNotFoundError as e:
        logger.error("Input file not found: %s", str(e))
    except ValueError as e:
        logger.error("Error parsing input file: %s", str(e))

    # Instantiate preprocessor
    cleaner = Cleaner(config)

    # Perform data cleaning
    try:
        cleaned_data = cleaner.clean_data(data)
    except ValueError as e:
        logger.error("Error cleaning data: %s", str(e))
        return

    # TODO: Add data normalization and feature engineering
    # # Perform data normalization
    normalizer = Normalizer(config)
    print(config.normalization_config)
    normalized_data = normalizer.normalize(cleaned_data)
    

    # # Perform feature engineering

    try:
        write_data(normalized_data, output_file, output_file_format=config.output_format)
    except Exception as e:
        logger.error(f"Error writing data to file {output_file}: {str(e)}")

    # Log completion message
    logger.info("Data preprocessing complete.")


if __name__ == "__main__":
    main()
