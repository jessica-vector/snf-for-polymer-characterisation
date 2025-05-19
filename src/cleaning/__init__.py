# cleaning/__init__.py
"""
This module provides basic data processing functions for polymer characterisation.
Each function is implemented in its respective file for modularity.
"""

# Import all characterisation functions from the module

from .DSC_clean import clean_dsc_batch, clean_dsc_spectrum

# Add all functions to __all__
__all__ = [
    "clean_dsc_spectrum",
    "clean_dsc_batch",
]
