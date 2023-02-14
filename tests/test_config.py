import pytest
from adprep.config import *

@pytest.fixture(scope="module")
def config():
    return load_config()

def test_load_config(config):
    assert isinstance(config, dict)
    assert len(config) > 0

def test_get_cleaning_config(config):
    cleaning_conf = get_cleaning_config(config)
    assert isinstance(cleaning_conf, dict)
    assert "handle_missing_values" in cleaning_conf
    assert "drop" in cleaning_conf["handle_missing_values"]
    assert "mean" in cleaning_conf["handle_missing_values"]
    assert "mode" in cleaning_conf["handle_missing_values"]
    assert "remove_duplicates" in cleaning_conf
    assert cleaning_conf["remove_duplicates"]

def test_get_normalization_config(config):
    normalization_conf = get_normalization_config(config)
    assert isinstance(normalization_conf, dict)
    assert "min_max" in normalization_conf
    assert "z_score" in normalization_conf
    assert "log" in normalization_conf
    assert normalization_conf["min_max"]
    assert not normalization_conf["z_score"]
    assert not normalization_conf["log"]

def test_get_feature_engineering_config(config):
    print(config)
    feature_engineering_conf = get_feature_engineering_config(config)
    print(feature_engineering_conf)
    assert isinstance(feature_engineering_conf, dict)
    assert len(feature_engineering_conf) == 3
    assert "one_hot_encoding" in feature_engineering_conf
    assert "feature_scaling" in feature_engineering_conf
    assert "feature_selection" in feature_engineering_conf
    assert feature_engineering_conf["one_hot_encoding"] == ["gender", "ethnicity"]
    assert feature_engineering_conf["feature_scaling"]["columns"] == ["height", "weight"]
    assert feature_engineering_conf["feature_scaling"]["range"] == [0, 1]
    assert feature_engineering_conf["feature_selection"] == ["age", "gender", "income"]