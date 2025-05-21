from sklearn.metrics import pairwise_distances
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean
import numpy as np
from scipy.stats import pearsonr

def compute_similarity_matrix(profiles, metric='dtw'):
    """
    Compute an N x N similarity matrix for given sample profiles.
    
    Parameters:
    -----------
    profiles : dict
        Mapping sample_id -> 2D array [x, y] (assuming same x grid for all)
    metric : str
        One of: 'dtw', 'euclidean', 'pearson', 'cosine'
        
    Returns:
    --------
    tuple
        (sample_ids, similarity_matrix) where similarity_matrix is a NumPy array
    """
    sample_ids = sorted(profiles.keys())
    n = len(sample_ids)
    # Initialize distance matrix
    dist_matrix = np.zeros((n, n))
    
    # Compute pairwise distances
    for i in range(n):
        for j in range(i+1, n):
            # Extract y-values (weight percentages) for comparison
            curve_i = np.asarray(profiles[sample_ids[i]][:, 1], dtype=np.float64)  # y-values
            curve_j = np.asarray(profiles[sample_ids[j]][:, 1], dtype=np.float64)  # y-values
            
            # Debug prints
            # print(f"curve_i shape: {curve_i.shape}")
            # print(f"curve_i ndim: {curve_i.ndim}")
            # print(f"curve_j shape: {curve_j.shape}")
            # print(f"curve_j ndim: {curve_j.ndim}")
            
            # Ensure 1D arrays
            curve_i = curve_i.ravel()
            curve_j = curve_j.ravel()
            
            if metric == 'dtw':
                # Dynamic Time Warping distance
                dist, _ = fastdtw(curve_i, curve_j, dist=lambda x, y: abs(x - y))
                dist_matrix[i, j] = dist_matrix[j, i] = dist
                
            elif metric == 'pearson':
                # Pearson correlation (1 - correlation to convert to distance)
                corr, _ = pearsonr(curve_i, curve_j)
                dist = 1 - corr  # Convert correlation to distance
                dist_matrix[i, j] = dist_matrix[j, i] = dist
                
            elif metric in ['euclidean', 'cosine']:
                # Use pairwise_distances for these metrics
                d = pairwise_distances(curve_i.reshape(1, -1), 
                                    curve_j.reshape(1, -1), 
                                    metric=metric)[0,0]
                dist_matrix[i, j] = dist_matrix[j, i] = d
                
            else:
                raise ValueError(f"Unsupported metric: {metric}. Choose from: 'dtw', 'euclidean', 'pearson', 'cosine'")
    
    # Convert distance matrix to similarity matrix
    # For DTW and Euclidean: scale distances first then sim = 1 / (1 + dist)
    # For Pearson and Cosine: sim = 1 - dist (since they're already in [0,1] range)
    if metric in ['dtw', 'euclidean']:
        # Scale distances to [0,1] range
        if dist_matrix.max() > 0:  # Avoid division by zero
            dist_matrix = dist_matrix / dist_matrix.max()
        sim_matrix = 1 / (1.0 + dist_matrix)
    else:  # pearson, cosine
        sim_matrix = 1 - dist_matrix
    
    # Set self-similarity to 1.0
    np.fill_diagonal(sim_matrix, 1.0)
    
    return sample_ids, sim_matrix

# Compute similarity matrices for each modality with recommended metrics

