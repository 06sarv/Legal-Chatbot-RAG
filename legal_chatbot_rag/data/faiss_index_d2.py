import os
import json
import pandas as pd
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np


DATA_DIR = "/home/sweetyjuhi7/legal_chatbot_rag/legal_chatbot_rag/data/"
MODEL_DIR = "/home/sweetyjuhi7/legal_chatbot_rag/legal_chatbot_rag/data/model"
FAISS_INDEX_PATH = os.path.join(DATA_DIR, "faiss_index_d1")
IPC_CSV_PATH = os.path.join(DATA_DIR, "ipc_sections.csv")


print("🔍 Loading Embedding Model...")
embedding_model = SentenceTransformer("/home/sweetyjuhi7/legal_chatbot_rag/legal_chatbot_rag/data/model")


dimension = 384  
index = faiss.IndexFlatL2(dimension) 

if os.path.exists(FAISS_INDEX_PATH):
    print("⚡ Loading existing FAISS index...")
    index = faiss.read_index(FAISS_INDEX_PATH) 
else:
    print("🚀 Creating new FAISS index...")


documents = []
json_files = ["constitution_qa.json", "crpc_qa.json", "ipc_qa.json"]

for file_name in json_files:
    abs_path = os.path.join(DATA_DIR, file_name)
    if not os.path.exists(abs_path):
        print(f"⚠️ Missing file: {abs_path}, skipping...")
        continue

    print(f"📂 Loading file: {file_name}")
    with open(abs_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        for item in data:
            text = item.get("question", "") + " " + item.get("answer", "")
            documents.append(Document(page_content=text))


if os.path.exists(IPC_CSV_PATH):
    print("📂 Loading IPC Sections from CSV...")
    ipc_df = pd.read_csv(IPC_CSV_PATH)
    
    if "Description" in ipc_df.columns:
        for desc in ipc_df["Description"].dropna():
            documents.append(Document(page_content=desc))
        print(f"✅ Loaded {len(ipc_df)} IPC sections")
    else:
        print("⚠️ 'Description' column not found in IPC CSV!")


if not documents:
    print("❌ No documents found. Exiting...")
    exit()

print("🔄 Splitting documents...")
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = splitter.split_documents(documents)
print(f"✅ Created {len(docs)} document chunks")

texts = [doc.page_content for doc in docs]


print("🔍 Generating embeddings...")
embeddings = embedding_model.encode(texts, convert_to_tensor=True)


print("➕ Adding embeddings to FAISS index...")
index.add(np.array(embeddings))


print("✅ Saving FAISS index...")
faiss.write_index(index, FAISS_INDEX_PATH)
print("✅ FAISS Index Saved Successfully!")
