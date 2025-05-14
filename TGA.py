import os

# Define the folder path containing the CSV files
folder_path = '/Users/jessicaagyemang/Documents/snf/data/TGA_clean'

print(f"Processing CSV files in: {folder_path}")

# Get a list of all files in the folder
try:
    files = os.listdir(folder_path)
except FileNotFoundError:
    print(f"Error: Folder not found at {folder_path}")
    files = [] # Empty list to prevent errors later

# Process each .csv file
for file_name in files:
    if file_name.endswith('.csv'):
        filepath = os.path.join(folder_path, file_name)

        print(f"Processing file: {file_name}")

        try:
            # Read all lines from the file
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            # Check if the file is empty or has only one line
            if not lines or len(lines) < 1:
                print(f"Warning: File {file_name} is empty or has only one line. Skipping line removal.")
                # If only one line, we still process it for text replacement
                lines_to_process = lines
            else:
                # Remove the first line by slicing the list
                lines_to_process = lines[1:]

            # Process the remaining lines: replace 'Tr' with 'Temperature'
            modified_lines = []
            for line in lines_to_process:
                # Replace 'Tr' with 'Temperature' in each line
                modified_line = line.replace('Tr', 'Temperature')
                modified_lines.append(modified_line)

            # Write the modified lines back to the same file, overwriting the original
            with open(filepath, 'w', encoding='utf-8') as f:
                f.writelines(modified_lines)

            print(f"Successfully processed and saved: {file_name}")

        except Exception as e:
            print(f"Error processing file {file_name}: {e}")

print("\nProcessing complete.")
