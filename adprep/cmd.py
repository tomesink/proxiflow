# adprep/main.py

from .config import *
# from data.data_loader import load_data
# from preprocessing.data_cleaning import clean_data

# from preprocessing.data_normalization import normalize_data
# from preprocessing.feature_engineering import engineer_features
# from output.data_writer import write_data
# from utils.logger import get_logger






def run_preprocessor():

    print("This is the main function.")
    # Load configuration
    config = load_config()
    # print(config)

    fe_conf = get_feature_engineering_config(config)
    print(config["feature_engineering"])

    # clean_data()

    # # Load data
    # data = load_data(conf["data_file"])

    # # Perform data cleaning
    # clean_data(data, conf["cleaning"])

    # # Perform data normalization
    # normalize_data(data, conf["normalization"])

    # # Perform feature engineering
    # engineer_features(data, conf["features"])

    # # Write output
    # write_data(data, conf["output_file"])

    # Log completion message
    # logger = get_logger(__name__)
    # logger.info("Data preprocessing complete.")


if __name__ == "__main__":
    run_preprocessor()