import polars as pl
import click

from .config import Config
from .utils.logger import get_logger
from .preprocessor import Preprocessor

# from preprocessing.data_normalization import normalize_data
# from preprocessing.feature_engineering import engineer_features
# from output.data_writer import write_data
# from utils.logger import get_logger


def load_data(data_file):
    return pl.read_csv(data_file)


@click.group(invoke_without_command=True, no_args_is_help=True)
@click.option("--config-file", "-c", required=True, type=click.Path(exists=True), help="Path to configuration file")
@click.option("--input-file", "-i", required=True, type=click.Path(exists=True), help="Path to input data file")
@click.option("--output-file", "-o", required=True, type=click.Path(exists=False), help="Path to output data file")
@click.pass_context
@click.version_option()

def run_preprocessor(ctx, config_file, input_file, output_file):
    # Set up logger
    logger = get_logger(__name__)

    # Load configuration
    config = Config(config_file)

    # Load data
    data = load_data(input_file)

    # Instantiate preprocessor
    preprocessor = Preprocessor(config)

    # Perform data cleaning
    cleaned_data = preprocessor.clean_data(data)

    # # Perform data normalization
    # normalize_data(data, conf["normalization"])

    # # Perform feature engineering
    # engineer_features(data, conf["features"])

    # # Write output
    # write_data(data, conf["output_file"])

    # Log completion message
    logger.info("Data preprocessing complete.")


if __name__ == "__main__":
    run_preprocessor()
