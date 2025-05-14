import os
import re

# Define the source directory containing the files
# IMPORTANT: Replace this path with the actual path to your folder if it's different
source_directory = '/Users/jessicaagyemang/Documents/snf/data/FTIR'

# Define the destination directory where renamed files will be moved
# IMPORTANT: You can change this path if you want the new folder elsewhere
destination_directory = '/Users/jessicaagyemang/Documents/snf/data/FTIR_renamed'

print(f"Checking files in source directory: {source_directory}")
print(f"Renamed files will be moved to: {destination_directory}")

# Check if the source directory exists
if not os.path.isdir(source_directory):
    print(f"Error: Source directory not found at {source_directory}")
else:
    # Create the destination directory if it doesn't exist
    if not os.path.exists(destination_directory):
        try:
            os.makedirs(destination_directory)
            print(f"Created destination directory: {destination_directory}")
        except OSError as e:
            print(f"Error creating destination directory {destination_directory}: {e}")
            # Exit the script if the destination directory cannot be created
            exit()

    # Iterate through all items in the source directory
    for filename in os.listdir(source_directory):
        # Construct the full path to the original file
        old_filepath = os.path.join(source_directory, filename)

        # Check if it's a file (not a directory)
        if os.path.isfile(old_filepath):
            # Define the updated pattern to look for, specifically starting with 'CPI-5-'
            # This regex now accounts for a file extension (like .CSV) after the number.
            # It looks for:
            # ^(CPI-5-[\w-]+)  -> Starts with 'CPI-5-', followed by word chars/hyphens (captured as group 1)
            # \.              -> A literal dot
            # (\w+)           -> One or more word characters (captured as group 2)
            # \.              -> A literal dot (before the extension)
            # (CSV|csv)$      -> The extension 'CSV' or 'csv' at the end of the string (captured as group 3)
            pattern = re.compile(r'^(CPI-5-[\w-]+)\.(\w+)\.(CSV|csv)$')


            # Try to match the pattern in the filename
            match = pattern.match(filename)

            # --- Debugging Prints ---
            print(f"\nProcessing file: '{filename}'")
            if match:
                print(f"  Pattern matched.")
                # Extract the parts before and after the dot we want to replace
                part_before_dot = match.group(1) # e.g., 'CPI-5-9'
                part_after_dot = match.group(2)  # e.g., '2'
                extension = match.group(3)       # e.g., 'CSV'

                # Construct the new filename by replacing the dot with an underscore and keeping the extension
                new_filename = f"{part_before_dot}_{part_after_dot}.{extension}"
                print(f"  Proposed new name: '{new_filename}'")
                print(f"  Old path: '{old_filepath}'")
                new_filepath = os.path.join(destination_directory, new_filename)
                print(f"  New path: '{new_filepath}'")
            else:
                print(f"  Pattern did NOT match.")
            # --- End Debugging Prints ---


            # If the pattern matches
            if match:
                # Extract the parts before and after the dot we want to replace
                part_before_dot = match.group(1) # e.g., 'CPI-5-9'
                part_after_dot = match.group(2)  # e.g., '2'
                extension = match.group(3)       # e.g., 'CSV'

                # Construct the new filename by replacing the dot with an underscore and keeping the extension
                new_filename = f"{part_before_dot}_{part_after_dot}.{extension}"
                # Construct the full path to the new file in the destination directory
                new_filepath = os.path.join(destination_directory, new_filename)

                # Check if the new filename is different from the old one (in the source directory)
                # and if a file with the new name doesn't already exist in the destination
                if os.path.exists(new_filepath):
                     print(f"Skipping '{filename}': File with new name '{new_filename}' already exists in destination.")
                elif old_filepath != new_filepath:
                    try:
                        # Rename (and move) the file
                        os.rename(old_filepath, new_filepath)
                        print(f"SUCCESS: Renamed and moved '{filename}' to '{new_filename}' in {destination_directory}")
                    except OSError as e:
                        print(f"Error renaming and moving file {filename}: {e}")
                # The 'else' for old_filepath != new_filepath is not needed here as we are moving to a new dir

            # else:
                # print(f"Skipping '{filename}': Does not match the expected 'CPI-5-X.Y.CSV' pattern.")

print("Renaming and moving process finished.")
