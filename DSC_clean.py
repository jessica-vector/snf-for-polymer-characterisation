import pandas as pd
import os

# Define the path to your folder
folder_path = '/Users/jessicaagyemang/Documents/snf/data/DSC/3_Heat'
output_folder_name = 'DSC_Clean'
output_folder_path = os.path.join(folder_path, output_folder_name)

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)
    print(f"Created output folder: {output_folder_path}")

print(f"Looking for CSV files in: {folder_path}")

# Iterate through all files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        file_path = os.path.join(folder_path, filename)
        output_file_path = os.path.join(output_folder_path, filename)

        print(f"Processing file: {filename}")

        try:
            # Read the CSV file
            df = pd.read_csv(file_path)

            # Check if the DataFrame is empty or has only one column
            if df.empty:
                print(f" - File is empty, skipping: {filename}")
                continue
            if df.shape[1] < 2:
                 print(f" - File has only one column or less, skipping time column removal: {filename}")
                 # Optionally, you could copy this file as is to the output folder
                 # df.to_csv(output_file_path, index=False)
                 continue


            # Verify the header of the first column (optional but good practice)
            # You can skip this check if you are absolutely certain the first column
            # is always 'Time' and you want to remove the first column regardless of header.
            # first_column_header = df.columns[0]
            # if first_column_header != 'Time':
            #     print(f" - Warning: First column header is '{first_column_header}' not 'Time' in {filename}. Removing the first column anyway.")
            # else:
            #      print(f" - Confirmed first column is 'Time'.")


            # Remove the first column (index 0)
            # axis=1 means drop columns, inplace=True modifies the DataFrame directly
            # To be safer and create a new DataFrame: df_modified = df.drop(df.columns[0], axis=1)
            df_modified = df.drop(df.columns[0], axis=1)


            # Save the modified DataFrame to a new CSV file in the output folder
            # index=False prevents pandas from writing the DataFrame index as a column
            df_modified.to_csv(output_file_path, index=False)

            print(f" - Successfully processed and saved to: {output_file_path}")

        except Exception as e:
            print(f" - Error processing file {filename}: {e}")

print("Processing complete.")