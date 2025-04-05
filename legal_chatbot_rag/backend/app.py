import os
import sys
import json
import faiss
import numpy as np
from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import google.generativeai as genai

# Allow import from data directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data')))
from documents import documents  # ⬅️ your full document list (JSON + CSV)

# Load environment variables
load_dotenv()

DATA_DIR = "/home/sweetyjuhi7/legal_chatbot_rag/legal_chatbot_rag/data/"
FAISS_INDEX_PATH = os.path.join(DATA_DIR, "faiss_index")

print("🔍 Loading Embedding Model...")
embedding_model = SentenceTransformer(os.path.join(DATA_DIR, "model"))

print("📥 Loading FAISS index...")
index = faiss.read_index(FAISS_INDEX_PATH)

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("API key is missing! Set it in the .env file.")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-pro-latest")

print("📄 Loading all legal documents...")
print(f"📄 Total documents loaded: {len(documents)}")

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the Legal Chatbot API! Use /chat for interacting with the chatbot."})

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        if not data or "message" not in data:
            return jsonify({"error": "Missing 'message' field in request"}), 400

        user_message = data["message"]
        print(f"🔹 Received message: {user_message}")

        # Get query embedding
        query_embedding = embedding_model.encode([user_message])
        query_embedding = np.array(query_embedding).reshape(1, -1)

        # Search FAISS index
        print("🔍 Searching for relevant documents in FAISS index...")
        k = 3
        D, I = index.search(query_embedding, k)
        print(f"🔍 FAISS results: Indices: {I}, Distances: {D}")

        # Collect top documents
        top_results = []
        for i, idx in enumerate(I[0]):
            if 0 <= idx < len(documents):
                top_results.append(documents[idx])

        # If FAISS returns valid results, use them
        if top_results:
            context = " ".join(top_results)
            prompt = f"{context}\n\nUser: {user_message}"
            response = model.generate_content(prompt)
        else:
            print("⚠️ No relevant documents found. Falling back to Gemini only.")
            response = model.generate_content(user_message)

        if response and hasattr(response, "text"):
            return jsonify({
                "response": response.text,
                "source": "FAISS + Gemini" if top_results else "Gemini only",
                "matches_found": len(top_results)
            })
        else:
            return jsonify({"error": "Invalid response from Gemini"}), 500

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
