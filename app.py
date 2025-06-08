import os
import json
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS  # <-- import flask_cors

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

app = Flask(__name__)
CORS(app)  # <-- enable CORS globally

@app.route('/webhook', methods=['POST', 'OPTIONS'])
def get_recipe():
    if request.method == 'OPTIONS':
        # flask-cors handles this automatically but just in case
        return '', 200

    data = request.get_json()
    user_input = data.get("user_input", "")

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama3-70b-8192",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a smart recipe assistant. Suggest recipes based on ingredients and dietary restrictions. If the user gives a dish name, return the full recipe, ingredients, and estimate cost for missing items."
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        }
    )

    reply = response.json()["choices"][0]["message"]["content"]
    return jsonify({"reply": reply})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
