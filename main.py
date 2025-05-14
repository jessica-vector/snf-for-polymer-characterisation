import src.cleaning as clean
import src.processing as process

dsc_data = clean.clean_dsc_batch("data/input_data/csv")
processed_dsc_data = process.process_dsc(dsc_data)

ftir_data = clean.clean_ftir_batch("data/input_data/ftir")
processed_dsc_data = process.process_dsc(dsc_data)