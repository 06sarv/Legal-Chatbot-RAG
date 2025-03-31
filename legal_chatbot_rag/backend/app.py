iimport google.generativeai as genai
from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Get the API key from environment variables
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("API key is missing! Set it in the .env file.")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-pro-latest")  # Change this if needed

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message")
    
    response = model.generate_content(user_message)
    
    return jsonify({"response": response.text})

if __name__ == "__main__":
    app.run(debug=True)
