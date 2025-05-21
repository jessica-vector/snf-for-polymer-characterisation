"""
This module provides various similarity and distance metrics for comparing data samples.
Each function is implemented in its respective file for modularity.
"""

# Import all similarity/distance functions from the modules
from .Similarity import compute_similarity_matrix

# Add all functions to __all__
__all__ = [
    "compute_similarity_matrix"
]


