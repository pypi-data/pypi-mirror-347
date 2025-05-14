# 📦 DWrappr
[![pypi](https://img.shields.io/pypi/v/dwrappr.svg)](https://pypi.org/project/dwrappr/)
[![versions](https://img.shields.io/pypi/pyversions/dwrappr.svg)](https://git-ce.rwth-aachen.de/kls/dwrappr)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://git-ce.rwth-aachen.de/kls/dwrappr/-/blob/main/LICENSE?ref_type=heads)

A lightweight and extensible Python package for managing data, tailored for researchers working with structured data.
In addition to general data management features, the package introduces a data structure specifically optimized for ML
research. This common format enables researchers to efficiently test new algorithms and methods,
streamlining collaboration and ensuring consistency in data management across projects.\n

Under development.

## 🧩 Features

- 🗃️ Consistent dataset object structure for handling structured data in ML use cases
- 🔄 Support for building a file-based internal dataset collaboration platform for researchers 
- 🧰 General utilities for managing data like saving and loading


## Help
See [Documentation](https://dwrappr-725c08.pages.git-ce.rwth-aachen.de/) for details.

# 🛠️ Package Installation
```bash
pip install dwrappr
```

## 🚀 Quickstart Example
### show available datasets in directory

```python
# examples/loading_datasets.py
from dwrappr import DataSet

# Adjust the path according to the location of the datasets.
PATH_TO_DATA_DIR = "./datasets/"
available_datasets = DataSet.get_available_datasets_in_folder(path=PATH_TO_DATA_DIR)
print(available_datasets)
```
Example output:
```
                 name  ...                      local_filepath
0   example_dataset_1  ...  ./datasets/example_dataset_1.joblib
1   example_dataset_2  ...  ./datasets/example_dataset_2.joblib
```
---
### load dataset from available datasets
```python
# examples/loading_datasets.py
row_of_dataset_to_load = 0
ds = DataSet.load(available_datasets.iloc[row_of_dataset_to_load]['local_filepath'])
print(ds.as_df.head(2))
```
Example output:
```
[12 rows x 12 columns]
   UDI Product ID Type  Air temperature [K]  ...    HDF    PWF    OSF    RNF
0    1     M14860    M                298.1  ...  False  False  False  False
1    2     L47181    L                298.2  ...  False  False  False  False
```
---
### load dataset directly 
```
# examples/loading_datasets.py
PATH_TO_DATASET = "local path to your dataset"
ds = DataSet.load(PATH_TO_DATASET)
```

## Maintainer
This project is maintained by [Nils](https://git-ce.rwth-aachen.de/nils.klasen).