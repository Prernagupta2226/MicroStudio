import logging
import sqlite3
from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Allow frontend requests

# Ollama local API endpoint
OLLAMA_API_URL = "http://localhost:11434/api/generate"

# Database setup
def init_db():
    conn = sqlite3.connect("chat_history.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT,
            response TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()  # Initialize the database on startup

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    if not user_input:
        logger.warning("No input provided in request.")
        return jsonify({"error": "No input provided"}), 400

    logger.info(f"Received request: {user_input}")

    payload = {
        "model": "llama2",  # Change this if using a different model
        "prompt": user_input,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_API_URL, json=payload)
        response_data = response.json()
        bot_response = response_data.get("response", "No response")

        # Store chat in database
        conn = sqlite3.connect("chat_history.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO chats (question, response) VALUES (?, ?)", (user_input, bot_response))
        conn.commit()
        conn.close()

        logger.info(f"Response from Ollama: {bot_response}")
        return jsonify({"response": bot_response})
    except Exception as e:
        logger.error(f"Error communicating with Ollama: {str(e)}")
        return jsonify({"error": str(e)})

@app.route('/history', methods=['GET'])
def get_history():
    conn = sqlite3.connect("chat_history.db")
    cursor = conn.cursor()
    cursor.execute("SELECT question, response FROM chats ORDER BY id DESC")
    chats = cursor.fetchall()
    conn.close()
    
    chat_list = [{"question": q, "response": r} for q, r in chats]
    return jsonify(chat_list)

if __name__ == '__main__':
    logger.info("Starting Flask server on port 5000...")
    app.run(host='0.0.0.0', port=5000, debug=True)
