import os
import string

def get_alphabet_prefix(index):
    """ Converts an index to an alphabetical sequence like A, B, ..., Z, AA, AB, ..., ZZ, AAA """
    prefix = ""
    while index >= 0:
        prefix = string.ascii_uppercase[index % 26] + prefix
        index = (index // 26) - 1
    return prefix

def rename_videos(directory):
    # Get all MP4 files in the folder
    files = [f for f in os.listdir(directory) if f.lower().endswith(".mp4")]
    
    # Sort files alphabetically (so A, B, ..., Z, AA, AB, etc. are in correct order)
    files.sort()

    # Rename files with numeric prefixes
    for index, filename in enumerate(files, start=1):
        parts = filename.split(" - ", 1)  # Splitting to extract prefix
        if len(parts) == 2:
            _, rest_of_name = parts  # Get the part after the first dash
        else:
            rest_of_name = filename  # If no dash, keep full name

        new_name = f"{index:02d} - {rest_of_name}"  # Prefix number (01, 02, ...)
        old_path = os.path.join(directory, filename)
        new_path = os.path.join(directory, new_name)

        os.rename(old_path, new_path)
        print(f"Renamed: {filename} → {new_name}")

# Change this to your actual downloads folder
download_folder = "Downloads"

rename_videos(download_folder)
print("Renaming completed!")
