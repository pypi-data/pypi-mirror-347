#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
single cell DNA methylation analysis tool 

"""
#from .build_mtx import *
#from ..preprocessing.generate_scm import generate_scm,sliding_windows,features_to_scm,load_features,caculate_bins_residual,feature_to_scm,import_cells,save_cells
from .adaptive_smooth import *
from ..preprocessing.scm import add_meta,load_scm,filter_features,filter_cells,feature_select
from .denovo import denovo
from ._build import import_cells,save_cells,feature_to_scm,features_to_scm
from .feature import sliding_windows,load_features
from ._format import format_check

__all__ = [
    "generate_scm",
    "sliding_windows"
]


