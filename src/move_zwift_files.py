import os
import shutil

# Define source and destination folders
source_folder = r"C:\Users\aucla\OneDrive\Documents\Zwift\Activities"
destination_folder = r"G:\My Drive\projects\zwift\data"

# Ensure destination exists
os.makedirs(destination_folder, exist_ok=True)

# Count files to process
files_to_process = []
for filename in os.listdir(source_folder):
    if filename == "inProgressActivity.fit":
        continue  # Skip this file
    src_file = os.path.join(source_folder, filename)
    if os.path.isfile(src_file):
        files_to_process.append(filename)

number_of_files = len(files_to_process)
if number_of_files > 0:
    print(f"Found {number_of_files} files to process.")

    # Move all files from source to destination
    for filename in files_to_process:
        src_file = os.path.join(source_folder, filename)
        dst_file = os.path.join(destination_folder, filename)
        shutil.move(src_file, dst_file)
        print(f"Moved: {filename}")

    print("All Zwift .fit files moved successfully.")
else:
    print("No files to process.")
    exit()
