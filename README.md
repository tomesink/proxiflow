[![image](https://badge.fury.io/py/proxiflow.svg)](https://badge.fury.io/py/proxiflow)
[![Documentation Status](https://readthedocs.org/projects/proxiflow/badge/?version=latest)](https://proxiflow.readthedocs.io/en/latest/?badge=latest)
[![PyPI download month](https://img.shields.io/pypi/dm/proxiflow.svg)](https://pypi.python.org/pypi/proxiflow/)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/tomesm/proxiflow/graphs/commit-activity)
[![PyPI license](https://img.shields.io/pypi/l/proxiflow.svg)](https://pypi.python.org/pypi/proxiflow/)
[![tests](https://github.com/tomesm/proxiflow/actions/workflows/tests.yml/badge.svg?branch=v0.1.3)](https://github.com/tomesm/proxiflow/actions/workflows/tests.yml)


# ProxiFlow

ProxiFlow is a data preparation tool for machine learning that performs
data cleaning, normalization, and feature engineering.

## Documentation
Read the full documentation [here](http://proxiflow.readthedocs.io/).

## Usage

To use ProxiFlow, install it via [pip]{.title-ref} (from test PyPi):

``` bash
pip install proxiflow
```

You can then call it from the command line:

``` bash
proxiflow --config-file myconfig.yaml --input-file mydata.csv --output-file cleaned_data.csv
```

Here\'s an example of a YAML configuration file:

``` yaml
data_cleaning:
  remove_duplicates: True
  handle_missing_values:
    drop: True

data_normalization: # mandatory
  min_max: #mandatory but values are not mandatory. It can be left empty
    # Specify columns:
    - Age # not mandatory
  z_score:
    - Price 
  log:
    - Floors

feature_engineering:
  ...
```

The above configuration specifies that duplicate rows should be removed
and missing values should be dropped.

## API

ProxiFlow can also be used as a Python library. Here\'s an example:

``` python
import polars as pl
from proxiflow.config import Config
from proxiflow.core import Cleaner

# Load the data
df = pl.read_csv("mydata.csv")

# Load the configuration
config = Config("myconfig.yaml")

# Preprocess the data
dfl = Cleaner(config)
cleaned_df = dfl.clean_data(df)

# Write the output data
cleaned_df.write_csv("cleaned_data.csv")
```

## TODO

-   \[x\] Data cleaning
-   \[ \] Data normalization
-   \[ \] Feature engineering

Note: only data cleaning is currently implemented; data normalization
and feature engineering are TODO features.
