import os
import json
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from sentence_transformers import SentenceTransformer

# Define Paths
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # Get current script directory
DATA_DIR = os.path.join(BASE_DIR, "")  # Ensure correct relative paths
MODEL_DIR = os.path.join(BASE_DIR, "model")  # Path to model directory
FAISS_INDEX_PATH = os.path.join(BASE_DIR, "faiss_index")

# ✅ Load pre-trained embedding model
print("🔍 Loading Embedding Model...")
embedding_model = HuggingFaceEmbeddings(model_name=MODEL_DIR)

# ✅ Load JSON files
documents = []
for file_name in ["constitution_qa.json", "crpc_qa.json", "ipc_qa.json"]:
    abs_path = os.path.join(DATA_DIR, file_name)
    if not os.path.exists(abs_path):
        print(f"⚠️ Missing file: {abs_path}")
        continue

    print(f"📂 Loading file: {file_name}")
    with open(abs_path, "r", encoding="utf-8") as f:
        data = json.load(f)

        # ✅ Debug: Show how many records are loaded
        print(f"✅ Loaded {len(data)} entries from {file_name}")

        for item in data:
            text = item.get("question", "") + " " + item.get("answer", "")
            documents.append(Document(page_content=text))

# ❌ Stop if no documents loaded
if not documents:
    print("❌ No documents found. Exiting...")
    exit()

# ✅ Split text into chunks
print("🔄 Splitting documents...")
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = splitter.split_documents(documents)
print(f"✅ Created {len(docs)} document chunks")

# ✅ FAISS Indexing
if os.path.exists(FAISS_INDEX_PATH):
    print("⚡ FAISS index already exists! Skipping creation.")
else:
    print("🚀 Creating FAISS index...")

    # Create FAISS index with correct embedding object
    vector_db = FAISS.from_documents(docs, embedding_model)

    vector_db.save_local(FAISS_INDEX_PATH)
    print("✅ FAISS Index Created Successfully!")
