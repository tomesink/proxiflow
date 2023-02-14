# adprep/config/config.py
import yaml

def load_config():
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
    return config

def get_cleaning_config(conf):
    return conf["data_cleaning"]

def get_normalization_config(conf):
    return conf["data_normalization"]

def get_feature_engineering_config(conf):
    return conf["feature_engineering"]