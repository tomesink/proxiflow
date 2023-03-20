Get started
===========

ProxiFlow is a data preparation tool for machine learning that performs data cleaning, normalization, and feature engineering.

Usage
-----

To use ProxiFlow, install it via `pip`:

.. code-block:: bash

    pip install proxiflow

You can then call it from the command line:

.. code-block:: bash

    proxiflow --config-file myconfig.yaml --input-file mydata.csv --output-file cleaned_data.csv

Here's an example of a YAML configuration file:

.. code-block:: yaml

    input_format: csv
    output_format: csv

    data_cleaning: #mandatory
      # NOTE: Not handling missing values can cause errors during data normalization
      handle_missing_values:
        drop: false
        mean: true # Only Int and Float columns are handled 
        # mode: true # Turned off for now. 

      handle_outliers: true # Only Float columns are handled
      remove_duplicates: true

    data_normalization: # mandatory
      min_max: #mandatory but values are not mandatory. It can be left empty
        # Specify columns:
        - Age # not mandatory
      z_score: 
        - Price 
      log:
        - Floors

    feature_engineering:
      one_hot_encoding: # mandatory
        - Bedrooms      # not mandatory

      feature_scaling:  # mandatory
        degree: 2       # not mandatory. It specifies the polynominal degree
        columns:        # not mandatory
          - Floors      # not mandatory
      ...

The above configuration specifies that duplicate rows should be removed and missing values should be dropped.

API
---

ProxiFlow can also be used as a Python library. Here's an example:

.. code-block:: python

    import polars as pl
    from proxiflow.config import Config
    from proxiflow.core import Cleaner

    # Load the data
    df = pl.read_csv("mydata.csv")

    # Load the configuration
    config = Config("myconfig.yaml")

    # Preprocess the data

    # Clean the data
    cleaner = Cleaner(config)
    cleaned_data = cleaner.clean_data(data)

    # Perform data normalization
    normalizer = Normalizer(config)
    normalized_data = normalizer.normalize(cleaned_data)

    # Perform feature engineering
    engineer = Engineer(config)
    engineered_data = engineer.execute(normalized_data)

    # Write the output data
    engineered_data.write_csv("cleaned_data.csv")

Log
---

- [x] Data cleaning
- [x] Data normalization
- [x] Feature engineering

