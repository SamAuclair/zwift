import os
import shutil

# Define source and destination folders
source_folder = r"C:\Users\aucla\OneDrive\Documents\Zwift\Activities"
destination_folder = r"G:\My Drive\projects\zwift\data"

# Ensure destination exists
os.makedirs(destination_folder, exist_ok=True)

# Move all files from source to destination
for filename in os.listdir(source_folder):
    if filename == "inProgressActivity.fit":
        continue  # Skip this file
    src_file = os.path.join(source_folder, filename)
    dst_file = os.path.join(destination_folder, filename)
    if os.path.isfile(src_file):
        shutil.move(src_file, dst_file)
        print(f"Moved: {filename}")

print("All Zwift .fit files moved successfully.")
