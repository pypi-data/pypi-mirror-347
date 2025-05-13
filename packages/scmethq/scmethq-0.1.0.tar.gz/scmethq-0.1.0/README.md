# scMethQ
## _single-cell DNA Methylation Analysis Toolkit_

![Python](https://img.shields.io/badge/python-3.9-blue)    ![License](https://img.shields.io/badge/license-GPL--3.0-orange)


![logo](./figure/logo.svg)

This study develops the Python-based tool scMethQ for single-cell DNA methylation data analysis.
The overall architecture of scMethQ is inspired by the Scanpy package, which was designed for scRNA-seq data analysis (Wolf et al., 2018).

## Dependencies

```
anndata==0.11.4
charset_normalizer==3.3.2
click==8.1.7
cosg==1.0.1
cycler==0.12.1
Flask_Board==0.1.0
gseapy==1.1.3
matplotlib==3.7.5
numba==0.58.1
numpy==2.2.5
packaging==25.0
pandas==2.2.3
plotly==5.22.0
psutil==5.9.8
pybedtools==0.10.0
PyComplexHeatmap==1.8.2
pyfaidx==0.8.1.3
pyranges==0.1.2
python_igraph==0.11.8
PyYAML==6.0.2
requests==2.32.3
scanpy==1.9.8
scikit_learn==1.4.0
scipy==1.15.2
seaborn==0.13.2y
tqdm==4.66.1
typing_extensions==4.13.2
setuptools>=65.0
wheel
mudata

```

## Installation
Install the develop version from GitHub source code with

```
git clone https://github.com/Wentting/scMethQ.git 
```

And run

``` 
pip install .
```

Uninstall using

```
pip uninstall scmethq
```

## Usage

See Documentation at  https://wentting.github.io/scMethQ

## Content
- `scMethQ/` contains the python code for the package
- `data`

## Cite