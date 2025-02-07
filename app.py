import logging
import sqlite3
from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
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
            chat_id TEXT NOT NULL,
            title TEXT,
            question TEXT,
            response TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

init_db()  # Initialize the database on startup

@app.route("/new_chat", methods=["POST"])
def new_chat():
    """Creates a new chat session."""
    chat_id = datetime.datetime.now().strftime("%Y%m%d%H%M%S")  # Unique chat ID based on timestamp
    return jsonify({"chat_id": chat_id})

@app.route("/chat", methods=["POST"])
def chat():
    """Handles user messages and fetches responses."""
    data = request.json
    user_input = data.get("message")
    chat_id = data.get("chat_id")

    if not user_input or not chat_id:
        logger.warning("Missing input or chat ID in request.")
        return jsonify({"error": "Missing input or chat ID"}), 400

    logger.info(f"Received request: {user_input} (Chat ID: {chat_id})")

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

        # If this is the first message, set title
        cursor.execute("SELECT COUNT(*) FROM chats WHERE chat_id = ?", (chat_id,))
        count = cursor.fetchone()[0]
        if count == 0:
            title = user_input[:30]  # First 30 chars of user input as title
            cursor.execute("INSERT INTO chats (chat_id, title, question, response) VALUES (?, ?, ?, ?)",
                           (chat_id, title, user_input, bot_response))
        else:
            cursor.execute("INSERT INTO chats (chat_id, title, question, response) VALUES (?, NULL, ?, ?)",
                           (chat_id, user_input, bot_response))
        conn.commit()
        conn.close()

        logger.info(f"Response from Ollama: {bot_response}")
        return jsonify({"response": bot_response})
    except Exception as e:
        logger.error(f"Error communicating with Ollama: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/chats", methods=["GET"])
def get_chats():
    """Fetches all chat sessions with titles."""
    conn = sqlite3.connect("chat_history.db")
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT chat_id, title FROM chats ORDER BY created_at DESC")
    chats = cursor.fetchall()
    conn.close()

    chat_list = [{"chat_id": c[0], "title": c[1] if c[1] else "Untitled Chat"} for c in chats]
    return jsonify(chat_list)

@app.route("/history/<chat_id>", methods=["GET"])
def get_chat_history(chat_id):
    """Fetches chat history for a specific session."""
    conn = sqlite3.connect("chat_history.db")
    cursor = conn.cursor()
    cursor.execute("SELECT question, response FROM chats WHERE chat_id = ? ORDER BY id ASC", (chat_id,))
    chats = cursor.fetchall()
    conn.close()

    chat_list = [{"question": q, "response": r} for q, r in chats]
    return jsonify(chat_list)

if __name__ == "__main__":
    logger.info("Starting Flask server on port 5000...")
    app.run(host="0.0.0.0", port=5000, debug=True)
