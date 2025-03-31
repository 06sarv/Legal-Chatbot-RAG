import json
import os

# Get the current script directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Ensure we're using the correct 'data' directory
data_dir = script_dir  # Since your JSON files are directly in the 'data' directory

# List the files in the correct directory
try:
    files = os.listdir(data_dir)
    print("Downloaded files:", files)
except FileNotFoundError:
    print(f"Error: The directory '{data_dir}' does not exist.")
    exit(1)

# Load and print sample data from JSON files
for file in files:
    if file.endswith(".json"):
        file_path = os.path.join(data_dir, file)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                print(f"\nSample from {file}:\n", json.dumps(data[:2], indent=2))  # Show first 2 entries
        except Exception as e:
            print(f"Error reading {file}: {e}")
