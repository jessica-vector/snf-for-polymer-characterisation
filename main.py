import src.cleaning as clean
import src.processing as process
import src.SNF as snf
import src.SNF.Matrices as matrices
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Processing and Cleaning


# single_dsc_data = clean.clean_dsc_spectrum("/Users/jessicaagyemang/Documents/snf/data/DSC/CPI-5-1.csv")
# processed_single_dsc = process.normalize_dsc(single_dsc_data)
# dsc_data = clean.clean_dsc_batch("/Users/jessicaagyemang/Documents/snf/data/DSC")
# processed_dsc_data = process.normalize_dsc(dsc_data)
# print(processed_dsc_data)
# ftir_data = clean.clean_ftir_batch("/Users/jessicaagyemang/Documents/snf/data/FTIR")
# processed_ftir_data = process.normalize_ftir(ftir_data)


tga_data = clean.clean_tga_batch("/Users/jessicaagyemang/Documents/snf/data/TGA")
processed_tga_data = process.normalize_tga(tga_data)
similarity_tga_data = process.prepare_data_for_dtw(processed_tga_data)
# print(similarity_tga_data)
# print(processed_tga_data)

# Get both sample IDs and similarity matrix
sample_ids, similarity_matrix = matrices.compute_similarity_matrix(similarity_tga_data, metric='euclidean')

# Define the desired sample order
desired_order = [
    'CPI-5-1', 'CPI-5-2', 'CPI-5-3', 'CPI-5-4', 'CPI-5-5', 'CPI-5-6', 'CPI-5-7', 'CPI-5-8', 
    'CPI-5-9', 'CPI-5-10', 'CPI-5-11', 'CPI-5-12', 'LDPE-Virgin', 'LDPE-Carmel-Eco', 
    'LDPE-EXP1', 'LDPE-EXP4'
]

# Create a mapping from current sample IDs to desired order
clean_sample_ids = [Path(id).stem for id in sample_ids]
current_to_desired = {old: new for old, new in zip(clean_sample_ids, desired_order)}

# Reorder the similarity matrix
order_mapping = {id: i for i, id in enumerate(desired_order)}
current_order = [order_mapping[current_to_desired[id]] for id in clean_sample_ids]
reordered_matrix = similarity_matrix[np.ix_(current_order, current_order)]

# Create a heatmap visualization of the similarity matrix
plt.figure(figsize=(10, 8))
sns.heatmap(reordered_matrix, 
            cmap='viridis', 
            annot=True, 
            fmt='.2f', 
            cbar_kws={'label': 'Similarity Score'},
            xticklabels=desired_order,
            yticklabels=desired_order)
plt.title('TGA Data Similarity Matrix')
plt.xlabel('Sample ID')
plt.ylabel('Sample ID')
plt.tight_layout()
plt.show()

# rheology_data = clean.clean_rheology_batch("/Users/jessicaagyemang/Documents/snf/data/Rheology")
# processed_rheology_data = process.normalize_rheology(rheology_data)
# print(processed_rheology_data)



# Similarity Matrices

# rheology_matrix = matrices.dtw_similarity_matrix(processed_rheology_data)
# tga_matrix = matrices.dtw_similarity_matrix(processed_tga_data)
# dsc_matrix = matrices.dtw_similarity_matrix(processed_dsc_data)
# ftir_matrix = matrices.pearson_correlation_matrix(processed_ftir_data)





