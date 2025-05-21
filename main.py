import src.cleaning as clean
import src.processing as process

# Process a single DSC file
# single_dsc_data = clean.clean_dsc_spectrum("/Users/jessicaagyemang/Documents/snf/data/DSC/CPI-5-1.csv")
# processed_single_dsc = process.normalize_dsc(single_dsc_data)

# Process batches of files
# dsc_data = clean.clean_dsc_batch("/Users/jessicaagyemang/Documents/snf/data/DSC")
# processed_dsc_data = process.normalize_dsc(dsc_data)

# ftir_data = clean.clean_ftir_batch("/Users/jessicaagyemang/Documents/snf/data/FTIR")
# processed_ftir_data = process.normalize_ftir(ftir_data)

# tga_data = clean.clean_tga_batch("/Users/jessicaagyemang/Documents/snf/data/TGA")
# print(tga_data)
# processed_tga_data = process.normalize_tga(tga_data)
# print(processed_tga_data)

rheology_data = clean.clean_rheology_batch("/Users/jessicaagyemang/Documents/snf/data/Rheology")
processed_rheology_data = process.normalize_rheology(rheology_data)
print(processed_rheology_data)