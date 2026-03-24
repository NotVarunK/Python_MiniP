from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from chatbot import get_response

app = Flask(__name__)
CORS(app)

# Serve index.html
@app.route("/")
def home():
    return send_from_directory('.', 'index.html')

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "")
    session = data.get("session", "default")

    if not message:
        return jsonify({"reply": "Please type something!"})

    reply = get_response(message, session=session)
    return jsonify({"reply": reply})

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"MediBot running on port {port}")
    app.run(host="0.0.0.0", port=port)5000)
