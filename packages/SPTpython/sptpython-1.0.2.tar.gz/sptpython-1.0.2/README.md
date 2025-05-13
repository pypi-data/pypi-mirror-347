# SPTpython

This package enables simple processing for single-particle tracking data. Currently a command-line interface is supported for processing results, but a GUI is planned to be added later. For details on what commands are supported by the CLI, refer to CLI.py.

This is intended to be used when taking large amounts of similar data in the form of .tif files. Functionality allows for easy comparison between datasets, using SPTpython.compare

## Installation
This project was built on Python 3.8.3, so install it [here](https://www.python.org/downloads/release/python-383/). I am not planning to add support for more recent versions.

Install python as normal, then make sure your pip and setuptools are upgraded:

`python -m pip install --upgrade pip ` 

`pip install --upgrade setuptools`

`pip install SPTpython`

(last updated v1.0.1)