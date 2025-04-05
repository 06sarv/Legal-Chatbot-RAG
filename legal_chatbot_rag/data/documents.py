import json
import pandas as pd
import os

# Get the directory of the current file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load the JSON datasets
with open(os.path.join(BASE_DIR, 'constitution_qa.json'), 'r') as f:
    constitution_data = json.load(f)

with open(os.path.join(BASE_DIR, 'crpc_qa.json'), 'r') as f:
    crpc_data = json.load(f)

with open(os.path.join(BASE_DIR, 'ipc_qa.json'), 'r') as f:
    ipc_data = json.load(f)

# Load the IPC sections CSV
ipc_df = pd.read_csv(os.path.join(BASE_DIR, 'ipc_sections.csv'))

# Create a list of documents
documents = []

# Add the text from JSON datasets
for data in constitution_data + crpc_data + ipc_data:
    documents.append(data['question'] + " " + data['answer'])

# Add the IPC sections from the CSV
for _, row in ipc_df.iterrows():
    documents.append(row['Section'])  # Ensure 'Section' is the correct column name
