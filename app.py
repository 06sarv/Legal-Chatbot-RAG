import google.generativeai as genai
from flask import Flask, request, jsonify

app = Flask(__name__)

genai.configure(api_key="AIzaSyDKiZI2ikH8avxkBmHbI2SBi0YL7lfS5kk")
model = genai.GenerativeModel("gemini-1.5-pro-latest")  # Change this if needed

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message")
    
    response = model.generate_content(user_message)
    
    return jsonify({"response": response.text})

if __name__ == "__main__":
    app.run(debug=True)
