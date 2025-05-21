# processing/__init__.py
"""
This module provides basic data processing functions for polymer characterisation.
Each function is implemented in its respective file for modularity.
"""

# Import all characterisation functions from the modules
from .DSC_process import normalize_dsc
from .FTIR_process import normalize_ftir
from .TGA_process import normalize_tga, prepare_data_for_dtw
from .Rheology_process import normalize_rheology


# Add all functions to __all__
__all__ = [
    "normalize_dsc",
    "normalize_ftir",
    "normalize_tga",
    "prepare_data_for_dtw",
    "normalize_rheology",

]
