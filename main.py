import src.cleaning as clean
import src.processing as process

dsc_data = clean.clean_dsc_batch("data/input_data/csv")
processed_dsc_data = process.process_dsc(dsc_data)

ftir_data = clean.clean_ftir_batch("data/input_data/ftir")
processed_ftir_data = process.process_ftir(ftir_data)

tga_data = clean.clean_tga_batch("data/input_data/tga")
processed_tga_data = process.process_tga(tga_data)

rheology_data = clean.clean_rheology_batch("data/input_data/rheology")
processed_rheology_data = process.process_rheology(rheology_data)