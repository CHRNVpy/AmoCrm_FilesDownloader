import os
import hashlib
from collections import defaultdict

def hash_file(file_path, block_size=65536):
    """Return the hash of a file for comparison."""
    hash_algo = hashlib.md5()
    with open(file_path, 'rb') as f:
        while chunk := f.read(block_size):
            hash_algo.update(chunk)
    return hash_algo.hexdigest()

def find_duplicate_files(folder_path):
    files_by_size = defaultdict(list)
    files_by_hash = defaultdict(list)

    for dirpath, _, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            file_size = os.path.getsize(file_path)
            files_by_size[file_size].append(file_path)

    for size, file_paths in files_by_size.items():
        if len(file_paths) > 1:
            for file_path in file_paths:
                file_hash = hash_file(file_path)
                files_by_hash[file_hash].append(file_path)

    duplicates = {hash_val: paths for hash_val, paths in files_by_hash.items() if len(paths) > 1}
    return duplicates

folder_path = 'downloads'
duplicate_files = find_duplicate_files(folder_path)

if duplicate_files:
    print("Duplicate files found:")
    for hash_val, files in duplicate_files.items():
        print(f"\nDuplicate group with hash {hash_val}:")
        for file in files:
            print(file)
else:
    print("No duplicate files found.")
