from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
import traceback

# Make sure we can import from the /data folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data')))

from documents import documents  # List of documents to query
import faiss
import pickle
from sentence_transformers import SentenceTransformer
import google.generativeai as genai

# --- Setup ---
app = Flask(__name__)
CORS(app)

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Load Gemini API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Load FAISS index
print("🔍 Loading Embedding Model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

print("📥 Loading FAISS index...")
index_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'faiss_index')
index = faiss.read_index(index_path)

with open(os.path.join(os.path.dirname(__file__), '..', 'data', 'documents.pkl'), 'rb') as f:
    faiss_documents = pickle.load(f)

print("📄 Loaded documents:", len(faiss_documents))

# Store chat history
chat_history = []

# --- Routes ---
@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_input = request.json.get("message")

        if not user_input:
            return jsonify({"error": "Message is required."}), 400

        # Add user message to history
        chat_history.append({"role": "user", "message": user_input})

        # Get embedding
        user_embedding = model.encode([user_input])
        D, I = index.search(user_embedding, k=3)

        # Get top matched documents
        context = ""
        for idx in I[0]:
            if idx < len(faiss_documents):
                context += faiss_documents[idx] + "\n"

        if context.strip() == "":
            context = "No matching documents found. Please generate a helpful answer."

        prompt = f"""You are a legal assistant chatbot. Answer based on the following legal context:\n\n{context}\n\nUser: {user_input}"""

        model_gemini = genai.GenerativeModel(model_name="models/gemini-1.5-pro")

        response = model_gemini.generate_content(prompt)

        # Add bot response to history
        bot_reply = response.text.strip()
        chat_history.append({"role": "assistant", "message": bot_reply})

        return jsonify({
            "response": bot_reply,
            "chat_history": chat_history
        })

    except Exception as e:
        traceback.print_exc()
        return jsonify({
            "error": "Oops! Something went wrong while processing your request.",
            "details": str(e)
        }), 500

@app.route("/history", methods=["GET"])
def get_history():
    return jsonify(chat_history)

# --- Extra Endpoints ---
@app.route("/reset", methods=["POST"])
def reset_chat():
    chat_history.clear()
    return jsonify({"message": "Chat history has been cleared."})

@app.route("/status", methods=["GET"])
def status():
    return jsonify({"status": "Legal chatbot backend is running."})

@app.route("/models", methods=["GET"])
def list_models():
    models = [{"name": m.name, "methods": m.supported_generation_methods} for m in genai.list_models()]
    return jsonify(models)

# --- Main ---
if __name__ == "__main__":
    app.run(debug=True)

