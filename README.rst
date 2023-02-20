Prepflow
========

Prepflow is a data preparation tool for machine learning that performs data cleaning, normalization, and feature engineering.

Usage
-----

To use Prepflow, install it via `pip` (from test PyPi):

.. code-block:: bash

    pip install --find-links ./wheels --index-url https://test.pypi.org/simple prepflow==0.1.2

You can then call it from the command line:

.. code-block:: bash

    prepflow --config-file myconfig.yaml --input-file mydata.csv --output-file cleaned_data.csv

Here's an example of a YAML configuration file:

.. code-block:: yaml

    data_cleaning:
      remove_duplicates: True
      handle_missing_values:
        drop: True

    data_normalization:
      ...

    feature_engineering:
      ...

The above configuration specifies that duplicate rows should be removed and missing values should be dropped.

API
---

Prepflow can also be used as a Python library. Here's an example:

.. code-block:: python

    import polars as pl
    from preppy.config import Config
    from preppy.preprocessor import Preprocessor

    # Load the data
    df = pl.read_csv("mydata.csv")

    # Load the configuration
    config = Config("myconfig.yaml")

    # Preprocess the data
    preprocessor = Preprocessor(config)
    cleaned_df = preprocessor.clean_data(df)

    # Write the output data
    cleaned_df.write_csv("cleaned_data.csv")

TODO
----

- [x] Data cleaning
- [ ] Data normalization
- [ ] Feature engineering

Note: only data cleaning is currently implemented; data normalization and feature engineering are TODO features.
