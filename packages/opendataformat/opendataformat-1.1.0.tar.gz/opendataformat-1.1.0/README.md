# opendataformat 

## Overview

The `opendataformat` package is specifically designed to facilitate the seamless utilization of the Open Data Format (ODF). It offers functionality to import data from the Open Data Format into a Python pandas data frame, as well as export data from a Pandas data frame to the Open Data Format. You can easily access comprehensive information about the dataset and variables in Python. This user-friendly approach ensures convenient exploration and utilization of dataset information within your preferred environment.

For more comprehensive insights into the Open Data Format specification, please visit: [Open Data Format Specification](https://opendataformat.github.io/specification). This resource provides detailed documentation and profiles illustrating the storage locations of attributes within the Open Data Format, as well as within the native formats to which they will be converted. Additionally, you can download a practical example of [real data in the Open Data Format](https://opendataformat.github.io/files/example_dataset_v1_1_0.odf.zip).


## Getting started

``` py
import opendataformat as odf
```

The opendataformat package consists of five main functions:

- `odf.read_odf()` to read an Open Data Format file in Pandas. This function takes an input parameter "filepath", which is the path to the Open Data Format ZIP file.

- `odf.docu_odf()` to display or retrieve metadata for a ODF data frame or a variable / column.

- `odf.write_odf()` to write the Pandas Dataframe to an Open Data Format ZIP file. By specifying the dataframe input and providing the output directory path the function will generate a ODF ZIP file (.odf.zip) containing the dataset as "data.csv" and "metadata.xml", as well as an version file "odf-version.json" (since ODF version 1.1.0).


### Multilingual Datasets

When working with a multilingual dataset, the `opendataformat` package provides the option to specify the language you want to work with for the main functions: `read_odf()`, `docu_odf()`, and `write_odf()`.
 
You can achieve this by using the `languages` argument and setting it to either `all` to include all languages, or by specifying the language code such as `de` for German or `en` for English. 
This allows you to easily select the desired language for your dataset operations.
The language codes are defined by the [ISO 639-1](https://de.wikipedia.org/wiki/Liste_der_ISO-639-1-Codes).


## Getting help

If you encounter a clear bug, please file a minimal reproducible example
on **https://github.com/opendataformat/python-package-opendataformat/issues**. 
