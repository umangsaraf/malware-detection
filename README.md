# Malware-detection

## Abstract

Recent work introduced a model using a Heterogeneous Information Network (HIN) representation of Android applications utilizing a meta-path approach to link applications through the API calls contained within them. It was found with multi-kernel learning, the model was able to identify malicious applications with high accuracy. This recent work was the first approach of this kind to be published; therefore, a replication process would allow for deeper understanding of this approach. In this paper, we introduce a framework for improving upon the model through scalability and testable measures with the purpose of maintaining or increasing accuracy while creating an easily executable pipeline. In particular, we employ dimensionality reduction and stochastic techniques to achieve reasonably replicable results. Additionally, we attempt to understand, through model explainability practices, the inner mechanisms of the complex model to better understand possible inaccuracies which may arise in creating a scaled version of a HIN approach.


## Usage Instructions

In a terminal or command window, navigate to the top-level project directory `malware-detection/` and run

`python3 run.py test`

or

`python3 run.py`


* Instructions

`python3 run.py test` - Runs code on test set of 3 benign and 3 malware apps


`python3 run.py` - Runs project on 1000 benign and 1000 malware apps including data collection pipeline

## Output 


`test-data/processes/app_to_api.json`: structure to create A matrix

`test-data/processes/code_block.json`: structure to create B matrix

`test-data/processes/library_dic.json`: structure to create P matrix

`test-data/processes/test_app_api.json`: structure to create A matrix for test set

`test-data/processes/unique_api.text`: txt file with all unique API's

`test-data/matrix/a_matrix.npz`: Sparse format of A matrix 

`test-data/matrix/b_matrix.npz`: Sparse format of B matrix 

`test-data/matrix/p_matrix.npz`: Sparse format of P matrix 

`results/scores.csv`: Performace metrics of model on diffrent kernels

`charts`: Conatins all ouput charts 


## Description of Contents

The project consists of these portions:
```
PROJECT

├── README.md
├── config
│   ├── data-params.json
|   └── test-params.json
|   └── env.json
├── test-data
│   ├── smalli
│   └── processes
│       ├── app_to_api.json
|       ├── code_block.json
|       └── libray_dic.json 
├── notebooks
│   ├── eda.ipynb
|   ├── coefficient_explaining.ipynb
|   ├── feature_extraction.ipynb
|   ├── model.ipynb
|   └── malware_type.ipynb
├── reports
|   └── malware detection.pdf    
├── src
|    ├── __init__.py
|    ├── build_features.py
|    ├── make_dataset.py
|    ├── elt.py
|    ├─ multi-kernel.py
|    ├─ model.py
|    └──coefficient_analysis.py
├── requirements.txt
├── run.py

``` 

### `src`

* `etl.py`: Library code that executes tasks useful for getting data.
* `make_dataset.PY`: Library code that excutes task useful to cleaning and building dataset
* `build_features.py`: Library code that excutes task to extract features from dataset
* `model.py`: Library code  that excutes task to create and test model.
* `Multi-kernel.py`: Library code pertaining the creation of multi kernel
* `coefficient_analysis.py` : Library code that conatins analysis of model outputs 

### `config`
* `env.json`: conatains dokcer conatiner id and outpaths of all files created after running run.py

* `params.json`: Common parameters for getting data, serving as
  inputs to library code.
  
* `test-set.json`: parameters for running small process on small
  test data.


### `notebooks`

* Jupyter notebooks for *analyses*
  - Contains data cleaning, eda, building features and building the model.




